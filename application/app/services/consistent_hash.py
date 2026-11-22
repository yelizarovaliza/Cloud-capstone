
from bisect import bisect_left
from hashlib import sha256


DEFAULT_VIRTUAL_NODES = 128


class EmptyHashRingError(Exception):
    """Raised when a lookup is attempted on an empty ring."""


class ConsistentHashRing:
    """SHA-256 consistent hash ring with virtual nodes."""

    def __init__(
        self,
        virtual_nodes_per_shard: int = DEFAULT_VIRTUAL_NODES,
    ) -> None:
        if (
            not isinstance(virtual_nodes_per_shard, int)
            or isinstance(virtual_nodes_per_shard, bool)
            or virtual_nodes_per_shard < 1
        ):
            raise ValueError(
                "virtual_nodes_per_shard must be a positive integer."
            )

        self.virtual_nodes_per_shard = virtual_nodes_per_shard

        # Each point: (hash_value, shard_id, virtual_node_index)
        self._ring: list[tuple[int, str, int]] = []
        self._shards: set[str] = set()

    @staticmethod
    def _hash(value: str) -> int:
        """Return an unsigned integer representation of SHA-256."""
        digest = sha256(value.encode("utf-8")).digest()
        return int.from_bytes(digest, byteorder="big")

    @staticmethod
    def qualify_key(
        table_name: str,
        partition_key: str,
    ) -> str:
        """Build the table-qualified key used for routing."""
        if not table_name or not partition_key:
            raise ValueError(
                "table_name and partition_key must not be empty."
            )

        return f"{table_name}#{partition_key}"

    def add_shard(self, shard_id: str) -> bool:
        """
        Add a Shard and generate its virtual nodes.

        Returns False if the Shard is already registered.
        """
        if not shard_id or not shard_id.strip():
            raise ValueError("shard_id must not be empty.")

        if shard_id in self._shards:
            return False

        points = [
            (
                self._hash(f"{shard_id}#{index}"),
                shard_id,
                index,
            )
            for index in range(self.virtual_nodes_per_shard)
        ]

        self._ring.extend(points)
        self._ring.sort()
        self._shards.add(shard_id)

        return True

    def remove_shard(self, shard_id: str) -> bool:
        """
        Remove a Shard and all its virtual nodes.

        Returns False if the Shard does not exist.
        """
        if shard_id not in self._shards:
            return False

        self._ring = [
            point
            for point in self._ring
            if point[1] != shard_id
        ]

        self._shards.remove(shard_id)
        return True

    def get_shard(
        self,
        table_name: str,
        partition_key: str,
    ) -> str:
        """Find the responsible Shard for a table-qualified key."""
        if not self._ring:
            raise EmptyHashRingError(
                "Cannot route a key because the hash ring is empty."
            )

        routing_key = self.qualify_key(
            table_name,
            partition_key,
        )

        key_hash = self._hash(routing_key)

        # Find the first point at or clockwise after the key hash.
        index = bisect_left(
            self._ring,
            (key_hash, "", -1),
        )

        # Wrap around to the first point if necessary.
        if index == len(self._ring):
            index = 0

        return self._ring[index][1]

    @property
    def shard_count(self) -> int:
        return len(self._shards)

    @property
    def ring_size(self) -> int:
        return len(self._ring)

    @property
    def shards(self) -> tuple[str, ...]:
        return tuple(sorted(self._shards))

    @property
    def ring_points(self) -> tuple[tuple[int, str, int], ...]:
        """Return an immutable snapshot of the ordered ring points."""
        return tuple(self._ring)
