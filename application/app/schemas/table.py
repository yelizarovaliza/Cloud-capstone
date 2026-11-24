from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TABLE_NAME_PATTERN = r"^[A-Za-z][A-Za-z0-9_-]*$"


class TableDefinition(BaseModel):
    """Public definition of a key-value table."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        min_length=1,
        max_length=128,
        pattern=TABLE_NAME_PATTERN,
    )
    primary_key: Literal["partitionKey"] = Field(alias="primaryKey")
    fields: dict[str, str] | None = None
    description: str | None = None
