# ADR-004: API Protocol and Format

- **Status:** Proposed
- **Date:** 2026-11-22
- **Decision:** HTTP REST with JSON and OpenAPI 3.1

## 1. Context

Milestone 2 requires a client-facing API, table registration, CRUD operations, and Shard registration. The repository does not establish a public API technology stack.

## 2. Decision Drivers

- Familiar operational tooling and YCSB integration options.
- Explicit request and response contracts.
- Simple internal network communication.
- Strong error handling and human-readable debugging.
- Low implementation complexity for a lightweight lab system.

## 3. Alternatives Considered

### REST over HTTP with JSON

Advantages:

- Broad library and tooling support.
- OpenAPI supports generated documentation and contract tests.
- Suitable for YCSB HTTP-style adapters.

Disadvantages:

- HTTP payload overhead compared with binary protocols.
- No built-in streaming or strong binary schema evolution.

### gRPC

Advantages:

- Efficient binary transport.
- Strong protobuf contracts.

Disadvantages:

- Additional code generation and toolchain complexity.
- Less convenient for assignment-focused HTTP clients.

### GraphQL

Advantages:

- Flexible client queries.

Disadvantages:

- Mutation and record CRUD require only a small fixed API.
- Introduces schema and resolver complexity without a demonstrated benefit.

## 4. Proposed Decision

Use HTTP/JSON REST and OpenAPI 3.1 for the public API and the same protocol for private Shard registration and internal operations.

Errors should use RFC 7807 problem details. All IDs and keys should be represented as JSON strings unless a numeric type is added by a future approved contract change.

## 5. Consequences

Positive:

- A small, reviewable API contract.
- Straightforward testing and YCSB adaptation.
- Clear HTTP status codes and structured errors.

Trade-offs:

- REST cannot enforce a binary transport contract.
- Read/write behavior remains subject to network latency and application implementation.

## 6. Review Required

This decision is Proposed and requires human approval before application implementation.
