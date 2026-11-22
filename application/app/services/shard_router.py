
from threading import RLock

from app.services.consistent_hash import ConsistentHashRing
from app.services.shard_registry import ShardRegistry
from app.schemas.shard import ShardRegistration


class NoRegisteredShardsError(Exception):
    """Raised when no Shards are registered."""


class ShardRouter:
    """Resolves the responsible Shard using the current registry."""

    def __init__(
        self,
        registry: ShardRegistry,
        virtual_nodes_per_shard: int = 128,
    ) -> None:
        self.registry = registry
        self.virtual_nodes_per_shard = virtual_nodes_per_shard

        self._ring = ConsistentHashRing(
            virtual_nodes_per_shard=virtual_nodes_per_shard,
        )
        self._member_ids: tuple[str, ...] = ()
        self._lock = RLock()

    def resolve(
        self,
        table_name: str,
        partition_key: str,
    ) -> ShardRegistration:
        """Return the current registration of the responsible Shard."""

        registrations = self.registry.get_all()

        if not registrations:
            raise NoRegisteredShardsError(
                "No Shards are registered with the Coordinator."
            )

        registrations_by_id = {
            registration.shard_id: registration
            for registration in registrations
        }

        current_ids = tuple(sorted(registrations_by_id))

        with self._lock:
            if current_ids != self._member_ids:
                new_ring = ConsistentHashRing(
                    virtual_nodes_per_shard=(
                        self.virtual_nodes_per_shard
                    )
                )

                for shard_id in current_ids:
                    new_ring.add_shard(shard_id)

                self._ring = new_ring
                self._member_ids = current_ids

            shard_id = self._ring.get_shard(
                table_name,
                partition_key,
            )

        return registrations_by_id[shard_id]

    @property
    def ring(self) -> ConsistentHashRing:
        """Expose the current ring for inspection and testing."""
        return self._ring
