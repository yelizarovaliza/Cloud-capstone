# Tasks

## 1. Application and API Foundation

- [x] 1.1 Approve Python/FastAPI, SQLite, REST/OpenAPI, SHA-256, and partition-key ADR decisions; verify the three ADR statuses are Proposed or Accepted by review.
- [x] 1.2 Implement table registration, table retrieval, and record validation; verify valid, invalid, existing, and missing table scenarios.
- [x] 1.3 Implement CREATE, READ, EXISTS, and DELETE Coordinator handlers; verify successful operations, missing records, and duplicate CREATE conflicts.
- [x] 1.4 Generate or align runtime API behavior with `docs/api/openapi.yaml`; verify a contract test passes.

## 2. Coordinator and Sharding

- [x] 2.1 Implement the Shard registry and startup registration; verify registration and repeated registration with the same shard_id.
- [x] 2.2 Implement SHA-256 consistent-hash ring with configurable virtual-node count; verify deterministic mapping and ring tests.
- [x] 2.3 Route CREATE, READ, EXISTS, and DELETE using the partition key; verify cross-component tests prove identical owner selection.
- [x] 2.4 Implement unavailable-shard handling; verify requests fail with the specified 503-style error and no fallback owner is used.
- [ ] 2.5 Implement the Shard internal API for CREATE, READ, EXISTS, and DELETE, together with local persistence; verify internal operations and read-after-write behavior.

## 3. Testing and Data Guarantees

- [ ] 3.1 Add unit tests for table registration, table retrieval, record validation, create-only behavior, and key-value operations; verify the test suite passes.
- [ ] 3.2 Add ring tests for add/remove membership and key movement; verify existing shard ownership remains stable except for the affected ring range.
- [ ] 3.3 Add integration tests for registration, routing, read-after-write, and unavailable Shards; verify no data is silently rerouted.
- [ ] 3.4 Document concurrency limitations and test behavior; verify the documentation matches implemented guarantees.

## 4. Infrastructure

- [ ] 4.1 Resolve IAM trust principal and AWS Academy permission blockers; verify deployment prerequisites are documented and approved.
- [ ] 4.2 Extend Terraform from the M1 network foundation; verify `terraform fmt -check` and `terraform validate` pass.
- [ ] 4.3 Define Security Groups and instance placement; verify `terraform plan` shows only approved public and private traffic.
- [ ] 4.4 Run cost and availability checks; verify deployment is blocked until the approved budget alternative is within $20 or additional approval exists.
- [ ] 4.5 Do not run `terraform apply` until approval; verify post-review evidence is required before any deployment task is closed.

## 5. CI/CD

- [ ] 5.1 Create CI stages for format, tests, OpenAPI validation, and Docker build; verify pull requests receive automated results.
- [ ] 5.2 Add Terraform formatting and validation plus plan artifacts; verify generated plans contain no sensitive state or credentials.
- [ ] 5.3 Add protected deployment stages and secret handling; verify deployment requires approval and no secret exists in repository files.
- [ ] 5.4 Add deployment verification; verify health and smoke tests are required before the pipeline reports success.

## 6. YCSB Benchmark

- [ ] 6.1 Implement or configure YCSB binding for the public API; verify smoke workloads execute without transport errors.
- [ ] 6.2 Select and document workload, record count, operation count, and concurrency; verify a benchmark configuration file or command reproduces the run.
- [ ] 6.3 Execute the approved benchmark; verify throughput, average, p95, p99, and error-rate metrics are recorded.
- [ ] 6.4 Publish the baseline report and environment metadata; verify values are marked measured or not measured, with no invented results.

## 7. Architecture and Traceability

- [ ] 7.1 Complete architecture documentation and diagrams; verify component placement and traffic directions match specifications.
- [ ] 7.2 Complete requirement traceability; verify every assignment item maps to a spec and verification method.
- [ ] 7.3 Review M2 for conflicts with M3-M5; verify no spec claims replication, rebalancing, consensus, or other later-milestone behavior.
- [ ] 7.4 Run final OpenSpec validation; verify `openspec validate milestone-2-distributed-kv-store --strict` passes or report the exact unresolved warning.

## Workflow follow-up

- Wait for human review of ADR-004 through ADR-006 and unresolved infrastructure decisions.
- Archive this change only after review and implementation according to repository governance.
