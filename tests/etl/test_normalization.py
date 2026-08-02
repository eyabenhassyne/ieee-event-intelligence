from datetime import datetime

from etl.common.normalization import blank_to_none, parse_bool, parse_timestamp, build_location_signature


def test_blank_to_none():
    assert blank_to_none("") is None
    assert blank_to_none("   ") is None
    assert blank_to_none("x") == "x"


def test_parse_bool():
    assert parse_bool("true") is True
    assert parse_bool("False") is False
    assert parse_bool("maybe") is None


def test_parse_timestamp():
    assert parse_timestamp("2026-09-17T21:30:00.000Z") is not None
    assert parse_timestamp("not-a-date") is None


def test_location_signature_stable():
    a = build_location_signature(" Lakewood ", "17415 Northwood Ave", "Icon Co Work", "Networking Room", 41.48, -81.81, "physical")
    b = build_location_signature("lakewood", "17415 northwood ave", "icon co work", "networking room", 41.48, -81.81, "physical")
    assert a == b
