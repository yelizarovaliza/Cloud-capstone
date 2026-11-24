from typing import Any

from pydantic import BaseModel, ConfigDict


class RecordInput(BaseModel):
    """Request body for creating a key-value record."""

    model_config = ConfigDict(extra="forbid")

    value: dict[str, Any]
