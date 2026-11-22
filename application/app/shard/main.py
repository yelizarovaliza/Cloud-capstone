import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.shard.registration import register_with_coordinator


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set."
        )

    return value


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Register the Shard before accepting requests."""

    shard_id = required_env("SHARD_ID")
    base_url = required_env("SHARD_BASE_URL")
    coordinator_url = required_env("COORDINATOR_URL")

    registration_result = await register_with_coordinator(
        coordinator_url=coordinator_url,
        shard_id=shard_id,
        base_url=base_url,
    )

    app.state.registration = registration_result

    yield


app = FastAPI(
    title="Cloud Capstone Shard",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}