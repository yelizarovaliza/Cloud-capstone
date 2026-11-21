# Spec Delta

## Purpose

Defines consistent-hash membership and routing behavior for independent Shards.

## ADDED Requirements

### Requirement: Unique Shard identity

Every Shard SHALL provide a stable, unique `shard_id` when registering with the Coordinator at startup.

#### Scenario: Shard startup registration

- **WHEN** a Shard starts and registers with a new shard_id
- **THEN** the Coordinator adds one logical Shard and its virtual-node entries to the ring

#### Scenario: Repeated registration

- **WHEN** a Shard registers with an already registered shard_id
- **THEN** the Coordinator recognizes the existing Shard entry
- **AND** does not create duplicate virtual nodes

### Requirement: Hash ring

The ring SHALL use SHA-256 with 128 virtual nodes per Shard as the proposed M2 configuration and SHALL represent virtual-node points in a consistently ordered form.

#### Scenario: Deterministic lookup

- **WHEN** the same partition key and unchanged ring are evaluated twice
- **THEN** both evaluations return the same Shard

### Requirement: Partition key routing

The Coordinator SHALL hash the table-qualified partition key and SHALL map it to the first ring point at or after the hash in clockwise ring order.

#### Scenario: Different keys

- **WHEN** two partition keys hash to distinct ring ranges
- **THEN** lookup MAY return different Shards according to ring ownership

### Requirement: Membership updates

The Coordinator SHALL support explicit Shard addition and removal and SHALL update the ring atomically for the next routing decision.

#### Scenario: Shard addition

- **WHEN** a Shard is added
- **THEN** it owns a bounded subset of keys and no unrelated key SHALL migrate to a different Shard

#### Scenario: Shard removal

- **WHEN** a Shard is removed
- **THEN** its virtual nodes are removed and the Coordinator SHALL NOT migrate or recreate its key data automatically

### Requirement: Create-only record storage

A Shard SHALL create a record only if the partition key does not already exist.

A Shard SHALL NOT overwrite an existing record during CREATE.

#### Scenario: New record

- **WHEN** a CREATE operation targets an unused partition key
- **THEN** the Shard stores the record

#### Scenario: Existing record

- **WHEN** a CREATE operation targets an existing partition key
- **THEN** the Shard returns a conflict result
- **AND** preserves the existing record
