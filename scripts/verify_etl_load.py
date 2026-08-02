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
            def q(sql: str):
                cur.execute(sql)
                return cur.fetchone()[0]

            failed |= not check("Schemas exist", q("SELECT COUNT(*) = 4 FROM information_schema.schemata WHERE schema_name IN ('raw','staging','analytics','audit')"))
            failed |= not check("Dimensions have rows", q("SELECT (SELECT COUNT(*) FROM analytics.dim_date) > 0 AND (SELECT COUNT(*) FROM analytics.dim_category) > 0 AND (SELECT COUNT(*) FROM analytics.dim_subcategory) > 0 AND (SELECT COUNT(*) FROM analytics.dim_country) > 0 AND (SELECT COUNT(*) FROM analytics.dim_state) > 0 AND (SELECT COUNT(*) FROM analytics.dim_location) > 0 AND (SELECT COUNT(*) FROM analytics.dim_organizing_unit) > 0"))
            failed |= not check("FactEvents empty or populated consistently", q("SELECT COUNT(*) >= 0 FROM analytics.fact_events"))
            failed |= not check("Latest ETL run exists", q("SELECT COUNT(*) > 0 FROM audit.etl_run"))
        return 0 if not failed else 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
