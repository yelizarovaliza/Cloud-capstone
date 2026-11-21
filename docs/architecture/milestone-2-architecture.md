# Milestone 2 Architecture

## 1. Status

Proposed. No application code or AWS M2 resources have been implemented or deployed.

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

- `POST /v1/tables`
- `PUT /v1/tables/{tableName}/records/{partitionKey}`
- `GET /v1/tables/{tableName}/records/{partitionKey}`
- `GET /v1/tables/{tableName}/records/{partitionKey}/exists`
- `DELETE /v1/tables/{tableName}/records/{partitionKey}`

Shard registration is exposed on the private interface:

- `POST /v1/internal/shards/register`

## 4. Coordinator Responsibilities

The Coordinator validates requests, registers table definitions, manages Shard membership, owns the ring, and routes operations. It does not hold authoritative local key-value data in the normal request path.

The Coordinator SHALL not silently retry against a fallback owner. A responsible Shard timeout or connection failure produces a structured unavailable response.

## 5. Shard Responsibilities

Each Shard has a stable ID and independent storage. It registers with the Coordinator, accepts only internal operations from the approved network path, and processes one local key operation at a time or with a documented local concurrency limit.

## 6. Routing

The proposed ring uses SHA-256 with 128 virtual nodes per Shard. Ring points are `<shard_id>#<virtual_node_index>`; key lookups use the table-qualified partition key.

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
