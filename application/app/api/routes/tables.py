from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse

from app.schemas.table import TABLE_NAME_PATTERN, TableDefinition
from app.services.table_registry import table_registry


router = APIRouter(prefix="/v1/tables", tags=["Tables"])


def problem_response(
    status_code: int,
    title: str,
    detail: str,
) -> JSONResponse:
    """Create an RFC 7807 problem response."""
    return JSONResponse(
        status_code=status_code,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
        },
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TableDefinition,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses={
        400: {"description": "Invalid table definition"},
        409: {"description": "Table already exists"},
    },
)
def register_table(table: TableDefinition):
    """Register a new table definition."""

    if not table_registry.register(table):
        return problem_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Table already exists",
            detail=f"Table '{table.name}' is already registered.",
        )

    return table


@router.get(
    "/{tableName}",
    response_model=TableDefinition,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses={
        400: {"description": "Invalid table name"},
        404: {"description": "Table not found"},
    },
)
def get_table(
    tableName: str = Path(
        alias="tableName",
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    ),
):
    """Retrieve a registered table definition."""

    table = table_registry.get(tableName)

    if table is None:
        return problem_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Table not found",
            detail=f"Table '{tableName}' is not registered.",
        )

    return table