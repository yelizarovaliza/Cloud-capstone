from app.schemas.table import TableDefinition


class TableRegistry:
    """In-memory registry of table definitions."""

    def __init__(self) -> None:
        self._tables: dict[str, TableDefinition] = {}

    def register(self, table: TableDefinition) -> bool:
        """Register a table if its name is not already used."""
        if table.name in self._tables:
            return False

        self._tables[table.name] = table
        return True

    def get(self, table_name: str) -> TableDefinition | None:
        """Return a table definition or None if it does not exist."""
        return self._tables.get(table_name)

    def clear(self) -> None:
        """Clear all registered tables."""
        self._tables.clear()


table_registry = TableRegistry()