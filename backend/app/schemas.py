"""Request and response bodies (validated by Pydantic)."""

from datetime import datetime
from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints

from app.domain import DropStatus

ProductName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]


class DropIn(BaseModel):
    """What a client sends to create a drop: no id, no remaining, no status."""

    model_config = ConfigDict(extra="forbid")

    product: ProductName
    description: str = Field(default="", max_length=2000)
    price_cents: int = Field(gt=0, description="Price in cents (18000 = 180 €)")
    stock: int = Field(gt=0, le=100_000)
    opens_at: AwareDatetime = Field(description="Opening time, RFC 3339")


class DropOut(BaseModel):
    id: int
    product: str
    description: str
    price_cents: int
    stock: int
    remaining: int
    opens_at: datetime
    status: DropStatus


class OrderOut(BaseModel):
    id: int
    drop_id: int
    created_at: datetime
    drop: DropOut


class HealthOut(BaseModel):
    status: str
    version: str
