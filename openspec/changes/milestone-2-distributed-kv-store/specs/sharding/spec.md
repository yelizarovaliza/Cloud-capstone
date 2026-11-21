# Spec Delta

## Purpose

Defines consistent-hash membership and routing behavior for independent Shards.

## ADDED Requirements

### Requirement: Unique Shard identity
Every Shard SHALL provide a stable, unique `shard_id` during registration and local startup.

#### Scenario: Unique registration
- **WHEN** a Shard starts and registers with a new shard_id
- **THEN** the Coordinator adds one logical Shard and its virtual-node entries to the ring

#### Scenario: Repeated registration
- **WHEN** a Shard re-registers with the same stable shard_id
- **THEN** the Coordinator refreshes its endpoint without changing virtual-node identity

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

### Requirement: Local Shard storage
Each Shard SHALL maintain independent local storage and SHALL accept internal CREATE, READ, EXISTS, and DELETE operations from the Coordinator only on the approved private interface.

#### Scenario: Local operation
- **WHEN** the Coordinator sends an internal operation for a key owned by that Shard
- **THEN** the Shard updates or reads only its local store

#### Scenario: Wrong-owner operation
- **WHEN** a Shard receives an operation for a key outside its computed ownership
- **THEN** it SHALL return an ownership error rather than storing or serving the key
