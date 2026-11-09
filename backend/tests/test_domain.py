from datetime import UTC, datetime, timedelta

import pytest

from app.domain import DropStatus, as_utc, compute_status

NOW = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    ("opens_at", "remaining", "expected"),
    [
        (NOW + timedelta(seconds=1), 10, DropStatus.UPCOMING),
        (NOW + timedelta(days=3), 0, DropStatus.UPCOMING),
        (NOW, 10, DropStatus.LIVE),
        (NOW - timedelta(days=1), 1, DropStatus.LIVE),
        (NOW - timedelta(days=1), 0, DropStatus.SOLD_OUT),
    ],
)
def test_compute_status(opens_at: datetime, remaining: int, expected: DropStatus) -> None:
    assert compute_status(opens_at, remaining, NOW) == expected


def test_naive_datetimes_are_treated_as_utc() -> None:
    naive = datetime(2026, 11, 9, 12, 0)
    assert as_utc(naive) == NOW
    assert compute_status(naive, 5, NOW) == DropStatus.LIVE


def test_other_timezones_are_converted() -> None:
    paris = datetime.fromisoformat("2026-11-09T13:00:00+01:00")
    assert as_utc(paris) == NOW
