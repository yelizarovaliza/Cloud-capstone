class ShardUnavailableError(Exception):
    """Raised when the responsible Shard cannot be reached."""


class RecordAlreadyExistsError(Exception):
    """Raised when CREATE targets an existing partition key."""
