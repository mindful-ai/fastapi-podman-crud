import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def reset_store():
    main.products.clear()
    main.next_id = 1
    yield
    main.products.clear()
    main.next_id = 1


@pytest.fixture
def client():
    return TestClient(main.app)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Product CRUD API is running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_product(client):
    response = client.post(
        "/products",
        json={"name": "LED TV", "price": 24999, "quantity": 10},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "LED TV",
        "price": 24999,
        "quantity": 10,
    }


def test_list_products(client):
    client.post(
        "/products",
        json={"name": "LED TV", "price": 24999, "quantity": 10},
    )
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "LED TV"


def test_get_product(client):
    created = client.post(
        "/products",
        json={"name": "Laptop", "price": 55000, "quantity": 5},
    )
    product_id = created.json()["id"]
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_update_product(client):
    created = client.post(
        "/products",
        json={"name": "LED TV", "price": 24999, "quantity": 10},
    )
    product_id = created.json()["id"]
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "LED TV 43 inch",
            "price": 27999,
            "quantity": 8,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "LED TV 43 inch"
    assert response.json()["quantity"] == 8


def test_delete_product(client):
    created = client.post(
        "/products",
        json={"name": "Mouse", "price": 500, "quantity": 20},
    )
    product_id = created.json()["id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert client.get(f"/products/{product_id}").status_code == 404


def test_missing_product_returns_404(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_invalid_product_returns_422(client):
    response = client.post(
        "/products",
        json={"name": "", "price": -10, "quantity": -1},
    )
    assert response.status_code == 422


def test_update_missing_product_returns_404(client):
    response = client.put(
        "/products/999",
        json={"name": "Monitor", "price": 12000, "quantity": 3},
    )
    assert response.status_code == 404


def test_delete_missing_product_returns_404(client):
    response = client.delete("/products/999")
    assert response.status_code == 404
