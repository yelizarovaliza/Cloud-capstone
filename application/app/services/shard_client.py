from urllib.parse import quote

import httpx

from app.schemas.record_response import ExistsResult, Record
from app.services.record_errors import (
    RecordAlreadyExistsError,
    ShardUnavailableError,
)


class ShardHttpClient:
    """HTTP client for forwarding Coordinator operations to a Shard."""

    timeout = 5.0

    def __init__(
        self,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.transport = transport

    @staticmethod
    def _record_path(
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> str:
        return (
            f"{base_url.rstrip('/')}"
            f"/v1/internal/tables/{quote(table_name, safe='')}"
            f"/records/{quote(partition_key, safe='')}"
        )

    def _request(
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> httpx.Response:
        try:
            with httpx.Client(
                timeout=self.timeout,
                transport=self.transport,
            ) as client:
                response = client.request(
                    method,
                    url,
                    **kwargs,
                )
        except httpx.RequestError as exc:
            raise ShardUnavailableError(
                "The responsible Shard could not be reached."
            ) from exc

        if response.status_code >= 500:
            raise ShardUnavailableError(
                "The responsible Shard returned a server error."
            )

        return response

    def create(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        response = self._request(
            "POST",
            self._record_path(
                base_url,
                table_name,
                partition_key,
            ),
            json={"value": value},
        )

        if response.status_code == 409:
            raise RecordAlreadyExistsError()

        response.raise_for_status()
        return Record.model_validate(response.json())

    def read(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        response = self._request(
            "GET",
            self._record_path(
                base_url,
                table_name,
                partition_key,
            ),
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return Record.model_validate(response.json())

    def exists(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> bool:
        url = (
            self._record_path(
                base_url,
                table_name,
                partition_key,
            )
            + "/exists"
        )

        response = self._request("GET", url)
        response.raise_for_status()

        result = ExistsResult.model_validate(response.json())
        return result.exists

    def delete(
        self,
        base_url: str,
        table_name: str,
        partition_key: str,
    ) -> bool:
        response = self._request(
            "DELETE",
            self._record_path(
                base_url,
                table_name,
                partition_key,
            ),
        )

        if response.status_code == 404:
            return False

        response.raise_for_status()
        return response.status_code == 204
