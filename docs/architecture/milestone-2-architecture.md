# Milestone 2 Architecture

## 1. Status

The M2 technology stack and architecture decisions ADR-004,
ADR-005, and ADR-006 are Accepted.

The initial Python application scaffold has been created
with FastAPI and a basic health-check endpoint.

The Coordinator, Shards, key-value operations, and M2 AWS
resources have not yet been implemented or deployed.

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

- VPC: `10.0.0.0/16`
- Public subnet: `10.0.1.0/24`
- Private subnet: `10.0.2.0/24`
- Region/AZ: `us-east-1` / `us-east-1a`

The Coordinator belongs in public placement only when client access is required. Shards belong in private placement. Security Groups permit public traffic only to the Coordinator and Shard traffic only from the Coordinator.

No NAT Gateway is currently defined. Private Shards may require approved image/runtime delivery alternatives.

## 9. Budget Constraint

Three `t2.small` instances are estimated at $50.37/month compute-only, exceeding the $20 AWS Academy budget. No live deployment is approved by this document.

## 10. CI/CD

CI validates source, API contracts, tests, Docker builds, Terraform formatting, Terraform validation, and plans. Deployment requires protected approval. Terraform apply and application deployment remain blocked until permissions, principal, runtime, and budget are approved.

## 11. YCSB

YCSB integration is a future implementation task. The baseline report shall record workload, data size, operations, concurrency, throughput, average/p95/p99 latency, error rate, and environment. No baseline value is claimed until measured.
