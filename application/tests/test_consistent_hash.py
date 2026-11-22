
import hashlib

import pytest

from app.services.consistent_hash import (
    ConsistentHashRing,
    DEFAULT_VIRTUAL_NODES,
    EmptyHashRingError,
)


def test_default_virtual_node_count():
    ring = ConsistentHashRing()

    assert ring.virtual_nodes_per_shard == 128


def test_custom_virtual_node_count():
    ring = ConsistentHashRing(
        virtual_nodes_per_shard=16,
    )

    ring.add_shard("shard-1")

    assert ring.ring_size == 16


def test_add_shard_creates_virtual_nodes():
    ring = ConsistentHashRing()

    ring.add_shard("shard-1")
    ring.add_shard("shard-2")

    assert ring.shard_count == 2
    assert ring.ring_size == 2 * DEFAULT_VIRTUAL_NODES


def test_duplicate_shard_does_not_create_virtual_nodes():
    ring = ConsistentHashRing()

    first = ring.add_shard("shard-1")
    second = ring.add_shard("shard-1")

    assert first is True
    assert second is False
    assert ring.shard_count == 1
    assert ring.ring_size == DEFAULT_VIRTUAL_NODES


def test_hash_points_use_sha256():
    ring = ConsistentHashRing(
        virtual_nodes_per_shard=2,
    )

    ring.add_shard("shard-1")

    expected_hash = int.from_bytes(
        hashlib.sha256(
            b"shard-1#0"
        ).digest(),
        byteorder="big",
    )

    assert (
        expected_hash,
        "shard-1",
        0,
    ) in ring.ring_points


def test_lookup_is_deterministic_regardless_of_add_order():
    ring_a = ConsistentHashRing()
    ring_b = ConsistentHashRing()

    ring_a.add_shard("shard-1")
    ring_a.add_shard("shard-2")
    ring_a.add_shard("shard-3")

    ring_b.add_shard("shard-3")
    ring_b.add_shard("shard-1")
    ring_b.add_shard("shard-2")

    keys = [
        ("users", "user-1"),
        ("users", "user-2"),
        ("orders", "order-1"),
        ("products", "product-1"),
    ]

    for table_name, partition_key in keys:
        assert ring_a.get_shard(
            table_name,
            partition_key,
        ) == ring_b.get_shard(
            table_name,
            partition_key,
        )


def test_partition_key_is_table_qualified():
    assert ConsistentHashRing.qualify_key(
        "users",
        "user-123",
    ) == "users#user-123"


def test_lookup_on_empty_ring_raises_error():
    ring = ConsistentHashRing()

    with pytest.raises(EmptyHashRingError):
        ring.get_shard("users", "user-123")


def test_remove_shard_removes_its_virtual_nodes():
    ring = ConsistentHashRing()

    ring.add_shard("shard-1")
    ring.add_shard("shard-2")

    removed = ring.remove_shard("shard-1")

    assert removed is True
    assert ring.shard_count == 1
    assert ring.ring_size == DEFAULT_VIRTUAL_NODES
    assert ring.shards == ("shard-2",)


def test_remove_unknown_shard_changes_nothing():
    ring = ConsistentHashRing()
    ring.add_shard("shard-1")

    removed = ring.remove_shard("unknown")

    assert removed is False
    assert ring.shard_count == 1
    assert ring.ring_size == DEFAULT_VIRTUAL_NODES


def test_lookup_wraps_around_to_first_ring_point(monkeypatch):
    ring = ConsistentHashRing()
    ring.add_shard("shard-1")
    ring.add_shard("shard-2")

    first_shard = ring.ring_points[0][1]

    # Simulate a key hash greater than every ring point.
    monkeypatch.setattr(
        ring,
        "_hash",
        lambda value: 2**256,
    )

    assert ring.get_shard(
        "users",
        "user-123",
    ) == first_shard


def test_invalid_virtual_node_count_is_rejected():
    with pytest.raises(ValueError):
        ConsistentHashRing(virtual_nodes_per_shard=0)
