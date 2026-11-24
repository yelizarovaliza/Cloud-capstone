import httpx


async def register_with_coordinator(
    coordinator_url: str,
    shard_id: str,
    base_url: str,
    transport: httpx.AsyncBaseTransport | None = None,
) -> dict:
    """Register this Shard with the Coordinator."""

    endpoint = f"{coordinator_url.rstrip('/')}/v1/internal/shards/register"

    payload = {
        "shardId": shard_id,
        "baseUrl": base_url,
    }

    async with httpx.AsyncClient(
        timeout=5.0,
        transport=transport,
    ) as client:
        response = await client.post(
            endpoint,
            json=payload,
        )
        response.raise_for_status()
        return response.json()
