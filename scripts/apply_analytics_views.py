from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
VIEWS_DIR = BASE_DIR / "database" / "views"


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


def ordered_sql_files() -> list[Path]:
    pattern = re.compile(r"^(\d+)_")
    return sorted(
        [p for p in VIEWS_DIR.glob("*.sql") if p.is_file()],
        key=lambda p: (int(pattern.match(p.name).group(1)) if pattern.match(p.name) else 10**9, p.name),
    )


def main() -> int:
    try:
        settings = load_settings()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    files = ordered_sql_files()
    print("SQL execution order:")
    for path in files:
        print(f"- {path.name}")

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

    try:
        with conn:
            with conn.cursor() as cur:
                for path in files:
                    print(f"Executing {path.name}")
                    cur.execute(path.read_text(encoding="utf-8"))
        print("SUCCESS: Analytics views applied.")
        return 0
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        print(f"ERROR: Analytics view application failed; rolled back: {exc}", file=sys.stderr)
        return 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
