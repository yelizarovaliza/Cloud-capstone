from app.main import app
from pathlib import Path

import yaml


def parameter_name(parameter, components=None):
    if "$ref" in parameter:
        component_name = parameter["$ref"].rsplit("/", 1)[-1]
        if components is not None:
            return components["parameters"][component_name]["name"]
        return component_name
    return parameter["name"]


def item_parameter_names(item, components=None):
    parameters = list(item.get("parameters", []))
    for method in ("get", "post", "put", "patch", "delete"):
        if method in item:
            parameters.extend(item[method].get("parameters", []))
    return {parameter_name(parameter, components) for parameter in parameters}


def test_runtime_openapi_uses_version_31():
    schema = app.openapi()

    assert schema["openapi"] == "3.1.0"


def test_runtime_openapi_contains_public_record_operations():
    schema = app.openapi()
    paths = schema["paths"]

    assert "/v1/tables/{tableName}/records/{partitionKey}" in paths

    operations = paths["/v1/tables/{tableName}/records/{partitionKey}"]

    assert "post" in operations
    assert "get" in operations
    assert "delete" in operations

    assert "/v1/tables/{tableName}/records/{partitionKey}/exists" in paths


def test_runtime_openapi_contains_expected_response_codes():
    schema = app.openapi()

    operations = schema["paths"]["/v1/tables/{tableName}/records/{partitionKey}"]

    assert "201" in operations["post"]["responses"]
    assert "409" in operations["post"]["responses"]
    assert "200" in operations["get"]["responses"]
    assert "404" in operations["get"]["responses"]
    assert "204" in operations["delete"]["responses"]


def test_runtime_public_paths_match_approved_yaml():
    yaml_path = Path(__file__).parents[2] / "docs" / "api" / "openapi.yaml"
    approved = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    runtime = app.openapi()
    approved_paths = approved["paths"]
    runtime_paths = runtime["paths"]

    public_paths = {
        "/v1/tables",
        "/v1/tables/{tableName}",
        "/v1/tables/{tableName}/records/{partitionKey}",
        "/v1/tables/{tableName}/records/{partitionKey}/exists",
    }

    for path in public_paths:
        assert path in approved_paths
        assert path in runtime_paths

        approved_item = approved_paths[path]
        runtime_item = runtime_paths[path]

        approved_methods = {
            method
            for method in ("get", "post", "put", "patch", "delete")
            if method in approved_item
        }
        runtime_methods = {
            method
            for method in ("get", "post", "put", "patch", "delete")
            if method in runtime_item
        }
        assert runtime_methods == approved_methods

        for method in approved_methods:
            approved_responses = set(approved_item[method]["responses"].keys())
            runtime_responses = set(runtime_item[method]["responses"].keys())
            assert runtime_responses == approved_responses

        approved_parameters = item_parameter_names(
            approved_item,
            approved["components"],
        )
        runtime_parameters = item_parameter_names(runtime_item)
        assert runtime_parameters == approved_parameters
