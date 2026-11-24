from threading import RLock

from app.schemas.shard import ShardRegistration


class DuplicateShardAddressError(Exception):
    """Raised when another Shard already uses the same base URL."""


class ShardRegistry:
    """In-memory registry of Shards known to the Coordinator."""

    def __init__(self) -> None:
        self._shards: dict[str, ShardRegistration] = {}
        self._lock = RLock()

    def register(
        self,
        registration: ShardRegistration,
    ) -> tuple[bool, ShardRegistration]:
        """
        Register a new Shard or refresh an existing one.

        Returns:
            (created, registration)
            created is True only for a new shard_id.
        """
        shard_id = registration.shard_id
        base_url = str(registration.base_url).rstrip("/")

        normalized = ShardRegistration(
            shardId=shard_id,
            baseUrl=base_url,
        )

        with self._lock:
            for existing_id, existing in self._shards.items():
                if (
                    existing_id != shard_id
                    and str(existing.base_url).rstrip("/") == base_url
                ):
                    raise DuplicateShardAddressError(
                        f"Address '{base_url}' is already used by "
                        f"Shard '{existing_id}'."
                    )

            created = shard_id not in self._shards
            self._shards[shard_id] = normalized

            return created, normalized

    def get(self, shard_id: str) -> ShardRegistration | None:
        with self._lock:
            return self._shards.get(shard_id)

    def get_all(self) -> list[ShardRegistration]:
        with self._lock:
            return list(self._shards.values())

    def clear(self) -> None:
        with self._lock:
            self._shards.clear()


shard_registry = ShardRegistry()
