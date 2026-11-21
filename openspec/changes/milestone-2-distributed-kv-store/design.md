# Design

## Context

Milestone 1 established Terraform, separate IAM and Network stacks, `us-east-1`, and the existing VPC/subnet addressing. It did not create live resources or establish an application stack. M2 therefore begins with proposed application choices and must remain executable in an approved, potentially cost-constrained environment.

## Goals / Non-Goals

**Goals:**

- Specify one Coordinator and at least two independently running Shards.
- Provide deterministic routing for every supported key operation.
- Keep the M2 consistency model explicit and limited to per-key routing consistency.
- Reuse the M1 network baseline and preserve deployment safety.
- Produce repeatable tests and YCSB baseline evidence.

**Non-Goals:**

- Data replication or shard-level availability guarantees.
- Automatic migration or rebalancing.
- Quorums, consensus, or distributed conflict resolution.
- Production multi-AZ deployment or autoscaling.

## Proposed Architecture

```text
Client -> Public Coordinator API
               |
               +-> Shard Registry
               +-> Consistent Hash Ring
               |
               +-> Shard 1 internal API
               +-> Shard 2 internal API
```

The proposed implementation uses FastAPI/Python with Pydantic and SQLite-compatible local file storage, because the repository establishes no application stack. These choices are recommendations in Proposed ADR-004/005/006 and must be approved before implementation.

## Decisions

### REST and OpenAPI

The proposed public protocol is HTTP/JSON and OpenAPI 3.1. The Shard registration and internal operations use the same protocol with private network-only paths.

Alternative: gRPC offers stronger contracts but adds implementation and tooling complexity. GraphQL is unnecessary for a small CRUD data model.

### Partition Key

The proposed primary key is a caller-supplied opaque `partition_key`. A compound partition/sort key is not required in M2 and MAY be added in a later milestone.

### Consistent Hashing

The proposed ring uses SHA-256 and 128 virtual nodes per Shard. The ring key is `<shard_id>#<virtual_node_index>` and the lookup key is the UTF-8 partition key.

Alternatives: MD5 is faster but weaker and not appropriate as a cryptographic choice; Rendezvous hashing avoids a ring but would not demonstrate the assignment's ring concept.

### Storage

Each Shard SHALL own an independent local key-value store. The proposed M2 implementation is SQLite for local persistence with one logical table and serialized access. The choice does not imply replication or distributed transactions.

Alternatives: in-memory storage is simpler but loses data across restarts; Redis adds an extra service and cost. SQLite is a low-cost single-process implementation if each Shard is one process.

### Deployment

The proposed physical placement is one public Coordinator and two private Shards on low-cost EC2 instances or one approved lab-compatible host arrangement. Docker Compose MAY run all processes on one lab host for functional testing, while the IaC specification SHALL also support separate instances.

The initial three-t2.small layout is $50.37/month compute-only and exceeds the $20 budget. Therefore, deployment SHALL remain blocked until an approved alternative, shortened lab run, or additional budget is documented.

## Data Flow

### CREATE

1. The Coordinator validates the table and record.
2. It applies the table record schema.
3. It hashes the partition key.
4. It selects the responsible Shard.
5. It forwards the CREATE to that Shard.
6. It returns the successful result or a structured service error.

### READ / EXISTS / DELETE

These operations use the same partition-key hash and owner lookup as CREATE. DELETE SHALL target the same owner. EXISTS SHALL report presence only for local storage on the selected Shard.

## Registration

A Shard SHALL send a registration request with a stable `shard_id`, base URL, and optional heartbeat metadata. The Coordinator SHALL validate uniqueness and membership, add virtual nodes, and return the effective ring configuration.

Re-registering the same shard SHALL refresh its record but SHALL NOT create duplicate ring entries. Removal SHALL occur through an explicit deregistration operation or heartbeat expiry if implemented and reviewed; M2 SHALL not infer automatic migration.

## Consistency and Failure

M2 provides routing consistency, not replicated consistency:

- A CREATE SHALL complete before the Coordinator reports success.
- A successful CREATE SHALL be immediately readable through the same Coordinator and ring.
- Shard process restarts SHALL preserve local data only if persistence survives.
- The system SHALL report an unavailable responsible Shard and SHALL NOT silently route to another Shard.
- Membership changes SHALL alter future routing but SHALL not move existing data automatically.

## CI/CD

CI SHALL run formatting, unit tests, OpenAPI validation, Terraform formatting and validate, Terraform plan, Docker builds, and integration tests. Deployment SHALL remain manual or require protected approval. Secrets SHALL come from CI secret storage or AWS-issued credentials, never source files.

## Benchmark

A YCSB adapter SHALL expose CREATE/READ/EXISTS/DELETE through one table. M2 SHALL run 1M baseline records where resources permit and retain measured operation count, concurrency, throughput, average latency, p95, p99, and error rate. The benchmark SHALL record instance sizing and environment even if live AWS execution is unavailable.

## Risks / Trade-offs

- [Budget overrun] → Prevent apply and use the smallest approved or local test setup.
- [No NAT gateway] → Shards SHALL receive no public route; private deployment requires access or a public image registry proxy approved for the environment.
- [No migration] → Document key remapping after membership changes.
- [Lab permission denied] → Keep deployment tasks blocked and preserve validation evidence.
- [No replication] → Report shard loss as unavailable data and prohibit strong-consistency claims.
- [One AZ] → Label availability as non-production.
