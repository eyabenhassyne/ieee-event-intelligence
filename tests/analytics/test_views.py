from __future__ import annotations

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def scalar(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchone()[0]


def test_views_exist_and_reconcile():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            views = [
                "v_event_overview",
                "v_monthly_event_summary",
                "v_category_performance",
                "v_organizing_unit_performance",
                "v_country_performance",
                "v_attendance_quality",
                "v_data_quality_summary",
                "v_etl_run_summary",
            ]
            for view in views:
                assert scalar(cur, "SELECT EXISTS (SELECT 1 FROM information_schema.views WHERE table_schema='analytics' AND table_name=%s)", (view,))

            assert scalar(cur, "SELECT COUNT(*) FROM analytics.v_event_overview") == 6197
            assert scalar(cur, "SELECT COUNT(DISTINCT source_event_id) = COUNT(*) FROM analytics.v_event_overview")
            assert scalar(cur, "SELECT SUM(total_events) FROM analytics.v_monthly_event_summary") == 6197
            assert scalar(cur, "SELECT SUM(event_count) FROM analytics.v_category_performance") == 6197
            assert scalar(cur, "SELECT SUM(event_count) FROM analytics.v_organizing_unit_performance") == 6197
            assert scalar(cur, "SELECT COUNT(*) > 0 FROM analytics.v_data_quality_summary")
            assert scalar(cur, "SELECT COUNT(*) > 0 FROM analytics.v_etl_run_summary")
    finally:
        conn.close()


def test_attendance_average_excludes_nulls():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            avg_total = scalar(cur, "SELECT AVG(total_attendance) FILTER (WHERE total_attendance IS NOT NULL) FROM analytics.fact_events")
            assert avg_total is not None
            missing = scalar(cur, "SELECT COUNT(*) FROM analytics.fact_events WHERE total_attendance IS NULL")
            assert missing == 1732
    finally:
        conn.close()
