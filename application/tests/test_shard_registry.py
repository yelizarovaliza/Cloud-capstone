import pytest

from app.schemas.shard import ShardRegistration
from app.services.shard_registry import (
    DuplicateShardAddressError,
    ShardRegistry,
)


@pytest.fixture
def registry():
    return ShardRegistry()


def make_registration(
    shard_id: str,
    base_url: str,
) -> ShardRegistration:
    return ShardRegistration(
        shardId=shard_id,
        baseUrl=base_url,
    )


def test_register_new_shard(registry):
    registration = make_registration(
        "shard-1",
        "http://127.0.0.1:8001",
    )

    created, stored = registry.register(registration)

    assert created is True
    assert stored.shard_id == "shard-1"
    assert str(stored.base_url).rstrip("/") == (
        "http://127.0.0.1:8001"
    )
    assert len(registry.get_all()) == 1


def test_repeated_registration_refreshes_existing_shard(registry):
    first = make_registration(
        "shard-1",
        "http://127.0.0.1:8001",
    )
    updated = make_registration(
        "shard-1",
        "http://127.0.0.1:8011",
    )

    created_first, _ = registry.register(first)
    created_second, stored = registry.register(updated)

    assert created_first is True
    assert created_second is False
    assert len(registry.get_all()) == 1
    assert str(stored.base_url).rstrip("/") == (
        "http://127.0.0.1:8011"
    )


def test_different_shards_cannot_use_same_address(registry):
    registry.register(
        make_registration(
            "shard-1",
            "http://127.0.0.1:8001",
        )
    )

    with pytest.raises(DuplicateShardAddressError):
        registry.register(
            make_registration(
                "shard-2",
                "http://127.0.0.1:8001",
            )
        )

    assert len(registry.get_all()) == 1


def test_get_unknown_shard_returns_none(registry):
    assert registry.get("unknown") is None


def test_clear_removes_all_shards(registry):
    registry.register(
        make_registration(
            "shard-1",
            "http://127.0.0.1:8001",
        )
    )

    registry.clear()

    assert registry.get_all() == []