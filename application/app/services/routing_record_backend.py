from typing import Protocol

from app.schemas.record_response import Record
from app.services.record_errors import ShardUnavailableError
from app.services.shard_client import ShardHttpClient
from app.services.shard_registry import shard_registry
from app.services.shard_router import (
    NoRegisteredShardsError,
    ShardRouter,
)


class ShardClientProtocol(Protocol):
    def create(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record: ...

    def read(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> Record | None: ...

    def exists(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> bool: ...

    def delete(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> bool: ...


class RoutingRecordBackend:
    """Routes record operations to the responsible Shard."""

    def __init__(
        self,
        router: ShardRouter | None = None,
        client: ShardClientProtocol | None = None,
    ) -> None:
        self.router = router or ShardRouter(shard_registry)
        self.client = client or ShardHttpClient()

    def _resolve(self, table_name: str, partition_key: str) -> str:
        try:
            registration = self.router.resolve(
                table_name,
                partition_key,
            )
        except NoRegisteredShardsError as exc:
            raise ShardUnavailableError("No responsible Shard is registered.") from exc

        return str(registration.base_url).rstrip("/")

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        base_url = self._resolve(table_name, partition_key)

        return self.client.create(
            base_url,
            table_name,
            partition_key,
            value,
        )

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        base_url = self._resolve(table_name, partition_key)

        return self.client.read(
            base_url,
            table_name,
            partition_key,
        )

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        base_url = self._resolve(table_name, partition_key)

        return self.client.exists(
            base_url,
            table_name,
            partition_key,
        )

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        base_url = self._resolve(table_name, partition_key)

        return self.client.delete(
            base_url,
            table_name,
            partition_key,
        )
