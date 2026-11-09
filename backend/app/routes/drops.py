"""Drops and orders endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import services
from app.dependencies import get_session
from app.domain import DropNotFoundError, DropNotOpenError, DropSoldOutError, DropStatus
from app.schemas import DropIn, DropOut, OrderOut

router = APIRouter(prefix="/drops", tags=["drops"])


@router.get("")
def list_drops(
    drop_status: DropStatus | None = Query(default=None, alias="status"),
    session: Session = Depends(get_session),
) -> list[DropOut]:
    return services.list_drops(session, drop_status)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_drop(
    data: DropIn, response: Response, session: Session = Depends(get_session)
) -> DropOut:
    drop = services.create_drop(session, data)
    response.headers["Location"] = f"/drops/{drop.id}"
    return drop


@router.get("/{drop_id}", responses={404: {"description": "Drop not found"}})
def get_drop(drop_id: int, session: Session = Depends(get_session)) -> DropOut:
    try:
        return services.get_drop(session, drop_id)
    except DropNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post(
    "/{drop_id}/orders",
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Drop not found"},
        409: {"description": "Drop not open yet, or sold out"},
    },
)
def place_order(drop_id: int, session: Session = Depends(get_session)) -> OrderOut:
    try:
        return services.place_order(session, drop_id)
    except DropNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (DropNotOpenError, DropSoldOutError) as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
