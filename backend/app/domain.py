"""Business rules of a drop, independent from the web framework and the database."""

from datetime import UTC, datetime
from enum import StrEnum


class DropStatus(StrEnum):
    UPCOMING = "upcoming"
    LIVE = "live"
    SOLD_OUT = "sold_out"


def as_utc(moment: datetime) -> datetime:
    """Return an aware UTC datetime (SQLite gives back naive datetimes)."""
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def compute_status(opens_at: datetime, remaining: int, now: datetime) -> DropStatus:
    """The status is computed on every read, never stored."""
    if as_utc(now) < as_utc(opens_at):
        return DropStatus.UPCOMING
    if remaining <= 0:
        return DropStatus.SOLD_OUT
    return DropStatus.LIVE


class DropNotFoundError(Exception):
    def __init__(self, drop_id: int) -> None:
        super().__init__(f"Drop {drop_id} introuvable")
        self.drop_id = drop_id


class DropNotOpenError(Exception):
    def __init__(self, drop_id: int) -> None:
        super().__init__(f"Le drop {drop_id} n'est pas encore ouvert")


class DropSoldOutError(Exception):
    def __init__(self, drop_id: int) -> None:
        super().__init__(f"Le drop {drop_id} est épuisé")
