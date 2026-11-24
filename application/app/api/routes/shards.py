from fastapi import APIRouter, Response, status

from app.api.routes.tables import problem_response
from app.schemas.shard import (
    ShardRegistration,
    ShardRegistrationResult,
)
from app.services.shard_registry import (
    DuplicateShardAddressError,
    shard_registry,
)


router = APIRouter(
    prefix="/v1/internal/shards",
    tags=["Shard Registry"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ShardRegistrationResult,
    response_model_by_alias=True,
    responses={
        200: {
            "model": ShardRegistrationResult,
            "description": "Shard registration refreshed",
        },
        400: {"description": "Invalid registration request"},
        409: {"description": "Shard address already belongs to another Shard"},
    },
)
def register_shard(
    payload: ShardRegistration,
    response: Response,
):
    """Register a new Shard or refresh an existing registration."""

    try:
        created, registration = shard_registry.register(payload)
    except DuplicateShardAddressError as exc:
        return problem_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Shard address conflict",
            detail=str(exc),
        )

    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

    return ShardRegistrationResult(
        shardId=registration.shard_id,
        registered=True,
        virtualNodeCount=128,
    )
