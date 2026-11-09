from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from tests.conftest import iso


def test_create_drop(client: TestClient) -> None:
    response = client.post(
        "/drops",
        json={
            "product": "  Air Max 1  ",
            "price_cents": 18000,
            "stock": 100,
            "opens_at": "2000-01-01T00:00:00Z",
        },
    )
    assert response.status_code == 201
    drop = response.json()
    assert response.headers["Location"] == f"/drops/{drop['id']}"
    assert drop["product"] == "Air Max 1"
    assert drop["description"] == ""
    assert drop["remaining"] == 100
    assert drop["status"] == "live"


def test_a_future_drop_is_upcoming(make_drop) -> None:
    drop = make_drop(opens_at="2100-01-01T00:00:00Z")
    assert drop["status"] == "upcoming"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("product", "   "),
        ("price_cents", 0),
        ("price_cents", -100),
        ("price_cents", 19.99),
        ("stock", 0),
        ("opens_at", "demain"),
        ("opens_at", "2026-11-09T12:00:00"),  # no timezone
    ],
)
def test_invalid_drops_are_rejected(client: TestClient, field: str, value) -> None:
    payload = {
        "product": "Air Max 1",
        "price_cents": 18000,
        "stock": 10,
        "opens_at": "2000-01-01T00:00:00Z",
    } | {field: value}
    response = client.post("/drops", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_missing_fields_and_unknown_fields_are_rejected(client: TestClient) -> None:
    assert client.post("/drops", json={"product": "Air Max 1"}).status_code == 422
    response = client.post(
        "/drops",
        json={
            "product": "Air Max 1",
            "price_cents": 18000,
            "stock": 10,
            "opens_at": "2000-01-01T00:00:00Z",
            "remaining": 0,
        },
    )
    assert response.status_code == 422


def test_get_drop(client: TestClient, make_drop) -> None:
    drop = make_drop()
    response = client.get(f"/drops/{drop['id']}")
    assert response.status_code == 200
    assert response.json() == drop


def test_get_unknown_drop(client: TestClient) -> None:
    response = client.get("/drops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Drop 999 introuvable"


def test_list_drops_sorted_by_id(client: TestClient, make_drop) -> None:
    assert client.get("/drops").json() == []
    first, second = make_drop(product="A"), make_drop(product="B")
    assert [d["id"] for d in client.get("/drops").json()] == [first["id"], second["id"]]


def test_list_drops_filtered_by_status(client: TestClient, make_drop) -> None:
    live = make_drop(product="Live")
    upcoming = make_drop(product="Upcoming", opens_at=iso(datetime.now(UTC) + timedelta(days=1)))
    sold_out = make_drop(product="Sold out", stock=1)
    client.post(f"/drops/{sold_out['id']}/orders")

    def ids(status: str) -> list[int]:
        return [d["id"] for d in client.get("/drops", params={"status": status}).json()]

    assert ids("live") == [live["id"]]
    assert ids("upcoming") == [upcoming["id"]]
    assert ids("sold_out") == [sold_out["id"]]


def test_list_drops_rejects_unknown_status(client: TestClient) -> None:
    assert client.get("/drops", params={"status": "soon"}).status_code == 422
