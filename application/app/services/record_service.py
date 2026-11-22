
from typing import Protocol

from app.schemas.record_response import ExistsResult, Record


class RecordBackend(Protocol):
    """Interface for the future Shard communication layer."""

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        ...

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        ...

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        ...

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        ...


class ShardUnavailableError(Exception):
    """Raised when no responsible Shard is available."""


class RecordService:
    """Coordinator-facing service for record operations."""

    def __init__(self, backend: RecordBackend):
        self.backend = backend

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        return self.backend.create(table_name, partition_key, value)

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        return self.backend.read(table_name, partition_key)

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        return self.backend.exists(table_name, partition_key)

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        return self.backend.delete(table_name, partition_key)


class UnavailableRecordBackend:
    """Default backend until Shard routing is implemented."""

    def _raise_unavailable(self):
        raise ShardUnavailableError("No Shard is currently available.")

    def create(self, table_name: str, partition_key: str, value: dict) -> Record:
        self._raise_unavailable()

    def read(self, table_name: str, partition_key: str) -> Record | None:
        self._raise_unavailable()

    def exists(self, table_name: str, partition_key: str) -> bool:
        self._raise_unavailable()

    def delete(self, table_name: str, partition_key: str) -> bool:
        self._raise_unavailable()


record_service = RecordService(UnavailableRecordBackend())

class RecordAlreadyExistsError(Exception):
    """Raised when CREATE targets an existing partition key."""