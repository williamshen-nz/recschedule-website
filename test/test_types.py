from datetime import datetime

import pytest

from recschedule_website.types import CustomDate


@pytest.mark.parametrize(
    "date_str, expected_datetime",
    [
        ("Thursday, March 3, 2022", datetime(2022, 3, 3)),
        ("Monday, February 28, 2022", datetime(2022, 2, 28)),
    ],
)
def test_custom_date(date_str: str, expected_datetime: datetime):
    custom_date = CustomDate(date_str)
    assert custom_date.date_str == date_str
    assert custom_date.datetime == expected_datetime
