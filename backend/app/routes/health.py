"""Health checks: liveness (the process answers) and readiness (the database answers)."""

import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import __version__
from app.dependencies import get_session
from app.schemas import HealthOut

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health")
def liveness() -> HealthOut:
    return HealthOut(status="ok", version=__version__)


@router.get("/health/ready", responses={503: {"model": HealthOut}})
def readiness(response: Response, session: Session = Depends(get_session)) -> HealthOut:
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("database not reachable")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthOut(status="unavailable", version=__version__)
    return HealthOut(status="ok", version=__version__)
