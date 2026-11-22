
from app.schemas.table import TableDefinition
from app.services.table_registry import TableRegistry


def create_table(name: str = "Users") -> TableDefinition:
    return TableDefinition(
        name=name,
        primaryKey="partitionKey",
    )


def test_register_and_get_table():
    registry = TableRegistry()
    table = create_table()

    registered = registry.register(table)

    assert registered is True
    assert registry.get("Users") == table


def test_register_duplicate_table_does_not_overwrite():
    registry = TableRegistry()
    original = create_table()
    duplicate = TableDefinition(
        name="Users",
        primaryKey="partitionKey",
        description="Duplicate table",
    )

    assert registry.register(original) is True
    assert registry.register(duplicate) is False
    assert registry.get("Users") == original


def test_get_missing_table_returns_none():
    registry = TableRegistry()

    assert registry.get("Unknown") is None
