# Proposal

## Why

Milestone 1 provides only a validated AWS network and IAM foundation. Milestone 2 needs an implementation contract for a lightweight, horizontally sharded key-value service before application or infrastructure code is added.

This proposal preserves the Milestone 1 AWS region, CIDR layout, Terraform decision, and explicit deployment limitations while defining the required Coordinator, Shards, API, routing, CI/CD, and YCSB baseline.

## What Changes

- Add a single-node Coordinator that registers Shards and routes key operations.
- Add two or more independent Shards with local key-value storage.
- Add a REST/OpenAPI client API for table registration, table information retrieval, and record operations.
- Add an internal Shard API for CREATE, READ, EXISTS, and DELETE operations, plus Shard registration.
- Add a consistent-hash ring with virtual nodes and deterministic key routing.
- Define infrastructure, security, budget, CI/CD, testing, and YCSB requirements.
- Add proposed ADR-004 through ADR-006 for review.
- Keep the change at documentation and specification stage until human review.

## Scope

### In Scope

- REST API, table and record data model, and error semantics.
- Coordinator registration, ring management, and read/write routing.
- Independent Shard storage and internal operations.
- Consistent hashing, dynamic shard membership, and routing consistency.
- Terraform scope and deployment constraints for approved environments.
- GitHub Actions or an equivalent CI/CD design.
- YCSB workloads and reproducible baseline reporting.
- Unit, integration, routing, infrastructure, and benchmark verification.

### Out of Scope

- Replication or quorum reads and writes.
- Multi-leader or leaderless behavior.
- Automatic data migration or rebalancing.
- Distributed conflict resolution.
- Production-grade multi-AZ fault tolerance.
- Automatic autoscaling.
- Application source code, Terraform resource implementation, live deployment, and AWS apply operations.

## Functional Requirements

1. The system SHALL support table registration, table information retrieval, record CRUD operations, and Shard registration.
2. The Coordinator SHALL implement EXISTS, CREATE, DELETE, and READ operations. CREATE SHALL NOT overwrite an existing record.
3. A CREATE or DELETE SHALL route using the partition key and SHALL target the same responsible Shard that a subsequent READ would select.
4. Shards SHALL register with the Coordinator at startup and SHALL expose local operations to the Coordinator through an internal API.
5. The Coordinator SHALL maintain a deterministic hash ring and SHALL not route to unregistered or unavailable Shards.
6. The infrastructure SHALL reuse the Milestone 1 VPC where approved and SHALL minimize cost.
7. CI/CD SHALL validate IaC and application changes and SHALL require explicit authorization before deployment.
8. YCSB SHALL produce a reproducible M2 baseline with throughput, average latency, p95, p99, and error rate.

## Constraints

- Milestone 1 remains unchanged.
- AWS region SHALL remain `us-east-1`.
- Reused network addresses SHALL remain `10.0.0.0/16`, `10.0.1.0/24`, and `10.0.2.0/24`.
- `voclabs` SHALL NOT be assumed equivalent to `LabRole`.
- The IAM trust principal SHALL remain unresolved until replaced with an approved ARN.
- No deployment SHALL occur unless AWS Academy permissions and the $20 budget are approved.
- No resource or benchmark result SHALL be represented as deployed or measured without evidence.

## Acceptance Criteria

1. The change contains proposal, design, tasks, and six testable capability specifications.
2. All assignment requirements are mapped to specification sections and verification methods.
3. The OpenAPI document validates and covers table registration, table retrieval, public record operations, internal Shard operations, and Shard registration.
4. ADR-004 through ADR-006 exist with Proposed status.
5. No Milestone 1 file is overwritten and no Terraform or application source code is added.
6. `openspec validate` passes for the change.

## Capabilities

### New Capabilities

- `kv-api`: REST table and record operations plus request/response contracts.
- `coordinator`: Coordinator routing, registry, local operation semantics, and Shard failure behavior.
- `sharding`: Hash ring, partition-key routing, Shard registration, and membership changes.
- `m2-infrastructure`: AWS placement, networking, IAM, security groups, and deployment constraints.
- `m2-cicd`: Validation, builds, controlled deployment, secrets, and verification.
- `m2-benchmark`: YCSB workloads, benchmark execution, metrics, and baseline publication.

### Modified Capabilities

- None.

## Impact

- Future application implementation in Python or another approved language.
- Future Docker image and container runtime configuration.
- Future Terraform networking, compute, security, and IAM resources.
- GitHub Actions or an approved CI/CD platform.
- YCSB runner and benchmark result documentation.
