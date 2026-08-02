from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class IssueRecord:
    rule_code: str
    severity: str
    field_name: str | None
    invalid_value: str | None
    description: str
    source_event_id: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_latitude(value) -> bool:
    return value is None or (-90 <= value <= 90)


def validate_longitude(value) -> bool:
    return value is None or (-180 <= value <= 180)


def validate_end_time(start_time, end_time) -> bool:
    return start_time is None or end_time is None or end_time >= start_time


def validate_nonnegative(value) -> bool:
    return value is None or value >= 0


def validate_event_id(value) -> bool:
    return value is not None
