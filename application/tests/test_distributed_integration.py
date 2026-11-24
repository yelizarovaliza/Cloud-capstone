import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app as coordinator_app
from app.shard.main import app as shard_app
from app.services.record_service import record_service
from app.services.shard_client import ShardHttpClient
from app.services.shard_registry import shard_registry
from app.services.shard_router import ShardRouter
from app.services.routing_record_backend import RoutingRecordBackend
from app.services.table_registry import table_registry


@pytest.fixture
def distributed_environment(tmp_path, monkeypatch):
    live_shard_id = "shard-1"
    unavailable_shard_id = "shard-2"

    live_base_url = "http://shard-1:8001"
    unavailable_base_url = "http://shard-2:8002"

    shard_registry.clear()
    table_registry.clear()

    original_backend = record_service.backend

    try:
        with TestClient(coordinator_app) as coordinator_client:

            async def register_with_test_coordinator(
                coordinator_url: str,
                shard_id: str,
                base_url: str,
            ) -> dict:
                response = coordinator_client.post(
                    "/v1/internal/shards/register",
                    json={
                        "shardId": shard_id,
                        "baseUrl": base_url,
                    },
                )

                response.raise_for_status()
                return response.json()

            monkeypatch.setattr(
                "app.shard.main.register_with_coordinator",
                register_with_test_coordinator,
            )

            monkeypatch.setenv("SHARD_ID", live_shard_id)
            monkeypatch.setenv(
                "SHARD_BASE_URL",
                live_base_url,
            )
            monkeypatch.setenv(
                "COORDINATOR_URL",
                "http://coordinator:8000",
            )
            monkeypatch.setenv(
                "SHARD_DB_PATH",
                str(tmp_path / "shard.sqlite3"),
            )

            with TestClient(shard_app) as shard_client:
                # Register a second Shard that will be unavailable.
                registration_response = coordinator_client.post(
                    "/v1/internal/shards/register",
                    json={
                        "shardId": unavailable_shard_id,
                        "baseUrl": unavailable_base_url,
                    },
                )

                assert registration_response.status_code == 201

                calls = []

                def dispatch_shard_request(
                    request: httpx.Request,
                ) -> httpx.Response:
                    base_url = str(request.url.copy_with(path="", query=None)).rstrip(
                        "/"
                    )

                    calls.append(base_url)

                    if base_url == unavailable_base_url:
                        raise httpx.ConnectError(
                            "Simulated Shard unavailability",
                            request=request,
                        )

                    if base_url != live_base_url:
                        raise httpx.ConnectError(
                            "Unknown Shard",
                            request=request,
                        )

                    response = shard_client.request(
                        request.method,
                        request.url.path,
                        content=request.content,
                        headers={
                            "content-type": request.headers.get(
                                "content-type",
                                "application/json",
                            )
                        },
                    )

                    return httpx.Response(
                        status_code=response.status_code,
                        headers=response.headers,
                        content=response.content,
                        request=request,
                    )

                transport = httpx.MockTransport(dispatch_shard_request)

                router = ShardRouter(shard_registry)

                record_service.backend = RoutingRecordBackend(
                    router=router,
                    client=ShardHttpClient(
                        transport=transport,
                    ),
                )

                yield {
                    "coordinator": coordinator_client,
                    "router": router,
                    "calls": calls,
                    "live_base_url": live_base_url,
                    "unavailable_base_url": unavailable_base_url,
                }

    finally:
        record_service.backend = original_backend
        shard_registry.clear()
        table_registry.clear()


def register_users_table(client):
    response = client.post(
        "/v1/tables",
        json={
            "name": "Users",
            "primaryKey": "partitionKey",
        },
    )

    assert response.status_code == 201


def find_key_for_shard(router, shard_id):
    for index in range(10000):
        partition_key = f"record-{index}"

        registration = router.resolve(
            "Users",
            partition_key,
        )

        if registration.shard_id == shard_id:
            return partition_key

    raise AssertionError(f"Could not find a key assigned to {shard_id}")


def test_registration_routing_and_read_after_write(
    distributed_environment,
):
    client = distributed_environment["coordinator"]
    router = distributed_environment["router"]
    calls = distributed_environment["calls"]
    live_base_url = distributed_environment["live_base_url"]

    # The live Shard must have registered during startup.
    assert shard_registry.get("shard-1") is not None
    assert shard_registry.get("shard-2") is not None

    register_users_table(client)

    # Find a key assigned to the available Shard.
    partition_key = find_key_for_shard(
        router,
        "shard-1",
    )

    record_url = f"/v1/tables/Users/records/{partition_key}"

    # CREATE
    create_response = client.post(
        record_url,
        json={
            "value": {
                "name": "Alice",
            }
        },
    )

    assert create_response.status_code == 201

    # READ immediately after CREATE.
    read_response = client.get(record_url)

    assert read_response.status_code == 200
    assert read_response.json()["value"] == {
        "name": "Alice",
    }

    # EXISTS
    exists_response = client.get(f"{record_url}/exists")

    assert exists_response.status_code == 200
    assert exists_response.json()["exists"] is True

    # All operations must reach the same responsible Shard.
    assert calls
    assert all(base_url == live_base_url for base_url in calls)


def test_unavailable_shard_returns_503_without_fallback(
    distributed_environment,
):
    client = distributed_environment["coordinator"]
    router = distributed_environment["router"]
    calls = distributed_environment["calls"]
    unavailable_base_url = distributed_environment["unavailable_base_url"]

    register_users_table(client)

    # Find a key assigned to the unavailable Shard.
    partition_key = find_key_for_shard(
        router,
        "shard-2",
    )

    calls.clear()

    response = client.post(
        f"/v1/tables/Users/records/{partition_key}",
        json={
            "value": {
                "name": "Bob",
            }
        },
    )

    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")

    assert calls == [unavailable_base_url]
