# Spec Delta

## Purpose

Defines the externally observable REST data model and CRUD behavior for Milestone 2.

## ADDED Requirements

### Requirement: Table information retrieval

The public API SHALL allow a client to retrieve the definition of an existing table by its name.

#### Scenario: Existing table

- **WHEN** a client requests a registered table by name
- **THEN** the Coordinator returns its table definition with HTTP 200

#### Scenario: Missing table

- **WHEN** a client requests a table that does not exist
- **THEN** the API returns HTTP 404

#### Scenario: Valid table registration

- **WHEN** a client submits a unique table name and valid record schema
- **THEN** the Coordinator creates the definition and returns 201 with the canonical table identifier

#### Scenario: Invalid table registration

- **WHEN** a client submits an unsupported or incomplete table definition
- **THEN** the API returns 400 with an RFC 7807 problem response

### Requirement: Record creation

The public API SHALL create a new record using its table name and partition key.

The API SHALL NOT overwrite an existing record. An attempt to create a record with an existing partition key SHALL return HTTP 409.

#### Scenario: Successful create

- **WHEN** a valid record is submitted for a registered table and unused partition key
- **THEN** the Coordinator routes it to the responsible Shard
- **AND** the API returns HTTP 201 with the created record

#### Scenario: Duplicate record

- **WHEN** a client attempts to create a record with an existing partition key
- **THEN** the API returns HTTP 409
- **AND** the existing record remains unchanged

#### Scenario: Missing table

- **WHEN** a create references an unregistered table
- **THEN** the API returns HTTP 404

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

### Requirement: Internal Shard operations

The Coordinator SHALL communicate with the responsible Shard through an internal API supporting CREATE, READ, EXISTS, and DELETE operations.

The internal API SHALL use the same table name and partition key as the public API.

#### Scenario: Internal create

- **WHEN** the Coordinator forwards a CREATE operation to the responsible Shard
- **THEN** the Shard creates the record if the partition key does not exist
- **AND** returns a conflict result if the record already exists

#### Scenario: Internal read

- **WHEN** the Coordinator forwards a READ operation to the responsible Shard
- **THEN** the Shard returns the requested record or a not-found result

#### Scenario: Internal exists

- **WHEN** the Coordinator forwards an EXISTS operation to the responsible Shard
- **THEN** the Shard returns whether the record exists

#### Scenario: Internal delete

- **WHEN** the Coordinator forwards a DELETE operation to the responsible Shard
- **THEN** the Shard deletes the record or returns a not-found result
