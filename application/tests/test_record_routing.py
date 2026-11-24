import pytest

from app.schemas.record_response import Record
from app.schemas.shard import ShardRegistration
from app.services.routing_record_backend import RoutingRecordBackend
from app.services.shard_registry import ShardRegistry
from app.services.shard_router import ShardRouter


class FakeShardClient:
    def __init__(self):
        self.calls = []

    def create(self, base_url, table_name, partition_key, value):
        self.calls.append(("create", base_url, table_name, partition_key))
        return Record(
            tableName=table_name,
            partitionKey=partition_key,
            value=value,
        )

    def read(self, base_url, table_name, partition_key):
        self.calls.append(("read", base_url, table_name, partition_key))
        return Record(
            tableName=table_name,
            partitionKey=partition_key,
            value={"name": "test"},
        )

    def exists(self, base_url, table_name, partition_key):
        self.calls.append(("exists", base_url, table_name, partition_key))
        return True

    def delete(self, base_url, table_name, partition_key):
        self.calls.append(("delete", base_url, table_name, partition_key))
        return True


@pytest.fixture
def routing_setup():
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
    client = FakeShardClient()

    backend = RoutingRecordBackend(
        router=router,
        client=client,
    )

    return registry, router, client, backend


def test_all_operations_use_the_same_shard(routing_setup):
    _, router, client, backend = routing_setup

    table_name = "Users"
    partition_key = "user-123"

    expected_registration = router.resolve(
        table_name,
        partition_key,
    )
    expected_url = str(expected_registration.base_url).rstrip("/")

    created = backend.create(
        table_name,
        partition_key,
        {"name": "test"},
    )
    read = backend.read(table_name, partition_key)
    exists = backend.exists(table_name, partition_key)
    deleted = backend.delete(table_name, partition_key)

    assert created.partition_key == partition_key
    assert read is not None
    assert exists is True
    assert deleted is True

    assert len(client.calls) == 4

    assert all(call[1] == expected_url for call in client.calls)

    assert [call[0] for call in client.calls] == [
        "create",
        "read",
        "exists",
        "delete",
    ]


def test_same_partition_key_in_different_tables_is_qualified(
    routing_setup,
):
    _, router, _, _ = routing_setup

    users_owner = router.resolve(
        "Users",
        "record-1",
    )
    orders_owner = router.resolve(
        "Orders",
        "record-1",
    )

    assert users_owner.shard_id in ("shard-1", "shard-2")
    assert orders_owner.shard_id in ("shard-1", "shard-2")


def test_new_registration_updates_ring_membership(
    routing_setup,
):
    registry, router, _, _ = routing_setup

    router.resolve("Users", "user-123")

    assert router.ring.shard_count == 2

    registry.register(
        ShardRegistration(
            shardId="shard-3",
            baseUrl="http://127.0.0.1:8003",
        )
    )

    router.resolve("Users", "user-123")

    assert router.ring.shard_count == 3
    assert router.ring.ring_size == 3 * 128


def test_repeated_registration_does_not_duplicate_ring_nodes(
    routing_setup,
):
    registry, router, _, _ = routing_setup

    router.resolve("Users", "user-123")

    assert router.ring.ring_size == 2 * 128

    registry.register(
        ShardRegistration(
            shardId="shard-1",
            baseUrl="http://127.0.0.1:8011",
        )
    )

    registration = router.resolve("Users", "user-123")

    assert router.ring.shard_count == 2
    assert router.ring.ring_size == 2 * 128

    if registration.shard_id == "shard-1":
        assert str(registration.base_url).rstrip("/") == ("http://127.0.0.1:8011")


def test_empty_registry_has_no_responsible_shard():
    from app.services.record_errors import ShardUnavailableError

    registry = ShardRegistry()
    backend = RoutingRecordBackend(
        router=ShardRouter(registry),
        client=FakeShardClient(),
    )

    with pytest.raises(ShardUnavailableError):
        backend.read("Users", "user-123")
