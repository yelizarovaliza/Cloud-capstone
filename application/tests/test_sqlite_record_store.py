import pytest

from app.schemas.record_response import Record
from app.services.record_errors import RecordAlreadyExistsError
from app.storage.sqlite_record_store import SQLiteRecordStore


@pytest.fixture
def store(tmp_path):
    database_path = tmp_path / "shard.sqlite3"
    record_store = SQLiteRecordStore(database_path)
    record_store.initialize()
    return record_store


def test_create_and_read_record(store):
    value = {"name": "Alice", "age": 25}

    created = store.create("Users", "user-1", value)
    retrieved = store.read("Users", "user-1")

    assert created == retrieved
    assert retrieved == Record(
        tableName="Users",
        partitionKey="user-1",
        value=value,
    )


def test_create_duplicate_record_does_not_overwrite(store):
    store.create("Users", "user-1", {"name": "Alice"})

    with pytest.raises(RecordAlreadyExistsError):
        store.create("Users", "user-1", {"name": "Bob"})

    record = store.read("Users", "user-1")
    assert record.value == {"name": "Alice"}


def test_same_partition_key_can_exist_in_different_tables(store):
    store.create("Users", "item-1", {"type": "user"})
    store.create("Orders", "item-1", {"type": "order"})

    assert store.read("Users", "item-1").value == {"type": "user"}
    assert store.read("Orders", "item-1").value == {"type": "order"}


def test_read_missing_record_returns_none(store):
    assert store.read("Users", "missing") is None


def test_exists_returns_correct_result(store):
    store.create("Users", "user-1", {"name": "Alice"})

    assert store.exists("Users", "user-1") is True
    assert store.exists("Users", "missing") is False


def test_delete_record(store):
    store.create("Users", "user-1", {"name": "Alice"})

    assert store.delete("Users", "user-1") is True
    assert store.read("Users", "user-1") is None
    assert store.delete("Users", "user-1") is False


def test_data_survives_database_reopen(tmp_path):
    database_path = tmp_path / "persistent.sqlite3"

    first_store = SQLiteRecordStore(database_path)
    first_store.initialize()
    first_store.create("Users", "user-1", {"name": "Alice"})

    second_store = SQLiteRecordStore(database_path)
    second_store.initialize()

    record = second_store.read("Users", "user-1")

    assert record is not None
    assert record.value == {"name": "Alice"}
