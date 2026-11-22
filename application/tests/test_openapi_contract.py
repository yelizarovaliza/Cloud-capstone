
from app.main import app
from pathlib import Path

import yaml


def test_runtime_openapi_uses_version_31():
    schema = app.openapi()

    assert schema["openapi"] == "3.1.0"


def test_runtime_openapi_contains_public_record_operations():
    schema = app.openapi()
    paths = schema["paths"]

    assert "/v1/tables/{tableName}/records/{partitionKey}" in paths

    operations = paths[
        "/v1/tables/{tableName}/records/{partitionKey}"
    ]

    assert "post" in operations
    assert "get" in operations
    assert "delete" in operations

    assert (
        "/v1/tables/{tableName}/records/{partitionKey}/exists"
        in paths
    )


def test_runtime_openapi_contains_expected_response_codes():
    schema = app.openapi()

    operations = schema["paths"][
        "/v1/tables/{tableName}/records/{partitionKey}"
    ]

    assert "201" in operations["post"]["responses"]
    assert "409" in operations["post"]["responses"]
    assert "200" in operations["get"]["responses"]
    assert "404" in operations["get"]["responses"]
    assert "204" in operations["delete"]["responses"]


def test_runtime_public_paths_match_approved_yaml():
    yaml_path = Path(__file__).parents[2] / "docs" / "api" / "openapi.yaml"
    approved = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    runtime_paths = app.openapi()["paths"]

    public_paths = {
        "/v1/tables/{tableName}",
        "/v1/tables/{tableName}/records/{partitionKey}",
        "/v1/tables/{tableName}/records/{partitionKey}/exists",
    }

    for path in public_paths:
        assert path in approved["paths"]
        assert path in runtime_paths
