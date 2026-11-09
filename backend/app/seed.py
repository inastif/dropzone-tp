"""Demo data, inserted at startup when the database is empty."""

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Drop

logger = logging.getLogger(__name__)


def demo_drops(now: datetime) -> list[Drop]:
    return [
        Drop(
            product="Air Max 1 « Laval »",
            description="Édition locale, semelle gomme, 100 paires numérotées.",
            price_cents=18000,
            stock=100,
            remaining=100,
            opens_at=now - timedelta(days=1),
        ),
        Drop(
            product="Jordan 4 « Mayenne »",
            description="Cuir nubuck bleu nuit, lacets de rechange.",
            price_cents=21000,
            stock=50,
            remaining=3,
            opens_at=now - timedelta(hours=2),
        ),
        Drop(
            product="Dunk Low « Saint-Berthevin »",
            description="Toutes les paires sont parties en quatre minutes.",
            price_cents=12000,
            stock=30,
            remaining=0,
            opens_at=now - timedelta(days=7),
        ),
        Drop(
            product="New Balance 550 « IIA »",
            description="Ouverture prochaine : préparez-vous.",
            price_cents=14000,
            stock=80,
            remaining=80,
            opens_at=now + timedelta(days=2, hours=3),
        ),
    ]


def seed_if_empty(session: Session) -> None:
    if session.scalar(select(func.count()).select_from(Drop)):
        return
    drops = demo_drops(datetime.now(UTC).replace(microsecond=0))
    session.add_all(drops)
    session.commit()
    logger.info("demo data inserted", extra={"drops": len(drops)})
