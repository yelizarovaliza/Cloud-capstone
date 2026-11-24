import asyncio
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app.shard.main import app
from app.shard.registration import register_with_coordinator


def test_registration_sends_correct_request():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert str(request.url) == (
            "http://coordinator:8000/v1/internal/shards/register"
        )

        payload = json.loads(request.content)

        assert payload == {
            "shardId": "shard-1",
            "baseUrl": "http://shard-1:8001",
        }

        return httpx.Response(
            201,
            json={
                "shardId": "shard-1",
                "registered": True,
                "virtualNodeCount": 128,
            },
        )

    transport = httpx.MockTransport(handler)

    result = asyncio.run(
        register_with_coordinator(
            coordinator_url="http://coordinator:8000",
            shard_id="shard-1",
            base_url="http://shard-1:8001",
            transport=transport,
        )
    )

    assert result["registered"] is True
    assert result["virtualNodeCount"] == 128


def test_registration_fails_when_coordinator_returns_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503)

    transport = httpx.MockTransport(handler)

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(
            register_with_coordinator(
                coordinator_url="http://coordinator:8000",
                shard_id="shard-1",
                base_url="http://shard-1:8001",
                transport=transport,
            )
        )


def test_shard_registers_during_startup(monkeypatch):
    monkeypatch.setenv("SHARD_ID", "shard-1")
    monkeypatch.setenv(
        "SHARD_BASE_URL",
        "http://127.0.0.1:8001",
    )
    monkeypatch.setenv(
        "COORDINATOR_URL",
        "http://127.0.0.1:8000",
    )

    calls = []

    async def fake_register(
        coordinator_url: str,
        shard_id: str,
        base_url: str,
    ) -> dict:
        calls.append((coordinator_url, shard_id, base_url))
        return {
            "shardId": shard_id,
            "registered": True,
            "virtualNodeCount": 128,
        }

    monkeypatch.setattr(
        "app.shard.main.register_with_coordinator",
        fake_register,
    )

    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200

    assert calls == [
        (
            "http://127.0.0.1:8000",
            "shard-1",
            "http://127.0.0.1:8001",
        )
    ]


def test_shard_startup_fails_without_required_configuration(
    monkeypatch,
):
    monkeypatch.delenv("SHARD_ID", raising=False)
    monkeypatch.delenv("SHARD_BASE_URL", raising=False)
    monkeypatch.delenv("COORDINATOR_URL", raising=False)

    with pytest.raises(RuntimeError):
        with TestClient(app):
            pass
