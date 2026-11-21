# ADR-006: Partition Key Strategy

- **Status:** Proposed
- **Date:** 2026-11-22
- **Decision:** Use a single opaque partition key

## 1. Context

The assignment permits, but does not require, a compound partition/sort key. A M2 primary-key strategy must be explicit for routing and CRUD behavior.

## 2. Decision Drivers

- Minimal M2 complexity.
- Direct hash-ring mapping.
- Clear read-after-write behavior.
- Compatibility with YCSB record IDs.
- Future extension to composite keys without changing existing routing concepts.

## 3. Alternatives Considered

### Single Partition Key

Advantages:

- One hash input per record.
- No ambiguity about key ownership.
- Easy YCSB key generation.

Disadvantages:

- Multiple logical record fields cannot share a partition before a sort-key extension.

### Compound Partition and Sort Key

Advantages:

- Supports ordered groups and richer record modeling.

Disadvantages:

- Routing and CRUD semantics become more complex.
- Not required for M2.
- YCSB mapping would require an additional agreed convention.

### Full Table Record Hash

Advantages:

- Could distribute by record content.

Disadvantages:

- Updates would change routing, making reads and deletes unstable.
- Client identity would be implicit rather than explicit.

## 4. Proposed Decision

Use a caller-supplied opaque `partition_key` string as the M2 primary key. Route only by a table-qualified partition key.

The optional compound partition/sort-key model SHALL NOT be part of M2. Later milestones MAY add it through a formal contract change.

## 5. Consequences

Positive:

- Stable routing for each key across CREATE, READ, EXISTS, and DELETE.
- Straightforward YCSB record IDs.

Trade-offs:

- Sort-key grouping is unavailable.
- Key strings may expose application identifiers in logs unless logging treats them as sensitive or high-cardinality.

## 6. Review Required

This decision is Proposed and requires human approval before application implementation.
