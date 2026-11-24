import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.table_registry import table_registry


@pytest.fixture
def client():
    table_registry.clear()

    with TestClient(app) as test_client:
        yield test_client

    table_registry.clear()


def valid_table() -> dict:
    return {
        "name": "Users",
        "primaryKey": "partitionKey",
        "fields": {
            "email": "string",
            "age": "integer",
        },
        "description": "User records",
    }


def test_register_table_returns_201(client: TestClient):
    response = client.post("/v1/tables", json=valid_table())

    assert response.status_code == 201
    assert response.json() == valid_table()


def test_get_registered_table_returns_200(client: TestClient):
    table = valid_table()
    client.post("/v1/tables", json=table)

    response = client.get("/v1/tables/Users")

    assert response.status_code == 200
    assert response.json() == table


def test_register_duplicate_table_returns_409(client: TestClient):
    table = valid_table()

    first_response = client.post("/v1/tables", json=table)

    changed_table = {
        **table,
        "description": "Changed description",
    }
    second_response = client.post("/v1/tables", json=changed_table)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.headers["content-type"].startswith(
        "application/problem+json"
    )

    stored_table = client.get("/v1/tables/Users")

    assert stored_table.json() == table


def test_register_table_with_invalid_primary_key_returns_400(
    client: TestClient,
):
    table = valid_table()
    table["primaryKey"] = "sortKey"

    response = client.post("/v1/tables", json=table)

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")


def test_register_table_with_invalid_name_returns_400(
    client: TestClient,
):
    table = valid_table()
    table["name"] = "123-invalid"

    response = client.post("/v1/tables", json=table)

    assert response.status_code == 400


def test_register_table_with_unknown_field_returns_400(
    client: TestClient,
):
    table = valid_table()
    table["unexpected"] = "value"

    response = client.post("/v1/tables", json=table)

    assert response.status_code == 400


def test_get_missing_table_returns_404(client: TestClient):
    response = client.get("/v1/tables/Unknown")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
