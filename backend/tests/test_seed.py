from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_demo_data_is_inserted_once() -> None:
    settings = Settings(database_url="sqlite:///:memory:", seed_demo_data=True)
    app = create_app(settings)
    with TestClient(app) as client:
        drops = client.get("/drops").json()
        statuses = {drop["status"] for drop in drops}
        assert statuses == {"live", "sold_out", "upcoming"}
    # A restart on the same database does not duplicate the demo data.
    with TestClient(app) as client:
        assert len(client.get("/drops").json()) == len(drops)
