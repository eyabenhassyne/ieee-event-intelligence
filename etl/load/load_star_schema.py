from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
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
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"
SCHEMA_DIR = BASE_DIR / "database" / "schema"
LOG = configure_logging("etl_load_star_schema")

PREFERRED_EVENTS = PROCESSED_DIR / "events_analytics.csv"
FALLBACK_EVENTS = PROCESSED_DIR / "events_clean.csv"


@dataclass
class SourceFileSpec:
    label: str
    path: Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return max(sum(1 for _ in fh) - 1, 0)


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df


def choose_events_source() -> SourceFileSpec:
    if PREFERRED_EVENTS.exists():
        return SourceFileSpec("events_analytics.csv", PREFERRED_EVENTS)
    return SourceFileSpec("events_clean.csv", FALLBACK_EVENTS)


def run_sql_file(cur, name: str) -> None:
    cur.execute((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def begin_run(cur) -> int:
    cur.execute(
        """
        INSERT INTO audit.etl_run (process_name, status, started_at, message)
        VALUES (%s, %s, current_timestamp, %s)
        RETURNING etl_run_id
        """,
        ("IEEE_EVENT_STAR_SCHEMA_LOAD", "STARTED", "ETL started"),
    )
    return cur.fetchone()[0]


def finish_run(cur, etl_run_id: int, status: str, rows_extracted: int, rows_loaded: int, rows_rejected: int, warning_count: int, error_count: int, message: str) -> None:
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
        (status, rows_extracted, rows_loaded, rows_rejected, warning_count, error_count, message, etl_run_id),
    )


def register_source_files(cur, etl_run_id: int, specs: list[SourceFileSpec]) -> None:
    rows = []
    for spec in specs:
        rows.append(
            (
                etl_run_id,
                spec.label,
                str(spec.path.relative_to(BASE_DIR)),
                sha256_file(spec.path),
                count_csv_rows(spec.path),
                datetime.fromtimestamp(spec.path.stat().st_mtime, tz=timezone.utc),
            )
        )
    execute_values(
        cur,
        """
        INSERT INTO audit.source_file (etl_run_id, file_name, file_path, file_hash, row_count, extracted_at)
        VALUES %s
        """,
        rows,
    )


def upsert_dim_date(cur, dates: set[date]) -> None:
    rows = []
    for current in sorted(dates):
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
    if rows:
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


def upsert_dim_category(cur, df: pd.DataFrame) -> None:
    rows = []
    for _, row in df.iterrows():
        cat_id = parse_int(row.get("category_id"))
        name = normalize_text(row.get("name"))
        if cat_id is None or not name:
            continue
        rows.append((cat_id, name, parse_bool(row.get("archived"))))
    if rows:
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


def upsert_dim_country(cur, df: pd.DataFrame) -> None:
    rows = []
    for _, row in df.iterrows():
        country_id = parse_int(row.get("country_id"))
        name = normalize_text(row.get("name"))
        if country_id is None or not name:
            continue
        rows.append((country_id, name, normalize_text(row.get("abbreviation"))))
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_country (source_country_id, country_name, abbreviation)
            VALUES %s
            ON CONFLICT (source_country_id) DO UPDATE
            SET country_name = COALESCE(EXCLUDED.country_name, analytics.dim_country.country_name),
                abbreviation = COALESCE(EXCLUDED.abbreviation, analytics.dim_country.abbreviation),
                updated_at = current_timestamp
            """,
            rows,
        )


def upsert_dim_state(cur, df: pd.DataFrame, country_by_source_id: dict[int, int], issues: list[IssueRecord]) -> None:
    rows = []
    for _, row in df.iterrows():
        state_id = parse_int(row.get("state_id"))
        name = normalize_text(row.get("name"))
        if state_id is None or not name:
            continue
        parent_country_id = parse_int(row.get("country_id"))
        country_key = country_by_source_id.get(parent_country_id, 0)
        if parent_country_id is None or country_key == 0:
            issues.append(IssueRecord("DQ-EVT-007", "INFO", "country_id", None if parent_country_id is None else str(parent_country_id), "Missing state parent country reference"))
        rows.append((state_id, country_key, name, normalize_text(row.get("abbreviation"))))
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_state (source_state_id, country_key, state_name, abbreviation)
            VALUES %s
            ON CONFLICT (source_state_id) DO UPDATE
            SET country_key = COALESCE(EXCLUDED.country_key, analytics.dim_state.country_key),
                state_name = COALESCE(EXCLUDED.state_name, analytics.dim_state.state_name),
                abbreviation = COALESCE(EXCLUDED.abbreviation, analytics.dim_state.abbreviation),
                updated_at = current_timestamp
            """,
            rows,
        )


def upsert_dim_subcategory(cur, df: pd.DataFrame, category_by_source_id: dict[int, int], issues: list[IssueRecord]) -> None:
    rows = []
    for _, row in df.iterrows():
        sub_id = parse_int(row.get("subcategory_id"))
        name = normalize_text(row.get("name"))
        if sub_id is None or not name:
            continue
        parent_category_id = parse_int(row.get("category_id"))
        category_key = category_by_source_id.get(parent_category_id, 0)
        if parent_category_id is None or category_key == 0:
            issues.append(IssueRecord("DQ-EVT-004", "WARNING", "category_id", None if parent_category_id is None else str(parent_category_id), "Missing category reference for subcategory"))
        rows.append((sub_id, category_key, name, parse_bool(row.get("archived"))))
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_subcategory (source_subcategory_id, category_key, subcategory_name, archived)
            VALUES %s
            ON CONFLICT (source_subcategory_id) DO UPDATE
            SET category_key = COALESCE(EXCLUDED.category_key, analytics.dim_subcategory.category_key),
                subcategory_name = COALESCE(EXCLUDED.subcategory_name, analytics.dim_subcategory.subcategory_name),
                archived = COALESCE(EXCLUDED.archived, analytics.dim_subcategory.archived),
                updated_at = current_timestamp
            """,
            rows,
        )


def upsert_dim_location(cur, events: pd.DataFrame) -> None:
    rows = []
    seen = set()
    for _, row in events.iterrows():
        city = normalize_text(row.get("city"))
        address1 = normalize_text(row.get("address1"))
        building = normalize_text(row.get("building"))
        room_number = normalize_text(row.get("room_number"))
        latitude = row.get("latitude")
        longitude = row.get("longitude")
        location_type = normalize_text(row.get("location_type"))
        signature = build_location_signature(city, address1, building, room_number, latitude, longitude, location_type)
        if not signature or signature in seen:
            continue
        seen.add(signature)
        rows.append(
            (
                city,
                address1,
                building,
                room_number,
                float(latitude) if pd.notna(latitude) else None,
                float(longitude) if pd.notna(longitude) else None,
                location_type,
                signature,
            )
        )
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_location (
                city, address1, building, room_number, latitude, longitude, location_type, location_signature
            ) VALUES %s
            ON CONFLICT (location_signature) DO UPDATE
            SET city = COALESCE(EXCLUDED.city, analytics.dim_location.city),
                address1 = COALESCE(EXCLUDED.address1, analytics.dim_location.address1),
                building = COALESCE(EXCLUDED.building, analytics.dim_location.building),
                room_number = COALESCE(EXCLUDED.room_number, analytics.dim_location.room_number),
                latitude = COALESCE(EXCLUDED.latitude, analytics.dim_location.latitude),
                longitude = COALESCE(EXCLUDED.longitude, analytics.dim_location.longitude),
                location_type = COALESCE(EXCLUDED.location_type, analytics.dim_location.location_type)
            """,
            rows,
        )


def upsert_dim_organizing_unit(cur, events: pd.DataFrame, issues: list[IssueRecord]) -> None:
    rows = []
    seen = set()
    for _, row in events.iterrows():
        spoid = normalize_text(row.get("primary_host_spoid"))
        if not spoid or spoid in seen:
            if not spoid:
                issues.append(IssueRecord("DQ-EVT-008", "WARNING", "primary_host_spoid", None, "Missing organizing-unit SPOID"))
            continue
        seen.add(spoid)
        rows.append(
            (
                spoid,
                normalize_text(row.get("primary_host_name")) or "Unknown",
                normalize_text(row.get("primary_host_type")),
                normalize_list_field(row.get("primary_host_section_spoids")),
                normalize_list_field(row.get("primary_host_region_spoids")),
                normalize_list_field(row.get("primary_host_society_spoids")),
            )
        )
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.dim_organizing_unit (
                primary_host_spoid, primary_host_name, primary_host_type,
                section_spoids, region_spoids, society_spoids
            ) VALUES %s
            ON CONFLICT (primary_host_spoid) DO UPDATE
            SET primary_host_name = COALESCE(EXCLUDED.primary_host_name, analytics.dim_organizing_unit.primary_host_name),
                primary_host_type = COALESCE(EXCLUDED.primary_host_type, analytics.dim_organizing_unit.primary_host_type),
                section_spoids = COALESCE(EXCLUDED.section_spoids, analytics.dim_organizing_unit.section_spoids),
                region_spoids = COALESCE(EXCLUDED.region_spoids, analytics.dim_organizing_unit.region_spoids),
                society_spoids = COALESCE(EXCLUDED.society_spoids, analytics.dim_organizing_unit.society_spoids),
                updated_at = current_timestamp
            """,
            rows,
        )


def lookup_map(cur, table: str, source_col: str, key_col: str) -> dict[int | str, int]:
    cur.execute(f"SELECT {key_col}, {source_col} FROM {table}")
    return {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}


def lookup_dim_location(cur) -> dict[str, int]:
    cur.execute("SELECT location_key, location_signature FROM analytics.dim_location")
    return {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}


def lookup_dim_organizing_unit(cur) -> dict[str, int]:
    cur.execute("SELECT organizing_unit_key, primary_host_spoid FROM analytics.dim_organizing_unit")
    return {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}


def log_issue_records(cur, etl_run_id: int, issues: list[IssueRecord]) -> None:
    rows = [
        (
            etl_run_id,
            issue.source_event_id,
            issue.rule_code,
            issue.severity,
            issue.field_name,
            issue.invalid_value,
            issue.description,
        )
        for issue in issues
    ]
    if rows:
        execute_values(
            cur,
            """
            INSERT INTO audit.data_quality_issue (
                etl_run_id, source_event_id, rule_code, severity, field_name, invalid_value, description
            ) VALUES %s
            """,
            rows,
        )


def load_fact_events(cur, etl_run_id: int, events: pd.DataFrame, category_by_source_id: dict[int, int], subcategory_by_source_id: dict[int, int], country_by_source_id: dict[int, int], state_by_source_id: dict[int, int], location_by_signature: dict[str, int], unit_by_spoid: dict[str, int], issues: list[IssueRecord]) -> tuple[int, int, int]:
    rows = []
    loaded = 0
    rejected = 0
    start_dates: set[date] = set()
    for _, row in events.iterrows():
        source_event_id = parse_int(row.get("id"))
        if not validate_event_id(source_event_id):
            issues.append(IssueRecord("DQ-EVT-001", "ERROR", "id", None, "Missing source event ID"))
            rejected += 1
            continue

        start_time = parse_timestamp(row.get("start_time"))
        if start_time is None or start_time.year < 1900 or start_time.year > 2100:
            issues.append(IssueRecord("DQ-EVT-002", "ERROR", "start_time", str(row.get("start_time")), "Invalid start date", source_event_id))
            rejected += 1
            continue
        start_dates.add(start_time.date())

        end_time = parse_timestamp(row.get("end_time"))
        if end_time is not None and not validate_end_time(start_time, end_time):
            issues.append(IssueRecord("DQ-EVT-003", "ERROR", "end_time", str(row.get("end_time")), "End time before start time", source_event_id))
            rejected += 1
            continue

        ieee_attending = parse_int(row.get("ieee_attending"))
        guests_attending = parse_int(row.get("guests_attending"))
        max_registrations = parse_int(row.get("max_registrations"))
        speaker_count = parse_int(row.get("speaker_count"))
        for code, field, value, sev in [
            ("DQ-EVT-011", "ieee_attending", ieee_attending, "ERROR"),
            ("DQ-EVT-012", "guests_attending", guests_attending, "ERROR"),
            ("DQ-EVT-013", "max_registrations", max_registrations, "ERROR"),
        ]:
            if value is not None and not validate_nonnegative(value):
                issues.append(IssueRecord(code, sev, field, str(value), f"Negative {field.replace('_', ' ')}", source_event_id))
                rejected += 1
                continue

        if rejected > 0 and any(i.source_event_id == source_event_id and i.severity == "ERROR" for i in issues):
            continue

        category_id = parse_int(row.get("category_id"))
        subcategory_id = parse_int(row.get("subcategory_id"))
        country_id = parse_int(row.get("country_id"))
        state_id = parse_int(row.get("state_id"))
        category_key = category_by_source_id.get(category_id, 0)
        subcategory_key = subcategory_by_source_id.get(subcategory_id, 0)
        country_key = country_by_source_id.get(country_id, 0)
        state_key = state_by_source_id.get(state_id, 0)

        if category_key == 0:
            issues.append(IssueRecord("DQ-EVT-004", "WARNING", "category_id", None if category_id is None else str(category_id), "Missing category reference", source_event_id))
        if subcategory_id is None:
            issues.append(IssueRecord("DQ-EVT-005", "INFO", "subcategory_id", None, "Missing subcategory reference", source_event_id))
        if country_key == 0 and not parse_bool(row.get("virtual")):
            issues.append(IssueRecord("DQ-EVT-006", "WARNING", "country_id", None if country_id is None else str(country_id), "Missing country for physical event", source_event_id))
        if state_id is None:
            issues.append(IssueRecord("DQ-EVT-007", "INFO", "state_id", None, "Missing state reference", source_event_id))

        city = normalize_text(row.get("city"))
        address1 = normalize_text(row.get("address1"))
        building = normalize_text(row.get("building"))
        room_number = normalize_text(row.get("room_number"))
        latitude = float(row["latitude"]) if pd.notna(row.get("latitude")) else None
        longitude = float(row["longitude"]) if pd.notna(row.get("longitude")) else None
        location_type = normalize_text(row.get("location_type"))
        location_signature = build_location_signature(city, address1, building, room_number, latitude, longitude, location_type)
        virtual_flag = parse_bool(row.get("virtual")) or False
        if latitude is not None and not validate_latitude(latitude):
            issues.append(IssueRecord("DQ-EVT-009", "WARNING", "latitude", str(latitude), "Invalid latitude", source_event_id))
        if longitude is not None and not validate_longitude(longitude):
            issues.append(IssueRecord("DQ-EVT-010", "WARNING", "longitude", str(longitude), "Invalid longitude", source_event_id))

        if virtual_flag:
            location_key = 1
        elif location_signature and location_signature in location_by_signature:
            location_key = location_by_signature[location_signature]
        elif location_signature:
            location_key = 0
            issues.append(IssueRecord("DQ-EVT-016", "WARNING", "location_signature", location_signature, "Unknown location for physical event", source_event_id))
        else:
            location_key = 0
            if any([city, address1, building, room_number, latitude, longitude, location_type]):
                issues.append(IssueRecord("DQ-EVT-016", "WARNING", "location_signature", None, "Unknown location for physical event", source_event_id))

        host_spoid = normalize_text(row.get("primary_host_spoid"))
        organizing_unit_key = unit_by_spoid.get(host_spoid, 0)
        if host_spoid is None:
            issues.append(IssueRecord("DQ-EVT-008", "WARNING", "primary_host_spoid", None, "Missing organizing-unit SPOID", source_event_id))

        attendance_available = ieee_attending is not None or guests_attending is not None
        if not attendance_available:
            issues.append(IssueRecord("DQ-EVT-014", "INFO", "attendance", None, "Missing attendance", source_event_id))
        if ieee_attending is not None and guests_attending is not None:
            total_attendance = ieee_attending + guests_attending
        elif ieee_attending is not None:
            total_attendance = ieee_attending
        elif guests_attending is not None:
            total_attendance = guests_attending
        else:
            total_attendance = None

        if max_registrations is not None and total_attendance is not None and total_attendance > max_registrations:
            issues.append(IssueRecord("DQ-EVT-015", "WARNING", "total_attendance", str(total_attendance), "Attendance exceeds capacity", source_event_id))

        duration_hours = None
        if end_time is not None:
            duration_hours = round((end_time - start_time).total_seconds() / 3600.0, 2)

        has_subcategory = subcategory_key != 0
        registration_available = any(
            pd.notna(row.get(col))
            for col in ["registration_start_time", "registration_end_time", "registration_url"]
            if col in row.index
        )
        has_location = location_key != 0
        has_capacity = max_registrations is not None
        published = parse_bool(row.get("publish")) or False

        rows.append(
            (
                source_event_id,
                int(start_time.strftime("%Y%m%d")),
                category_key,
                subcategory_key,
                country_key,
                state_key,
                location_key,
                organizing_unit_key,
                normalize_text(row.get("title")) or "Unknown",
                normalize_text(row.get("description")),
                start_time,
                end_time,
                normalize_text(row.get("time_zone")),
                normalize_text(row.get("link")),
                duration_hours,
                ieee_attending,
                guests_attending,
                total_attendance,
                max_registrations,
                speaker_count,
                1,
                virtual_flag,
                parse_bool(row.get("cancelled")) or False,
                published,
                parse_bool(row.get("is_valid_date")),
                attendance_available,
                registration_available,
                has_capacity,
                has_location,
                has_subcategory,
                parse_timestamp(row.get("created_at")),
                parse_timestamp(row.get("updated_at")),
                etl_run_id,
            )
        )
        loaded += 1

    if rows:
        execute_values(
            cur,
            """
            INSERT INTO analytics.fact_events (
                source_event_id, date_key, category_key, subcategory_key, country_key, state_key,
                location_key, organizing_unit_key, title, description, start_time, end_time, time_zone,
                source_link, duration_hours, ieee_attending, guests_attending, total_attendance,
                max_registrations, speaker_count, event_count, virtual, cancelled, published,
                is_valid_date, attendance_available, registration_available, has_capacity, has_location,
                has_subcategory, source_created_at, source_updated_at, etl_run_id
            ) VALUES %s
            ON CONFLICT (source_event_id) DO UPDATE SET
                date_key = EXCLUDED.date_key,
                category_key = EXCLUDED.category_key,
                subcategory_key = EXCLUDED.subcategory_key,
                country_key = EXCLUDED.country_key,
                state_key = EXCLUDED.state_key,
                location_key = EXCLUDED.location_key,
                organizing_unit_key = EXCLUDED.organizing_unit_key,
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                start_time = EXCLUDED.start_time,
                end_time = EXCLUDED.end_time,
                time_zone = EXCLUDED.time_zone,
                source_link = EXCLUDED.source_link,
                duration_hours = EXCLUDED.duration_hours,
                ieee_attending = EXCLUDED.ieee_attending,
                guests_attending = EXCLUDED.guests_attending,
                total_attendance = EXCLUDED.total_attendance,
                max_registrations = EXCLUDED.max_registrations,
                speaker_count = EXCLUDED.speaker_count,
                event_count = EXCLUDED.event_count,
                virtual = EXCLUDED.virtual,
                cancelled = EXCLUDED.cancelled,
                published = EXCLUDED.published,
                is_valid_date = EXCLUDED.is_valid_date,
                attendance_available = EXCLUDED.attendance_available,
                registration_available = EXCLUDED.registration_available,
                has_capacity = EXCLUDED.has_capacity,
                has_location = EXCLUDED.has_location,
                has_subcategory = EXCLUDED.has_subcategory,
                source_created_at = EXCLUDED.source_created_at,
                source_updated_at = EXCLUDED.source_updated_at,
                etl_run_id = EXCLUDED.etl_run_id,
                loaded_at = current_timestamp
            """,
            rows,
        )

    return loaded, rejected, len(start_dates)


def main() -> int:
    source = choose_events_source()
    LOG.info("Selected source: %s", source.path)
    events_df = read_csv(source.path)
    categories_df = read_csv(RAW_DIR / "categories.csv")
    subcategories_df = read_csv(RAW_DIR / "subcategories.csv")
    countries_df = read_csv(RAW_DIR / "countries.csv")
    states_df = read_csv(RAW_DIR / "states.csv")

    issue_records: list[IssueRecord] = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                run_sql_file(cur, "001_create_schemas.sql")
                run_sql_file(cur, "002_create_dimensions.sql")
                run_sql_file(cur, "005_create_audit_tables.sql")
                conn.commit()

            with conn.cursor() as cur:
                etl_run_id = begin_run(cur)
                conn.commit()

                register_source_files(
                    cur,
                    etl_run_id,
                    [
                        source,
                        SourceFileSpec("categories.csv", RAW_DIR / "categories.csv"),
                        SourceFileSpec("subcategories.csv", RAW_DIR / "subcategories.csv"),
                        SourceFileSpec("countries.csv", RAW_DIR / "countries.csv"),
                        SourceFileSpec("states.csv", RAW_DIR / "states.csv"),
                    ],
                )
                conn.commit()

                dates = set()
                for value in events_df.get("start_time", pd.Series(dtype=object)):
                    ts = parse_timestamp(value)
                    if ts is not None and 1900 <= ts.year <= 2100:
                        dates.add(ts.date())
                upsert_dim_date(cur, dates)
                upsert_dim_category(cur, categories_df)
                conn.commit()

                cur.execute("SELECT category_key, source_category_id FROM analytics.dim_category")
                category_by_source_id = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}

                upsert_dim_subcategory(cur, subcategories_df, category_by_source_id, issue_records)
                upsert_dim_country(cur, countries_df)
                conn.commit()

                cur.execute("SELECT country_key, source_country_id FROM analytics.dim_country")
                country_by_source_id = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}

                upsert_dim_state(cur, states_df, country_by_source_id, issue_records)
                upsert_dim_location(cur, events_df)
                upsert_dim_organizing_unit(cur, events_df, issue_records)
                conn.commit()

                cur.execute("SELECT subcategory_key, source_subcategory_id FROM analytics.dim_subcategory")
                subcategory_by_source_id = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}
                cur.execute("SELECT location_key, location_signature FROM analytics.dim_location")
                location_by_signature = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}
                cur.execute("SELECT organizing_unit_key, primary_host_spoid FROM analytics.dim_organizing_unit")
                unit_by_spoid = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}
                cur.execute("SELECT state_key, source_state_id FROM analytics.dim_state")
                state_by_source_id = {row[1]: row[0] for row in cur.fetchall() if row[1] is not None}

                loaded, rejected, date_count = load_fact_events(
                    cur,
                    etl_run_id,
                    events_df,
                    category_by_source_id,
                    subcategory_by_source_id,
                    country_by_source_id,
                    state_by_source_id,
                    location_by_signature,
                    unit_by_spoid,
                    issue_records,
                )
                log_issue_records(cur, etl_run_id, issue_records)
                rows_extracted = len(events_df)
                rows_loaded = loaded
                rows_rejected = rejected
                warning_count = sum(1 for issue in issue_records if issue.severity == "WARNING")
                error_count = sum(1 for issue in issue_records if issue.severity == "ERROR")
                status = "PARTIAL" if rows_rejected else "SUCCEEDED"
                finish_run(
                    cur,
                    etl_run_id,
                    status,
                    rows_extracted,
                    rows_loaded,
                    rows_rejected,
                    warning_count,
                    error_count,
                    f"Selected source {source.label}; dates loaded: {date_count}",
                )
                conn.commit()

        print("ETL complete")
        print(f"Selected source: {source.path}")
        print(f"Rows extracted: {rows_extracted}")
        print(f"Rows loaded: {rows_loaded}")
        print(f"Rows rejected: {rows_rejected}")
        print(f"Warnings: {warning_count}")
        print(f"Errors: {error_count}")
        print(f"ETL run ID: {etl_run_id}")
        return 0
    except Exception as exc:  # noqa: BLE001
        LOG.exception("ETL failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
