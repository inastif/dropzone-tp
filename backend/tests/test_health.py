import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def test_liveness(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_checks_the_database(client: TestClient) -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_reports_a_database_failure(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def database_down(*args, **kwargs):
        raise OperationalError("SELECT 1", {}, Exception("connection refused"))

    monkeypatch.setattr(Session, "execute", database_down)
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
