from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
SCHEMA_DIR = BASE_DIR / "database" / "schema"


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


def sql_files_in_order() -> list[Path]:
    files = [p for p in SCHEMA_DIR.glob("*.sql") if p.is_file()]
    pattern = re.compile(r"^(\d+)_")
    return sorted(files, key=lambda p: (int(pattern.match(p.name).group(1)) if pattern.match(p.name) else 10**9, p.name))


def main() -> int:
    try:
        settings = load_settings()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    sql_files = sql_files_in_order()
    if not sql_files:
        print(f"ERROR: No SQL files found in {SCHEMA_DIR}", file=sys.stderr)
        return 1

    print("SQL execution order:")
    for path in sql_files:
        print(f"- {path.name}")

    try:
        conn = psycopg2.connect(
            host=settings["DB_HOST"],
            port=settings["DB_PORT"],
            dbname=settings["DB_NAME"],
            user=settings["DB_USER"],
            password=settings["DB_PASSWORD"],
        )
    except psycopg2.OperationalError as exc:
        print(f"ERROR: Unable to connect to PostgreSQL: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Unexpected connection error: {exc}", file=sys.stderr)
        return 2

    try:
        with conn:
            with conn.cursor() as cur:
                for path in sql_files:
                    print(f"Executing {path.name}")
                    sql = path.read_text(encoding="utf-8")
                    cur.execute(sql)
        print("SUCCESS: Database schema applied.")
        return 0
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        print(f"ERROR: Schema application failed; transaction rolled back: {exc}", file=sys.stderr)
        return 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
