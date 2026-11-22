# ADR-005: Hash Function and Virtual Nodes

- **Status:** Accepted
- **Date:** 2026-11-22
- **Decision:** SHA-256 and 128 virtual nodes per Shard

## 1. Context

The Coordinator must deterministically route keys to registered Shards and support dynamic shard membership.

## 2. Decision Drivers

- Deterministic, reproducible routing.
- Low implementation complexity.
- Bounded key redistribution when membership changes.
- Transparent ring representation.
- Hardware-neutral hash behavior.

## 3. Alternatives Considered

### SHA-256 with Virtual Nodes

Advantages:

- Widely available and deterministic.
- Virtual nodes support more even key ownership.
- Ring behavior is easy to test and document.

Disadvantages:

- Slower than simple non-cryptographic hashes for very large workloads.
- 128 nodes per Shard increases ring entries and lookup memory modestly.

### MD5 or CRC32

Advantages:

- Fast and simple.

Disadvantages:

- CRC32 is not intended for even distribution across arbitrary keys.
- MD5 is cryptographically weak and unnecessary for this use.

### Rendezvous Hashing

Advantages:

- No virtual ring representation.
- Strong natural key redistribution behavior.

Disadvantages:

- Does not directly implement the assignment's consistent-hashing ring model.
- The repository has no existing rendezvous implementation or tooling.

## 4. Proposed Decision

Use SHA-256 over the virtual-node token `<shard_id>#<virtual_node_index>` for ring points and over the table-qualified partition key for key lookup.

Use 128 virtual nodes per Shard. Lookups shall return the first ring point at or after the key hash in clockwise unsigned-byte order.

## 5. Consequences

Positive:

- Deterministic routing independent of process order.
- Adding or removing a Shard affects only a bounded ring range.

Trade-offs:

- Existing data is not migrated.
- Virtual-node count is tunable but changing it changes future routing.
