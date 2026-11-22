
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.record_response import Record
from app.services.record_service import (
    RecordAlreadyExistsError,
    record_service,
)
from app.services.table_registry import table_registry


class FakeRecordBackend:
    def __init__(self):
        self.records = {}

    def create(self, table_name, partition_key, value):
        key = (table_name, partition_key)

        if key in self.records:
            raise RecordAlreadyExistsError()

        record = Record(
            tableName=table_name,
            partitionKey=partition_key,
            value=value,
        )
        self.records[key] = record
        return record

    def read(self, table_name, partition_key):
        return self.records.get((table_name, partition_key))

    def exists(self, table_name, partition_key):
        return (table_name, partition_key) in self.records

    def delete(self, table_name, partition_key):
        return self.records.pop((table_name, partition_key), None) is not None


@pytest.fixture
def client():
    table_registry.clear()
    original_backend = record_service.backend
    record_service.backend = FakeRecordBackend()

    with TestClient(app) as test_client:
        test_client.post(
            "/v1/tables",
            json={
                "name": "Users",
                "primaryKey": "partitionKey",
            },
        )
        yield test_client

    record_service.backend = original_backend
    table_registry.clear()


def test_create_record_returns_201(client):
    response = client.post(
        "/v1/tables/Users/records/user-1",
        json={"value": {"email": "user@example.com"}},
    )

    assert response.status_code == 201
    assert response.json() == {
        "tableName": "Users",
        "partitionKey": "user-1",
        "value": {"email": "user@example.com"},
    }


def test_duplicate_create_returns_409_without_overwrite(client):
    client.post(
        "/v1/tables/Users/records/user-1",
        json={"value": {"email": "first@example.com"}},
    )

    response = client.post(
        "/v1/tables/Users/records/user-1",
        json={"value": {"email": "second@example.com"}},
    )

    assert response.status_code == 409

    read_response = client.get("/v1/tables/Users/records/user-1")
    assert read_response.json()["value"]["email"] == "first@example.com"


def test_read_missing_record_returns_404(client):
    response = client.get("/v1/tables/Users/records/missing")

    assert response.status_code == 404


def test_exists_record(client):
    client.post(
        "/v1/tables/Users/records/user-1",
        json={"value": {"email": "user@example.com"}},
    )

    response = client.get(
        "/v1/tables/Users/records/user-1/exists"
    )

    assert response.status_code == 200
    assert response.json()["exists"] is True


def test_exists_missing_record(client):
    response = client.get(
        "/v1/tables/Users/records/missing/exists"
    )

    assert response.status_code == 200
    assert response.json()["exists"] is False


def test_delete_record_returns_204(client):
    client.post(
        "/v1/tables/Users/records/user-1",
        json={"value": {"email": "user@example.com"}},
    )

    response = client.delete("/v1/tables/Users/records/user-1")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_record_returns_404(client):
    response = client.delete("/v1/tables/Users/records/missing")

    assert response.status_code == 404


def test_create_record_for_missing_table_returns_404(client):
    response = client.post(
        "/v1/tables/Unknown/records/user-1",
        json={"value": {"email": "user@example.com"}},
    )

    assert response.status_code == 404


def test_invalid_record_body_returns_400(client):
    response = client.post(
        "/v1/tables/Users/records/user-1",
        json={"partitionKey": "user-1"},
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    ("method", "path", "json"),
    [
        (
            "POST",
            "/v1/tables/Users/records/user-1",
            {"value": {"name": "test"}},
        ),
        (
            "GET",
            "/v1/tables/Users/records/user-1",
            None,
        ),
        (
            "GET",
            "/v1/tables/Users/records/user-1/exists",
            None,
        ),
        (
            "DELETE",
            "/v1/tables/Users/records/user-1",
            None,
        ),
    ],
)
def test_unavailable_shard_returns_503(
    client,
    method,
    path,
    json,
):
    from app.services.record_service import UnavailableRecordBackend

    record_service.backend = UnavailableRecordBackend()

    response = client.request(
        method,
        path,
        json=json,
    )

    assert response.status_code == 503
    assert response.headers["content-type"].startswith(
        "application/problem+json"
    )
    assert response.json()["status"] == 503
