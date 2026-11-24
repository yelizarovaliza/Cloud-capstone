import json
import sqlite3
from contextlib import closing
from pathlib import Path

from app.schemas.record_response import Record
from app.services.record_errors import RecordAlreadyExistsError


class SQLiteRecordStore:
    """Local persistent key-value storage for one Shard."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

    def initialize(self) -> None:
        """Create the database and records table if they do not exist."""
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    table_name TEXT NOT NULL,
                    partition_key TEXT NOT NULL,
                    value_json TEXT NOT NULL,
                    PRIMARY KEY (table_name, partition_key)
                )
                """
            )
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=5.0,
        )
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def create(
        self,
        table_name: str,
        partition_key: str,
        value: dict,
    ) -> Record:
        """Insert a new record without overwriting an existing one."""
        serialized_value = json.dumps(value)

        try:
            with closing(self._connect()) as connection:
                with connection:
                    connection.execute(
                        """
                        INSERT INTO records (
                            table_name,
                            partition_key,
                            value_json
                        )
                        VALUES (?, ?, ?)
                        """,
                        (
                            table_name,
                            partition_key,
                            serialized_value,
                        ),
                    )
        except sqlite3.IntegrityError as exc:
            raise RecordAlreadyExistsError("The record already exists.") from exc

        return Record(
            tableName=table_name,
            partitionKey=partition_key,
            value=value,
        )

    def read(
        self,
        table_name: str,
        partition_key: str,
    ) -> Record | None:
        """Retrieve a record by its table and partition key."""
        with closing(self._connect()) as connection:
            row = connection.execute(
                """
                SELECT value_json
                FROM records
                WHERE table_name = ? AND partition_key = ?
                """,
                (table_name, partition_key),
            ).fetchone()

        if row is None:
            return None

        return Record(
            tableName=table_name,
            partitionKey=partition_key,
            value=json.loads(row[0]),
        )

    def exists(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        """Check whether a record exists."""
        with closing(self._connect()) as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM records
                WHERE table_name = ? AND partition_key = ?
                """,
                (table_name, partition_key),
            ).fetchone()

        return row is not None

    def delete(
        self,
        table_name: str,
        partition_key: str,
    ) -> bool:
        """Delete a record and report whether it existed."""
        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    DELETE FROM records
                    WHERE table_name = ? AND partition_key = ?
                    """,
                    (table_name, partition_key),
                )

        return cursor.rowcount > 0
