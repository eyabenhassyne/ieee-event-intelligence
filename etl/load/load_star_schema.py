from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Any

import pandas as pd
from psycopg2.extras import execute_values

from etl.common.database import get_connection
from etl.common.logging_utils import configure_logging
from etl.common.normalization import (
    blank_to_none,
    build_location_signature,
    normalize_list_field,
    normalize_text,
    parse_bool,
    parse_decimal,
    parse_int,
    parse_timestamp,
)
from etl.common.validation import (
    IssueRecord,
    validate_end_time,
    validate_event_id,
    validate_latitude,
    validate_longitude,
    validate_nonnegative,
)


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR / "raw"
SCHEMA_DIR = BASE_DIR / "database" / "schema"
LOG = configure_logging("etl_load_star_schema")

PREFERRED_EVENTS = PROCESSED_DIR / "events_analytics.csv"
FALLBACK_EVENTS = PROCESSED_DIR / "events_clean.csv"


@dataclass
class SourceSpec:
    label: str
    path: Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def row_count_csv(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return max(sum(1 for _ in fh) - 1, 0)


def choose_events_source() -> SourceSpec:
    if PREFERRED_EVENTS.exists():
        return SourceSpec("events_analytics.csv", PREFERRED_EVENTS)
    return SourceSpec("events_clean.csv", FALLBACK_EVENTS)


def load_events_dataframe(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def normalized_location_signature(row: pd.Series) -> str | None:
    return build_location_signature(
        row.get("city"),
        row.get("address1"),
        row.get("building"),
        row.get("room_number"),
        row.get("latitude"),
        row.get("longitude"),
        row.get("location_type"),
    )


def load_sql_text(name: str) -> str:
    return (SCHEMA_DIR / name).read_text(encoding="utf-8")


def execute_sql_file(cur, name: str) -> None:
    cur.execute(load_sql_text(name))


def start_etl_run(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO audit.etl_run (process_name, status, started_at, message)
            VALUES (%s, %s, current_timestamp, %s)
            RETURNING etl_run_id
            """,
            ("IEEE_EVENT_STAR_SCHEMA_LOAD", "STARTED", "ETL started"),
        )
        return cur.fetchone()[0]


def finish_etl_run(conn, etl_run_id: int, status: str, extracted: int, loaded: int, rejected: int, warnings: int, errors: int, message: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE audit.etl_run
            SET completed_at = current_timestamp,
                status = %s,
                rows_extracted = %s,
                rows_loaded = %s,
                rows_rejected = %s,
                warning_count = %s,
                error_count = %s,
                message = %s
            WHERE etl_run_id = %s
            """,
            (status, extracted, loaded, rejected, warnings, errors, message, etl_run_id),
        )
    conn.commit()


def register_source_file(conn, etl_run_id: int, path: Path, file_name: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO audit.source_file (etl_run_id, file_name, file_path, file_hash, row_count, extracted_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                etl_run_id,
                file_name,
                str(path.relative_to(BASE_DIR)) if path.is_relative_to(BASE_DIR) else str(path),
                sha256_file(path),
                row_count_csv(path),
                datetime.fromtimestamp(path.stat().st_mtime),
            ),
        )


def ensure_unknown_members(conn) -> None:
    with conn.cursor() as cur:
        execute_sql_file(cur, "003_seed_unknown_members.sql")


def load_dim_date(conn, min_date: date, max_date: date) -> None:
    if min_date is None or max_date is None:
        return
    rows = []
    current = min_date
    while current <= max_date:
        rows.append(
            (
                int(current.strftime("%Y%m%d")),
                current,
                current.day,
                current.strftime("%A"),
                current.isoweekday(),
                int(current.strftime("%U")) + 1,
                current.month,
                current.strftime("%B"),
                (current.month - 1) // 3 + 1,
                current.year,
                current.weekday() >= 5,
            )
        )
        current = current.fromordinal(current.toordinal() + 1)
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_date (
                date_key, full_date, day_number, day_name, weekday_number, week_number,
                month_number, month_name, quarter_number, year_number, is_weekend
            ) VALUES %s
            ON CONFLICT (full_date) DO NOTHING
            """,
            rows,
        )


def upsert_dim_category(conn, df: pd.DataFrame) -> None:
    if not {"category_id", "name"}.issubset(df.columns):
        return
    rows = [
        (
            parse_int(r.get("category_id")),
            normalize_text(r.get("name")),
            parse_bool(r.get("archived")),
        )
        for _, r in df.iterrows()
        if parse_int(r.get("category_id")) is not None and normalize_text(r.get("name")) is not None
    ]
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_category (source_category_id, category_name, archived)
            VALUES %s
            ON CONFLICT (source_category_id) DO UPDATE
            SET category_name = COALESCE(EXCLUDED.category_name, analytics.dim_category.category_name),
                archived = COALESCE(EXCLUDED.archived, analytics.dim_category.archived),
                updated_at = current_timestamp
            """,
            rows,
        )


def build_lookup(cur, table: str, key_col: str, value_col: str) -> dict[Any, Any]:
    cur.execute(f"SELECT {key_col}, {value_col} FROM {table}")
    return {row[1]: row[0] for row in cur.fetchall()}


def record_issue(issue_log: list[IssueRecord], rule_code: str, severity: str, field_name: str | None, invalid_value: Any, description: str, source_event_id: int | None = None) -> None:
    issue_log.append(
        IssueRecord(
            rule_code=rule_code,
            severity=severity,
            field_name=field_name,
            invalid_value=None if invalid_value is None else str(invalid_value),
            description=description,
            source_event_id=source_event_id,
        )
    )


def select_event_row(row: pd.Series) -> dict[str, Any]:
    return row.to_dict()


def main() -> int:
    source = choose_events_source()
    LOG.info("Selected source: %s", source.path)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                execute_sql_file(cur, "001_create_schemas.sql")
                execute_sql_file(cur, "002_create_dimensions.sql")
                execute_sql_file(cur, "005_create_audit_tables.sql")
                conn.commit()

            etl_run_id = start_etl_run(conn)
            conn.commit()
            LOG.info("Started ETL run %s", etl_run_id)
            sources = [
                source,
                SourceSpec("categories.csv", RAW_DIR / "categories.csv"),
                SourceSpec("subcategories.csv", RAW_DIR / "subcategories.csv"),
                SourceSpec("countries.csv", RAW_DIR / "countries.csv"),
                SourceSpec("states.csv", RAW_DIR / "states.csv"),
            ]
            for spec in sources:
                register_source_file(conn, etl_run_id, spec.path, spec.label)
            conn.commit()

            events_df = load_events_dataframe(source.path)
            events_df.columns = [c.strip() for c in events_df.columns]
            events_df["start_time_parsed"] = events_df["start_time"].apply(parse_timestamp) if "start_time" in events_df.columns else None
            valid_starts = [ts.date() for ts in events_df["start_time_parsed"].dropna()] if "start_time_parsed" in events_df.columns else []
            if valid_starts:
                load_dim_date(conn, min(valid_starts), max(valid_starts))
                conn.commit()

            categories_df = pd.read_csv(RAW_DIR / "categories.csv")
            subcategories_df = pd.read_csv(RAW_DIR / "subcategories.csv")
            countries_df = pd.read_csv(RAW_DIR / "countries.csv")
            states_df = pd.read_csv(RAW_DIR / "states.csv")

            upsert_dim_category(conn, categories_df)
            conn.commit()

            with conn.cursor() as cur:
                category_lookup = build_lookup(cur, "analytics.dim_category", "category_key", "source_category_id")

            # skipped detailed upserts for brevity in this stage
            LOG.info("Dimension upsert scaffolding loaded")
            return 0
    except Exception as exc:  # noqa: BLE001
        LOG.exception("ETL failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
