# Milestone 2 Architecture

## 1. Status

The M2 technology stack and architecture decisions ADR-004,
ADR-005, and ADR-006 are Accepted.

The Python application has been implemented using FastAPI.
The implementation includes a Coordinator, independent Shards,
local SQLite storage, a public JSON API, internal Shard operations,
and consistent-hash routing.

The Coordinator and two Shards have been started and tested locally.
Shard registration, record creation, and read-after-write behavior
have been verified through the running application.

A custom Java YCSB binding has been implemented and used to run
Workload D locally. The Load and Run results are recorded in
`docs/testing/concurrency-and-test-behavior.md`.

AWS deployment has not been performed. Terraform plans and local
benchmark results do not constitute evidence of a live AWS deployment.

## 2. Logical Architecture

```text
Client
  |
  | HTTPS/HTTP JSON
  v
Coordinator
  +-- Table definitions
  +-- Shard registry
  +-- SHA-256 consistent-hash ring
  |
  +-- Private HTTP --> Shard 1 --> Local persistent key-value store
  +-- Private HTTP --> Shard 2 --> Local persistent key-value store
```

Milestone 2 uses one Coordinator process and at least two independent Shards. The exact runtime remains subject to ADR approval.

## 3. Public API

The public API is defined in `docs/api/openapi.yaml`.

It includes:

- `POST /v1/tables` — register a table.
- `GET /v1/tables/{tableName}` — retrieve a table definition.
- `POST /v1/tables/{tableName}/records/{partitionKey}` — create a new record.
- `GET /v1/tables/{tableName}/records/{partitionKey}` — read a record.
- `GET /v1/tables/{tableName}/records/{partitionKey}/exists` — check record existence.
- `DELETE /v1/tables/{tableName}/records/{partitionKey}` — delete a record.

CREATE does not overwrite an existing record. A duplicate CREATE returns HTTP 409.

The partition key is provided only in the URL and is not duplicated in the request body.

Shard registration is exposed on the private interface:

- `POST /v1/internal/shards/register`

The internal Shard API supports:

- `POST /v1/internal/tables/{tableName}/records/{partitionKey}` — create a record.
- `GET /v1/internal/tables/{tableName}/records/{partitionKey}` — read a record.
- `GET /v1/internal/tables/{tableName}/records/{partitionKey}/exists` — check record existence.
- `DELETE /v1/internal/tables/{tableName}/records/{partitionKey}` — delete a record.

The Coordinator forwards key operations to the responsible Shard through this internal API.

## 4. Coordinator Responsibilities

The Coordinator validates requests, registers table definitions, manages Shard membership, owns the ring, and routes operations. It does not hold authoritative local key-value data in the normal request path.

The Coordinator SHALL not silently retry against a fallback owner. A responsible Shard timeout or connection failure produces a structured unavailable response.

## 5. Shard Responsibilities

Each Shard has a stable ID and independent storage. It registers with the Coordinator, accepts only internal operations from the approved network path, and processes one local key operation at a time or with a documented local concurrency limit.

## 6. Routing

The proposed ring uses SHA-256 with 128 virtual nodes per Shard. Ring points are `<shard_id>#<virtual_node_index>`; key lookups hash the UTF-8 encoding of `<table_name>#<partition_key>`.

CREATE, READ, EXISTS, and DELETE use the same lookup algorithm. The ring can add or remove Shards. Existing data is not moved in M2.

## 7. Consistency

Successful CREATE operations are read-after-write visible through the same Coordinator and unchanged ring. M2 does not provide replication, quorum behavior, distributed transactions, or conflict resolution.

## 8. Infrastructure

The existing M1 network remains the baseline:

- VPC: `172.31.0.0/16`
- Public subnet: `172.31.80.0/20`
- Private subnet: `172.31.96.0/20`
- Region/AZ: `us-east-1` / `us-east-1a`

The M2 infrastructure has been reviewed through Terraform configuration and planning. No live AWS deployment is claimed.

The Coordinator belongs in public placement only when client access is required. Shards belong in private placement. Security Groups permit public traffic only to the Coordinator and Shard traffic only from the Coordinator.

No NAT Gateway is currently defined. Private Shards may require approved image/runtime delivery alternatives.

## 9. Budget Constraint

Three `t2.small` instances are estimated at $50.37/month compute-only, exceeding the $20 AWS Academy budget. No live deployment is approved by this document.

## 10. CI/CD

CI validates source, API contracts, tests, Docker builds, Terraform formatting, Terraform validation, and plans. Deployment requires protected approval. Terraform apply and application deployment remain blocked until permissions, principal, runtime, and budget are approved.

## 11. YCSB

A custom Java binding, `CloudCapstoneYcsbClient`, integrates YCSB
0.17.0 with the Coordinator's public HTTP API.

Workload D was executed locally with 100 records, 100 operations,
and one thread.

The Load phase completed 100 INSERT operations successfully.
The Run phase completed 95 READ and 5 INSERT operations successfully.

The measured throughput was 0.4133 ops/sec during Load and
0.4462 ops/sec during Run.

Both phases reported zero failed operations. Detailed runtime,
latency, and percentile metrics are recorded in
`docs/testing/concurrency-and-test-behavior.md`.

These measurements are a local M2 baseline, not AWS deployment
or production performance results.
