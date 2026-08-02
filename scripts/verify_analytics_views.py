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


def check(label: str, condition: bool) -> bool:
    print(f"{label}: {'PASS' if condition else 'FAIL'}")
    return condition


def scalar(cur, sql: str):
    cur.execute(sql)
    return cur.fetchone()[0]


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
        print(f"ERROR: Unable to connect: {exc}", file=sys.stderr)
        return 2

    failed = False
    try:
        with conn.cursor() as cur:
            expected_views = [
                "v_event_overview",
                "v_monthly_event_summary",
                "v_category_performance",
                "v_organizing_unit_performance",
                "v_country_performance",
                "v_attendance_quality",
                "v_data_quality_summary",
                "v_etl_run_summary",
            ]
            for view in expected_views:
                cur.execute(
                    "SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_schema='analytics' AND table_name=%s)",
                    (view,),
                )
                failed |= not check(f"View exists: {view}", cur.fetchone()[0])

            cur.execute("SELECT COUNT(*) FROM analytics.v_event_overview")
            failed |= not check("Event overview row count", cur.fetchone()[0] == 6197)
            cur.execute("SELECT COUNT(DISTINCT source_event_id) = COUNT(*) FROM analytics.v_event_overview")
            failed |= not check("Event overview uniqueness", cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) FROM analytics.v_monthly_event_summary")
            failed |= not check("Monthly summary has rows", cur.fetchone()[0] > 0)
            cur.execute("SELECT SUM(event_count) = (SELECT COUNT(*) FROM analytics.fact_events) FROM analytics.v_category_performance")
            failed |= not check("Category reconciliation", cur.fetchone()[0])
            cur.execute("SELECT SUM(event_count) = (SELECT COUNT(*) FROM analytics.fact_events) FROM analytics.v_organizing_unit_performance")
            failed |= not check("Organizing-unit reconciliation", cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) > 0 FROM analytics.v_attendance_quality WHERE missing_attendance")
            failed |= not check("Attendance-null handling", cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) > 0 FROM analytics.v_data_quality_summary")
            failed |= not check("DQ summary has issues", cur.fetchone()[0])
            cur.execute("SELECT COUNT(*) > 0 FROM analytics.v_etl_run_summary")
            failed |= not check("ETL summary has runs", cur.fetchone()[0])

        return 0 if not failed else 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
