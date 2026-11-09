from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """An API backed by a fresh in-memory SQLite database, without demo data."""
    settings = Settings(database_url="sqlite:///:memory:", seed_demo_data=False)
    with TestClient(create_app(settings)) as test_client:
        yield test_client


def iso(moment: datetime) -> str:
    return moment.isoformat().replace("+00:00", "Z")


@pytest.fixture
def make_drop(client: TestClient) -> Callable[..., dict]:
    """Create a drop through the API. By default it opened one hour ago (live)."""

    def _make_drop(**overrides) -> dict:
        payload = {
            "product": "Air Max 1",
            "description": "Test drop",
            "price_cents": 18000,
            "stock": 10,
            "opens_at": iso(datetime.now(UTC) - timedelta(hours=1)),
        } | overrides
        response = client.post("/drops", json=payload)
        assert response.status_code == 201, response.text
        return response.json()

    return _make_drop
