# Spec Delta

## Purpose

Defines the Coordinator responsibilities, operation semantics, registration behavior, and routing safety.

## ADDED Requirements

### Requirement: Coordinator is the public entry point
The Coordinator SHALL accept client API requests in single-node mode and SHALL forward key operations to exactly one responsible Shard.

#### Scenario: Single-node startup
- **WHEN** the Coordinator starts with a configured Shard registry
- **THEN** it serves the public API and uses the configured ring for routing

### Requirement: Coordinator operation support
The Coordinator SHALL implement EXISTS, CREATE, DELETE, and READ operations with table and partition-key validation.

#### Scenario: Valid operation
- **WHEN** a valid operation arrives for a registered table
- **THEN** the Coordinator routes it and returns the Shard-derived success or not-found result

### Requirement: Deterministic routing
The Coordinator SHALL route CREATE and DELETE to the same responsible Shard that READ and EXISTS use for the table and partition key.

#### Scenario: Read after write
- **WHEN** CREATE reports success for a partition key
- **THEN** a subsequent READ using the same table and partition key resolves the same ring owner

### Requirement: Shard registry
The Coordinator SHALL maintain a unique registry of registered Shards and SHALL include only registered healthy or explicitly registered members in routing decisions.

#### Scenario: Duplicate registration
- **WHEN** a Shard submits registration with an existing shard_id
- **THEN** the Coordinator refreshes that Shard entry without duplicating ring virtual nodes

### Requirement: Unavailable shard handling
The Coordinator SHALL report service unavailable when the responsible Shard cannot be reached and SHALL NOT route the operation to an arbitrary fallback Shard.

#### Scenario: Responsible shard unavailable
- **WHEN** a key maps to a reachable-ring member that fails or times out
- **THEN** the Coordinator returns 503 and records no successful mutation

### Requirement: Coordinator consistency limit
The Coordinator SHALL document that M2 provides read-after-write consistency on a successful mutation without replication or distributed transactions.

#### Scenario: Concurrent local writes
- **WHEN** concurrent writes target the same local key
- **THEN** the implementation applies a deterministic local serialization behavior and SHALL NOT claim distributed conflict resolution
