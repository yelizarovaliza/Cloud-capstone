
from fastapi import APIRouter, Path, Response, status

from app.api.routes.tables import problem_response
from app.schemas.record import RecordInput
from app.schemas.record_response import ExistsResult, Record
from app.services.record_service import (
    ShardUnavailableError,
    record_service,
)
from app.schemas.table import TABLE_NAME_PATTERN
from app.services.table_registry import table_registry
from app.services.record_service import RecordAlreadyExistsError


def table_registry_contains(table_name: str) -> bool:
    return table_registry.get(table_name) is not None

router = APIRouter(prefix="/v1/tables", tags=["Records"])

@router.post(
    "/{tableName}/records/{partitionKey}",
    status_code=status.HTTP_201_CREATED,
    response_model=Record,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Table not found"},
        409: {"description": "Record already exists"},
        503: {"description": "Shard unavailable"},
    },
)
def create_record(
    payload: RecordInput,
    tableName: str = Path(
        alias="tableName",
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    ),
    partitionKey: str = Path(
        alias="partitionKey",
        min_length=1,
        max_length=1024,
    ),
):
    if not table_registry_contains(tableName):
        return problem_response(404, "Table not found", f"Table '{tableName}' is not registered.")

    try:
        return record_service.create(
            tableName,
            partitionKey,
            payload.value,
        )
    except ShardUnavailableError:
        return problem_response(503, "Shard unavailable", "No responsible Shard is available.")
    except RecordAlreadyExistsError:
        return problem_response(409, "Record already exists", "The partition key is already in use.")


@router.get(
    "/{tableName}/records/{partitionKey}",
    response_model=Record,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Record or table not found"},
        503: {"description": "Shard unavailable"},
    },
)
def read_record(
    tableName: str = Path(
        alias="tableName",
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    ),
    partitionKey: str = Path(
        alias="partitionKey",
        min_length=1,
        max_length=1024,
    ),
):
    if not table_registry_contains(tableName):
        return problem_response(404, "Table not found", f"Table '{tableName}' is not registered.")

    try:
        record = record_service.read(tableName, partitionKey)
    except ShardUnavailableError:
        return problem_response(503, "Shard unavailable", "No responsible Shard is available.")

    if record is None:
        return problem_response(404, "Record not found", "The requested record does not exist.")

    return record


@router.get(
    "/{tableName}/records/{partitionKey}/exists",
    response_model=ExistsResult,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Table not found"},
        503: {"description": "Shard unavailable"},
    },
)
def exists_record(
    tableName: str = Path(
        alias="tableName",
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    ),
    partitionKey: str = Path(
        alias="partitionKey",
        min_length=1,
        max_length=1024,
    ),
):
    if not table_registry_contains(tableName):
        return problem_response(404, "Table not found", f"Table '{tableName}' is not registered.")

    try:
        exists = record_service.exists(tableName, partitionKey)
    except ShardUnavailableError:
        return problem_response(503, "Shard unavailable", "No responsible Shard is available.")

    return ExistsResult(
        tableName=tableName,
        partitionKey=partitionKey,
        exists=exists,
    )


@router.delete(
    "/{tableName}/records/{partitionKey}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Record or table not found"},
        503: {"description": "Shard unavailable"},
    },
)
def delete_record(
    tableName: str = Path(
        alias="tableName",
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    ),
    partitionKey: str = Path(
        alias="partitionKey",
        min_length=1,
        max_length=1024,
    ),
):
    if not table_registry_contains(tableName):
        return problem_response(404, "Table not found", f"Table '{tableName}' is not registered.")

    try:
        deleted = record_service.delete(tableName, partitionKey)
    except ShardUnavailableError:
        return problem_response(503, "Shard unavailable", "No responsible Shard is available.")

    if not deleted:
        return problem_response(404, "Record not found", "The requested record does not exist.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
