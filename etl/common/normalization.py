from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import pandas as pd


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def blank_to_none(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    return value


def parse_bool(value: Any) -> bool | None:
    value = blank_to_none(value)
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "t", "1", "yes", "y"}:
        return True
    if text in {"false", "f", "0", "no", "n"}:
        return False
    return None


def parse_int(value: Any) -> int | None:
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def parse_decimal(value: Any) -> Decimal | None:
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def parse_timestamp(value: Any):
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        ts = pd.to_datetime(value, errors="coerce", utc=True, format="mixed")
        if pd.isna(ts):
            return None
        return ts.to_pydatetime()
    except Exception:  # noqa: BLE001
        return None


def normalize_list_field(value: Any) -> str | None:
    value = blank_to_none(value)
    if value is None:
        return None
    if isinstance(value, (list, tuple, set)):
        items = [normalize_text(item) for item in value]
    else:
        items = [normalize_text(part) for part in str(value).split(",")]
    cleaned = [item for item in items if item]
    return "|".join(cleaned) if cleaned else None


def build_location_signature(city, address1, building, room_number, latitude, longitude, location_type) -> str | None:
    parts = [
        normalize_text(city),
        normalize_text(address1),
        normalize_text(building),
        normalize_text(room_number),
        normalize_text(latitude),
        normalize_text(longitude),
        normalize_text(location_type),
    ]
    cleaned = [part.lower() for part in parts if part]
    return " | ".join(cleaned) if cleaned else None
