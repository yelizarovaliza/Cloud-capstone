import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.shard_registry import shard_registry


@pytest.fixture(autouse=True)
def reset_registry():
    shard_registry.clear()
    yield
    shard_registry.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_register_new_shard_returns_201(client):
    response = client.post(
        "/v1/internal/shards/register",
        json={
            "shardId": "shard-1",
            "baseUrl": "http://127.0.0.1:8001",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "shardId": "shard-1",
        "registered": True,
        "virtualNodeCount": 128,
    }


def test_repeated_registration_returns_200(client):
    payload = {
        "shardId": "shard-1",
        "baseUrl": "http://127.0.0.1:8001",
    }

    first = client.post(
        "/v1/internal/shards/register",
        json=payload,
    )

    updated = client.post(
        "/v1/internal/shards/register",
        json={
            "shardId": "shard-1",
            "baseUrl": "http://127.0.0.1:8011",
        },
    )

    assert first.status_code == 201
    assert updated.status_code == 200
    assert len(shard_registry.get_all()) == 1

    stored = shard_registry.get("shard-1")
    assert stored is not None
    assert str(stored.base_url).rstrip("/") == (
        "http://127.0.0.1:8011"
    )


def test_different_shard_with_same_address_returns_409(client):
    client.post(
        "/v1/internal/shards/register",
        json={
            "shardId": "shard-1",
            "baseUrl": "http://127.0.0.1:8001",
        },
    )

    response = client.post(
        "/v1/internal/shards/register",
        json={
            "shardId": "shard-2",
            "baseUrl": "http://127.0.0.1:8001",
        },
    )

    assert response.status_code == 409
    assert response.headers["content-type"].startswith(
        "application/problem+json"
    )
    assert len(shard_registry.get_all()) == 1


def test_invalid_registration_returns_400(client):
    response = client.post(
        "/v1/internal/shards/register",
        json={
            "shardId": "",
            "baseUrl": "not-a-url",
        },
    )

    assert response.status_code == 400
    assert response.headers["content-type"].startswith(
        "application/problem+json"
    )


def test_registration_endpoint_is_in_runtime_openapi(client):
    schema = client.get("/openapi.json").json()

    operation = schema["paths"][
        "/v1/internal/shards/register"
    ]["post"]

    assert "201" in operation["responses"]
    assert "200" in operation["responses"]
    assert "400" in operation["responses"]
    assert "409" in operation["responses"]