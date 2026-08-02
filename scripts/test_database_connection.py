from __future__ import annotations

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
        value = __import__("os").environ.get(key)
        if value is None or not value.strip():
            missing.append(key)
        else:
            settings[key] = value.strip()

    if missing:
        raise ValueError(f"Missing required environment variables in {ENV_PATH}: {', '.join(missing)}")

    return settings


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
    except psycopg2.OperationalError as exc:
        message = str(exc).strip()
        lowered = message.lower()
        if "password authentication failed" in lowered or "authentication failed" in lowered:
            print("ERROR: PostgreSQL authentication failed. Please verify the password in .env.", file=sys.stderr)
        elif "could not connect to server" in lowered:
            print("ERROR: Could not connect to PostgreSQL on localhost:5432. Check the service and port.", file=sys.stderr)
        else:
            print(f"ERROR: Database connection failed: {message}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Unexpected database connection failure: {exc}", file=sys.stderr)
        return 2

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                cur.execute("SELECT current_database(), current_user;")
                current_database, current_user = cur.fetchone()

        print("SUCCESS: PostgreSQL connection verified.")
        print(f"PostgreSQL version: {version}")
        print(f"Connected database: {current_database}")
        print(f"Connected user: {current_user}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Connection test failed after authentication: {exc}", file=sys.stderr)
        return 3
    finally:
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    raise SystemExit(main())
