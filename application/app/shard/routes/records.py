
from fastapi import APIRouter, Path, Request, Response, status

from app.api.routes.tables import problem_response
from app.schemas.record import RecordInput
from app.schemas.record_response import ExistsResult, Record
from app.schemas.table import TABLE_NAME_PATTERN
from app.services.record_errors import RecordAlreadyExistsError


router = APIRouter(
    prefix="/v1/internal/tables",
    tags=["Internal Records"],
)


@router.post(
    "/{tableName}/records/{partitionKey}",
    status_code=status.HTTP_201_CREATED,
    response_model=Record,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
        409: {"description": "Record already exists"},
    },
)
def create_record(
    payload: RecordInput,
    request: Request,
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
    store = request.app.state.record_store

    try:
        return store.create(
            tableName,
            partitionKey,
            payload.value,
        )
    except RecordAlreadyExistsError:
        return problem_response(
            409,
            "Record already exists",
            "The partition key is already in use.",
        )


@router.get(
    "/{tableName}/records/{partitionKey}",
    response_model=Record,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Record not found"},
    },
)
def read_record(
    request: Request,
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
    store = request.app.state.record_store

    record = store.read(tableName, partitionKey)

    if record is None:
        return problem_response(
            404,
            "Record not found",
            "The requested record does not exist.",
        )

    return record


@router.get(
    "/{tableName}/records/{partitionKey}/exists",
    response_model=ExistsResult,
    response_model_by_alias=True,
    responses={
        400: {"description": "Invalid request"},
    },
)
def exists_record(
    request: Request,
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
    store = request.app.state.record_store

    return ExistsResult(
        tableName=tableName,
        partitionKey=partitionKey,
        exists=store.exists(tableName, partitionKey),
    )


@router.delete(
    "/{tableName}/records/{partitionKey}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        400: {"description": "Invalid request"},
        404: {"description": "Record not found"},
    },
)
def delete_record(
    request: Request,
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
    store = request.app.state.record_store

    deleted = store.delete(tableName, partitionKey)

    if not deleted:
        return problem_response(
            404,
            "Record not found",
            "The requested record does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
