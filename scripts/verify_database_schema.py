from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"


def load_settings() -> dict[str, str]:
    load_dotenv(dotenv_path=ENV_PATH)
    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    settings: dict[str, str] = {}
    missing: list[str] = []
    for key in required:
        value = os.environ.get(key)
        if value is None or not value.strip():
            missing.append(key)
        else:
            settings[key] = value.strip()
    if missing:
        raise ValueError(f"Missing required environment variables in {ENV_PATH}: {', '.join(missing)}")
    return settings


def fetch_value(cur, sql: str, params: tuple | None = None) -> object | None:
    if params is None:
        cur.execute(sql)
    else:
        cur.execute(sql, params)
    row = cur.fetchone()
    return row[0] if row else None


def check(label: str, condition: bool) -> bool:
    print(f"{label}: {'PASS' if condition else 'FAIL'}")
    return condition


def main() -> int:
    try:
        settings = load_settings()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        conn = psycopg2.connect(
            host=settings["DB_HOST"],
            port=settings["DB_PORT"],
            dbname=settings["DB_NAME"],
            user=settings["DB_USER"],
            password=settings["DB_PASSWORD"],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Unable to connect for verification: {exc}", file=sys.stderr)
        return 2

    failed = False
    try:
        with conn.cursor() as cur:
            def run(label: str, condition: bool) -> None:
                nonlocal failed
                if not check(label, condition):
                    failed = True

            for schema in ["raw", "staging", "analytics", "audit"]:
                run(
                    f"Schema exists: {schema}",
                    bool(fetch_value(cur, "SELECT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = %s)", (schema,))),
                )

            expected_tables = [
                ("analytics", "dim_date"),
                ("analytics", "dim_category"),
                ("analytics", "dim_subcategory"),
                ("analytics", "dim_country"),
                ("analytics", "dim_state"),
                ("analytics", "dim_location"),
                ("analytics", "dim_organizing_unit"),
                ("analytics", "fact_events"),
                ("audit", "etl_run"),
                ("audit", "source_file"),
                ("audit", "data_quality_issue"),
            ]
            for schema, table in expected_tables:
                run(
                    f"Table exists: {schema}.{table}",
                    bool(fetch_value(cur, "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = %s AND table_name = %s)", (schema, table))),
                )

            run("No DimEventStatus table", not bool(fetch_value(cur, "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='analytics' AND table_name='dim_event_status')")))
            run("No FactAttendance table", not bool(fetch_value(cur, "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='analytics' AND table_name='fact_attendance')")))

            run(
                "DimSubcategory references DimCategory",
                bool(
                    fetch_value(
                        cur,
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM information_schema.table_constraints tc
                            WHERE tc.table_schema = 'analytics'
                              AND tc.table_name = 'dim_subcategory'
                              AND tc.constraint_type = 'FOREIGN KEY'
                        )
                        """,
                    )
                ),
            )
            run(
                "DimState references DimCountry",
                bool(
                    fetch_value(
                        cur,
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM information_schema.table_constraints tc
                            WHERE tc.table_schema = 'analytics'
                              AND tc.table_name = 'dim_state'
                              AND tc.constraint_type = 'FOREIGN KEY'
                        )
                        """,
                    )
                ),
            )
            run(
                "FactEvents has unique source_event_id",
                bool(
                    fetch_value(
                        cur,
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM pg_indexes
                            WHERE schemaname = 'analytics'
                              AND tablename = 'fact_events'
                              AND indexdef ILIKE '%UNIQUE%'
                              AND indexdef ILIKE '%source_event_id%'
                        )
                        """,
                    )
                ),
            )
            run("FactEvents populated", fetch_value(cur, "SELECT COUNT(*) FROM analytics.fact_events") > 0)

            unknown_tests = [
                ("analytics.dim_category", "is_unknown", "category_key = 0"),
                ("analytics.dim_subcategory", "is_unknown", "subcategory_key = 0"),
                ("analytics.dim_country", "is_unknown", "country_key = 0"),
                ("analytics.dim_state", "is_unknown", "state_key = 0"),
                ("analytics.dim_location", "is_unknown", "location_key IN (0,1)"),
                ("analytics.dim_organizing_unit", "is_unknown", "organizing_unit_key = 0"),
            ]
            for table, column, predicate in unknown_tests:
                run(
                    f"Unknown member exists: {table}",
                    bool(fetch_value(cur, f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {predicate} AND {column} = TRUE)")),
                )

        print("Database verification result: PASS" if not failed else "Database verification result: FAIL")
        return 0 if not failed else 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
