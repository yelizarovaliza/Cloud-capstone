from typing import Protocol

from app.schemas.record_response import Record
from app.services.record_errors import (
    RecordAlreadyExistsError,
    ShardUnavailableError,
)
from app.services.routing_record_backend import RoutingRecordBackend


class RecordBackend(Protocol):
    """Interface for record storage and Shard routing."""

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record: ...

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None: ...

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool: ...

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool: ...


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
        return self.backend.create(
            table_name,
            partition_key,
            value,
        )

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        return self.backend.read(
            table_name,
            partition_key,
        )

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        return self.backend.exists(
            table_name,
            partition_key,
        )

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        return self.backend.delete(
            table_name,
            partition_key,
        )


class UnavailableRecordBackend:
    """Backend that simulates an unavailable Shard."""

    @staticmethod
    def _raise_unavailable() -> None:
        raise ShardUnavailableError("No Shard is currently available.")

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        self._raise_unavailable()

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        self._raise_unavailable()

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        self._raise_unavailable()

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        self._raise_unavailable()


# Use real Shard routing instead of the previous unavailable placeholder.
record_service = RecordService(RoutingRecordBackend())
