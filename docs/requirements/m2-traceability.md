# Milestone 2 Requirements Traceability

## Purpose

Maps the assignment requirements to OpenSpec specifications and future verification methods.

| Assignment requirement                             | OpenSpec specification                      | Verification method                                                                                                |
| -------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Public API for table registration                  | `openspec/changes/.../specs/kv-api/spec.md` | OpenAPI contract test and API integration test                                                                     |
| Public CREATE, READ, EXISTS, and DELETE operations | `kv-api`, `coordinator`                     | API integration tests for CREATE, READ, EXISTS, DELETE                                                             |
| Shard registration and internal operations         | `kv-api`, `coordinator`, `sharding`         | Registration and internal API integration tests                                                                    |
| Compound primary key optional                      | ADR-006, `kv-api`, `sharding`               | Verify only partition-key contract is exposed                                                                      |
| Coordinator EXISTS/CREATE/DELETE/READ              | `coordinator`                               | Handler unit tests and end-to-end API tests                                                                        |
| Coordinator hash and routing                       | `coordinator`, `sharding`                   | Ring unit tests and routing integration tests                                                                      |
| Shards register at startup                         | `coordinator`, `sharding`                   | Startup/registration integration test                                                                              |
| Consistent dynamic membership                      | `sharding`                                  | Add/remove tests with ownership stability checks                                                                   |
| Reads use write routing decision                   | `coordinator`, `sharding`                   | Same-key read-after-write routing test                                                                             |
| Terraform infrastructure                           | `m2-infrastructure`                         | `terraform fmt -check`, `terraform validate`, and `terraform plan`                                                 |
| Reuse M1 network                                   | `m2-infrastructure`, architecture doc       | Reviewed Terraform plan and network configuration                                                                  |
| CI/CD infrastructure updates                       | `m2-cicd`                                   | Pipeline run against infrastructure change                                                                         |
| CI/CD application updates                          | `m2-cicd`                                   | Pipeline run against application change                                                                            |
| Automated checks and tests                         | `m2-cicd`                                   | CI logs for unit, integration, OpenAPI, and IaC checks                                                             |
| Controlled deployment                              | `m2-cicd`                                   | Protected environment approval and deployment audit; actual deployment remains subject to permissions and approval |
| YCSB integration                                   | `m2-benchmark`                              | Successful local YCSB Load and Run using the custom Java binding                                                   |
| M2 baseline preservation                           | `m2-benchmark`                              | Recorded local baseline in `docs/testing/concurrency-and-test-behavior.md`                                         |

| API protocol ADR | ADR-004 | Human ADR approval |
| Hash and virtual-node ADR | ADR-005 | Human ADR approval and ring tests |
| Partition-key ADR | ADR-006 | Human ADR approval and contract review |
| Shard placement and traffic | `m2-infrastructure` | Terraform plan and Security Group tests |
| IAM and deployment constraints | `m2-infrastructure` | Principal review and permission evidence |
| AWS Academy and budget constraints | `m2-infrastructure`, proposal | Cost review and deployment gate |
| Shard independent execution | `coordinator`, `sharding` | Process-level integration test |
| Local key-value storage | `sharding` | Restart persistence test |
| Read-after-write consistency | `coordinator` | Integration test immediately after successful CREATE |
| Concurrency limitations | `coordinator`, design | Documented review and concurrency test |
| No replication/conflict/quorum | proposal, design, all specs | Negative scope review and implementation diff review |
| YCSB record count | `m2-benchmark` | Workload configuration review; 100 records loaded successfully |
| YCSB operation count/concurrency | `m2-benchmark` | YCSB output: 100 Load inserts; 100 Run operations; one thread |
| Throughput and latency metrics | `m2-benchmark` | Recorded Load and Run throughput and latency percentiles |
| Error rate | `m2-benchmark` | YCSB output reports 100 successful operations and zero failed operations in each phase |
| Reproducibility | `m2-benchmark`, tasks | Binding source, workload configuration, and recorded environment |
| Public API for table information retrieval | `kv-api` | API integration test for existing and missing tables |
| CREATE does not overwrite existing records | `kv-api`, `coordinator`, `sharding` | Integration test verifies HTTP 409 and unchanged existing record |
