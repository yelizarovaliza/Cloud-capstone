from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Check whether the application is running."""
    return {"status": "ok"}
