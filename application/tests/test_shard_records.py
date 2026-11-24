import pytest
from fastapi.testclient import TestClient

from app.shard.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("SHARD_ID", "shard-1")
    monkeypatch.setenv(
        "SHARD_BASE_URL",
        "http://127.0.0.1:8001",
    )
    monkeypatch.setenv(
        "COORDINATOR_URL",
        "http://127.0.0.1:8000",
    )
    monkeypatch.setenv(
        "SHARD_DB_PATH",
        str(tmp_path / "shard.sqlite3"),
    )

    async def fake_register(
        coordinator_url: str,
        shard_id: str,
        base_url: str,
    ) -> dict:
        return {
            "shardId": shard_id,
            "registered": True,
            "virtualNodeCount": 128,
        }

    monkeypatch.setattr(
        "app.shard.main.register_with_coordinator",
        fake_register,
    )

    with TestClient(app) as test_client:
        yield test_client


def test_internal_crud_flow(client):
    url = "/v1/internal/tables/Users/records/user-1"

    # CREATE
    response = client.post(
        url,
        json={"value": {"name": "Alice"}},
    )

    assert response.status_code == 201
    assert response.json() == {
        "tableName": "Users",
        "partitionKey": "user-1",
        "value": {"name": "Alice"},
    }

    # READ
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["value"] == {"name": "Alice"}

    # EXISTS
    response = client.get(f"{url}/exists")

    assert response.status_code == 200
    assert response.json() == {
        "tableName": "Users",
        "partitionKey": "user-1",
        "exists": True,
    }

    # DELETE
    response = client.delete(url)

    assert response.status_code == 204

    # EXISTS after DELETE
    response = client.get(f"{url}/exists")

    assert response.status_code == 200
    assert response.json()["exists"] is False


def test_create_duplicate_returns_409(client):
    url = "/v1/internal/tables/Users/records/user-1"

    first = client.post(
        url,
        json={"value": {"name": "Alice"}},
    )
    second = client.post(
        url,
        json={"value": {"name": "Bob"}},
    )

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.headers["content-type"].startswith("application/problem+json")

    # The original value must not be overwritten.
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["value"] == {"name": "Alice"}


def test_read_and_delete_missing_record_return_404(client):
    url = "/v1/internal/tables/Users/records/missing"

    read_response = client.get(url)
    delete_response = client.delete(url)

    assert read_response.status_code == 404
    assert delete_response.status_code == 404


def test_same_partition_key_is_isolated_by_table(client):
    users_url = "/v1/internal/tables/Users/records/item-1"
    orders_url = "/v1/internal/tables/Orders/records/item-1"

    client.post(users_url, json={"value": {"type": "user"}})
    client.post(orders_url, json={"value": {"type": "order"}})

    users_record = client.get(users_url).json()
    orders_record = client.get(orders_url).json()

    assert users_record["value"] == {"type": "user"}
    assert orders_record["value"] == {"type": "order"}
