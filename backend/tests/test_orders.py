from fastapi.testclient import TestClient


def test_an_order_decrements_the_stock(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=10)

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 201
    order = response.json()
    assert order["drop_id"] == drop["id"]
    assert order["drop"]["remaining"] == 9
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 9


def test_the_last_pair_makes_the_drop_sold_out(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=1)

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 201
    assert response.json()["drop"]["remaining"] == 0
    assert response.json()["drop"]["status"] == "sold_out"


def test_a_sold_out_drop_is_refused(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=1)
    client.post(f"/drops/{drop['id']}/orders")

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 409
    # The last pair is never sold twice.
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 0


def test_an_upcoming_drop_is_refused(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=10, opens_at="2100-01-01T00:00:00Z")

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 409
    assert client.get(f"/drops/{drop['id']}").json()["remaining"] == 10


def test_an_unknown_drop_is_not_found(client: TestClient) -> None:
    response = client.post("/drops/999/orders")

    assert response.status_code == 404
