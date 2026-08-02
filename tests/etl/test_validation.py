from datetime import datetime

from etl.common.validation import validate_latitude, validate_longitude, validate_end_time, validate_nonnegative


def test_coordinate_ranges():
    assert validate_latitude(41.0)
    assert not validate_latitude(91.0)
    assert validate_longitude(-81.0)
    assert not validate_longitude(181.0)


def test_end_time_validation():
    start = datetime(2026, 9, 17, 21, 30)
    end = datetime(2026, 9, 17, 22, 30)
    assert validate_end_time(start, end)
    assert not validate_end_time(end, start)


def test_nonnegative():
    assert validate_nonnegative(0)
    assert not validate_nonnegative(-1)
