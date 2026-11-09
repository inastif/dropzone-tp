"""Use cases: create and list drops, place an order."""

import logging
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.domain import (
    DropNotFoundError,
    DropNotOpenError,
    DropSoldOutError,
    DropStatus,
    as_utc,
    compute_status,
)
from app.models import Drop, Order
from app.schemas import DropIn, DropOut, OrderOut

logger = logging.getLogger(__name__)


def now_utc() -> datetime:
    return datetime.now(UTC)


def to_out(drop: Drop, now: datetime) -> DropOut:
    return DropOut(
        id=drop.id,
        product=drop.product,
        description=drop.description,
        price_cents=drop.price_cents,
        stock=drop.stock,
        remaining=drop.remaining,
        opens_at=as_utc(drop.opens_at),
        status=compute_status(drop.opens_at, drop.remaining, now),
    )


def create_drop(session: Session, data: DropIn) -> DropOut:
    drop = Drop(
        product=data.product,
        description=data.description,
        price_cents=data.price_cents,
        stock=data.stock,
        remaining=data.stock,
        opens_at=as_utc(data.opens_at),
    )
    session.add(drop)
    session.commit()
    logger.info("drop created", extra={"drop_id": drop.id, "stock": drop.stock})
    return to_out(drop, now_utc())


def list_drops(session: Session, status: DropStatus | None = None) -> list[DropOut]:
    now = now_utc()
    drops = [to_out(drop, now) for drop in session.scalars(select(Drop).order_by(Drop.id))]
    if status is None:
        return drops
    return [drop for drop in drops if drop.status == status]


def get_drop(session: Session, drop_id: int) -> DropOut:
    drop = session.get(Drop, drop_id)
    if drop is None:
        raise DropNotFoundError(drop_id)
    return to_out(drop, now_utc())


def place_order(session: Session, drop_id: int) -> OrderOut:
    """Sell one pair. Never sells more pairs than the stock, even under concurrent requests."""
    drop = session.get(Drop, drop_id)
    if drop is None:
        raise DropNotFoundError(drop_id)
    now = now_utc()
    if compute_status(drop.opens_at, drop.remaining, now) == DropStatus.UPCOMING:
        raise DropNotOpenError(drop_id)

    # Atomic decrement: the database checks "remaining > 0" and updates in one statement,
    # so two buyers can never get the last pair.
    result = session.execute(
        update(Drop)
        .where(Drop.id == drop_id, Drop.remaining > 0)
        .values(remaining=Drop.remaining - 1)
    )
    if result.rowcount == 0:
        session.rollback()
        raise DropSoldOutError(drop_id)

    order = Order(drop_id=drop_id, created_at=now)
    session.add(order)
    session.commit()
    session.refresh(drop)
    logger.info("order placed", extra={"drop_id": drop_id, "remaining": drop.remaining})
    return OrderOut(
        id=order.id, drop_id=drop_id, created_at=order.created_at, drop=to_out(drop, now)
    )
