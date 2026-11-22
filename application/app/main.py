from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.tables import router as tables_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    openapi_version="3.1.0",
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