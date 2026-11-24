from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Record(BaseModel):
    """Public representation of a stored record."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    table_name: str = Field(alias="tableName")
    partition_key: str = Field(alias="partitionKey")
    value: dict[str, Any]


class ExistsResult(BaseModel):
    """Result of a record existence check."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    table_name: str = Field(alias="tableName")
    partition_key: str = Field(alias="partitionKey")
    exists: bool
