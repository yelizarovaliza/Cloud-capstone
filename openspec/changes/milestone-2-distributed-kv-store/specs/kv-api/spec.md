# Spec Delta

## Purpose

Defines the externally observable REST data model and CRUD behavior for Milestone 2.

## ADDED Requirements

### Requirement: Table registration
The public API SHALL allow a client to register a named table and SHALL reject duplicate or invalid table definitions.

#### Scenario: Valid table registration
- **WHEN** a client submits a unique table name and valid record schema
- **THEN** the Coordinator creates the definition and returns 201 with the canonical table identifier

#### Scenario: Invalid table registration
- **WHEN** a client submits an unsupported or incomplete table definition
- **THEN** the API returns 400 with an RFC 7807 problem response

### Requirement: Record creation
The public API SHALL create or replace a record by table name and partition key.

#### Scenario: Successful create
- **WHEN** a valid record is submitted for a registered table
- **THEN** the Coordinator routes it to the responsible Shard and returns 200 or 201 according to the operation contract

#### Scenario: Missing table
- **WHEN** a create references an unregistered table
- **THEN** the API returns 404

### Requirement: Record reads and existence
The public API SHALL retrieve a record or report whether its key exists.

#### Scenario: Existing record
- **WHEN** a read or exists request names a present partition key
- **THEN** the API returns the record or an existence result of true

#### Scenario: Missing record
- **WHEN** a read or exists request names an absent partition key
- **THEN** READ returns 404 and EXISTS returns an existence result of false

### Requirement: Record deletion
The public API SHALL remove a record by table name and partition key.

#### Scenario: Successful delete
- **WHEN** a DELETE identifies a present record
- **THEN** the selected Shard removes it and returns 204

#### Scenario: Delete absent record
- **WHEN** a DELETE identifies no present record
- **THEN** the API returns 404

### Requirement: Structured errors
The API SHALL return machine-readable JSON errors and SHALL identify table, key, Shard availability, or validation failures without exposing secrets.

#### Scenario: Shard unavailable
- **WHEN** the responsible Shard cannot be reached
- **THEN** the API returns a documented 503 problem response
