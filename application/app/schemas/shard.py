from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class ShardRegistration(BaseModel):
    """Information a Shard sends to the Coordinator."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    shard_id: str = Field(
        alias="shardId",
        min_length=1,
        max_length=128,
    )
    base_url: AnyHttpUrl = Field(alias="baseUrl")


class ShardRegistrationResult(BaseModel):
    """Coordinator response after registering a Shard."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    shard_id: str = Field(alias="shardId")
    registered: bool
    virtual_node_count: int = Field(
        default=128,
        alias="virtualNodeCount",
        ge=128,
        le=128,
    )
