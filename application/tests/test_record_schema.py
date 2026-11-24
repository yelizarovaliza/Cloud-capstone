import pytest
from pydantic import ValidationError

from app.schemas.record import RecordInput


def test_valid_record_input():
    payload = {
        "value": {
            "email": "user@example.com",
            "age": 20,
            "active": True,
        }
    }

    record = RecordInput.model_validate(payload)

    assert record.value == payload["value"]


def test_record_input_requires_value():
    with pytest.raises(ValidationError):
        RecordInput.model_validate({})


def test_record_value_must_be_an_object():
    with pytest.raises(ValidationError):
        RecordInput.model_validate({"value": ["not", "an", "object"]})


def test_record_input_rejects_unknown_top_level_fields():
    with pytest.raises(ValidationError):
        RecordInput.model_validate(
            {
                "value": {"email": "user@example.com"},
                "partitionKey": "user-1",
            }
        )
