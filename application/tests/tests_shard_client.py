import httpx
import pytest

from app.services.record_errors import ShardUnavailableError
from app.services.shard_client import ShardHttpClient


def test_server_error_raises_shard_unavailable():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            503,
            request=request,
        )
    )

    client = ShardHttpClient(transport=transport)

    with pytest.raises(ShardUnavailableError):
        client.read(
            "http://127.0.0.1:8001",
            "Users",
            "user-1",
        )


from app.schemas.shard import ShardRegistration
from app.services.routing_record_backend import RoutingRecordBackend
from app.services.shard_registry import ShardRegistry
from app.services.shard_router import ShardRouter


def test_unavailable_responsible_shard_has_no_fallback():
    requested_urls = []

    def handler(request):
        requested_urls.append(str(request.url))
        return httpx.Response(503, request=request)

    registry = ShardRegistry()
    registry.register(
        ShardRegistration(
            shardId="shard-1",
            baseUrl="http://127.0.0.1:8001",
        )
    )
    registry.register(
        ShardRegistration(
            shardId="shard-2",
            baseUrl="http://127.0.0.1:8002",
        )
    )

    router = ShardRouter(registry)
    registration = router.resolve("Users", "user-1")

    transport = httpx.MockTransport(handler)
    shard_client = ShardHttpClient(transport=transport)

    backend = RoutingRecordBackend(
        router=router,
        client=shard_client,
    )

    with pytest.raises(ShardUnavailableError):
        backend.read("Users", "user-1")

    assert len(requested_urls) == 1
    assert requested_urls[0].startswith(
        str(registration.base_url).rstrip("/")
    )

def test_connection_error_raises_shard_unavailable():
    def handler(request):
        raise httpx.ConnectError(
            "Connection failed",
            request=request,
        )

    transport = httpx.MockTransport(handler)
    client = ShardHttpClient(transport=transport)

    with pytest.raises(ShardUnavailableError):
        client.read(
            "http://127.0.0.1:8001",
            "Users",
            "user-1",
        )