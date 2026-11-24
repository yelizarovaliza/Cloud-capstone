from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.tables import router as tables_router
from app.api.routes.records import router as records_router
from app.core.config import settings
from app.api.routes.shards import router as shards_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="A lightweight distributed key-value store.",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return validation errors using RFC 7807 format."""
    return JSONResponse(
        status_code=400,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": "Invalid request",
            "status": 400,
            "detail": "The request does not match the API contract.",
        },
    )


app.include_router(health_router)
app.include_router(tables_router)
app.include_router(records_router)
app.include_router(shards_router)


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.1.0",
    )

    for path_item in openapi_schema["paths"].values():
        for operation in path_item.values():
            if isinstance(operation, dict):
                operation.get("responses", {}).pop("422", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
