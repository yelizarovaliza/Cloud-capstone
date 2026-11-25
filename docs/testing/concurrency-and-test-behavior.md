# Concurrency Limitations and Test Behavior

## 1. Scope

Milestone 2 provides basic concurrency handling for independent Shards and their local SQLite storage.

The implementation does not provide distributed transactions, replication, consensus, or global synchronization across Shards.

Concurrency guarantees are limited to individual operations performed by the current Coordinator and the responsible Shard.

## 2. SQLite Storage

Each Shard owns an independent SQLite database.

The `SQLiteRecordStore` implementation:

- Opens a separate SQLite connection for each storage operation.
- Uses a connection timeout of 5 seconds.
- Configures `PRAGMA busy_timeout = 5000`.
- Uses SQLite transactions for write operations.
- Defines `(table_name, partition_key)` as the composite primary key.

### Concurrent CREATE requests

SQLite's primary-key constraint prevents two records with the same table name and partition key from being stored simultaneously.

If concurrent requests attempt to create the same record:

- One request can successfully insert the record.
- A subsequent conflicting insert is rejected by SQLite.
- The application maps the uniqueness violation to `RecordAlreadyExistsError`, which the API exposes as HTTP 409.

The existing record is not overwritten.

The implementation does not guarantee that every concurrent request completes without database contention. SQLite may wait for a database lock, and an operation can still fail if the lock cannot be acquired within the configured timeout.

## 3. Coordinator and Registry Limitations

### Shard registry

`ShardRegistry` uses a reentrant lock (`RLock`) to synchronize registration, lookup, retrieval of all registrations, and clearing the registry.

### Shard routing

`ShardRouter` uses an `RLock` when checking and rebuilding its consistent-hash ring.

The router obtains a snapshot of registered Shards and uses the current ring membership to resolve the responsible Shard.

Membership changes affect future routing decisions. They do not automatically migrate existing records.

### Table registry

`TableRegistry` currently uses an in-memory dictionary without an explicit synchronization lock.

Concurrent table registration is therefore not guaranteed to be thread-safe.

Table definitions are also not persisted: they exist only in the Coordinator's process memory.

### Multi-operation consistency

CREATE, READ, EXISTS, and DELETE are separate API operations.

The implementation does not provide a transaction spanning multiple requests. A sequence of operations can therefore observe changes made by other requests between operations.

The system does not implement distributed locking or conflict resolution.

## 4. Failure and Membership Behavior

If the responsible Shard is unavailable, the Coordinator returns HTTP 503.

The Coordinator does not silently select another Shard as a fallback.

Adding or removing a Shard changes the hash-ring mapping for affected keys. Existing data is not automatically transferred to the new owner.

Consequently, a key whose owner changes after a membership update may no longer be available through the new routing assignment. Automatic data migration is outside the M2 scope.

## 5. Test Behavior

The M2 test suite verifies the following behavior:

| Test area               | Verified behavior                                                             |
| ----------------------- | ----------------------------------------------------------------------------- |
| Table registry          | Registration, retrieval, duplicate registration, and missing tables           |
| Record validation       | Valid and invalid record requests                                             |
| Record operations       | CREATE, READ, EXISTS, DELETE, and missing records                             |
| Create-only behavior    | Duplicate CREATE returns a conflict and does not overwrite data               |
| SQLite storage          | Persistence, table-qualified keys, and CRUD behavior                          |
| Consistent hashing      | Deterministic ownership, virtual nodes, and ring membership                   |
| Key movement            | Adding or removing a Shard only changes ownership in the affected ring ranges |
| Shard registration      | Startup registration and repeated registration                                |
| Distributed integration | Registration, routing, and read-after-write behavior                          |
| Shard unavailability    | HTTP 503 without fallback routing                                             |

### Integration test limitations

Integration tests use FastAPI `TestClient` and an HTTPX mock transport to simulate communication between the Coordinator and Shards.

The tests verify application-level request routing and error handling without requiring deployed infrastructure or live network connections.

The unavailable-Shard scenario is simulated by raising an HTTP connection error for the selected Shard.

The current integration tests execute requests sequentially. They do not constitute a concurrent load test and do not measure throughput, contention, or race-condition behavior under parallel requests.

## 6. YCSB Benchmark Results

### Benchmark environment

The M2 YCSB benchmark was executed locally against the Python FastAPI Coordinator and two independently running Shards.

| Parameter            | Value                                 |
| -------------------- | ------------------------------------- |
| Benchmark            | Yahoo! Cloud Serving Benchmark (YCSB) |
| YCSB version         | 0.17.0                                |
| Binding              | Custom Java `CloudCapstoneYcsbClient` |
| Workload             | Workload D                            |
| Record count         | 100                                   |
| Operation count      | 100                                   |
| Thread count         | 1                                     |
| Request distribution | `latest`                              |
| Coordinator          | `http://localhost:8000`               |
| Shard 1              | `http://localhost:8001`               |
| Shard 2              | `http://localhost:8002`               |

### Load phase

The Load phase inserted 100 records.

| Metric                  |         Result |
| ----------------------- | -------------: |
| Operations              |     100 INSERT |
| Successful operations   |            100 |
| Failed operations       |              0 |
| Runtime                 |     241,940 ms |
| Throughput              | 0.4133 ops/sec |
| Average latency         |    2,416.49 ms |
| Minimum latency         |    2,199.55 ms |
| Maximum latency         |   18,120.70 ms |
| 95th percentile latency |    2,328.58 ms |
| 99th percentile latency |    2,512.90 ms |

### Run phase

The Run phase executed 100 operations: 95 READ operations and 5 INSERT operations.

| Metric                  |        READ |      INSERT |
| ----------------------- | ----------: | ----------: |
| Operations              |          95 |           5 |
| Successful operations   |          95 |           5 |
| Failed operations       |           0 |           0 |
| Average latency         | 2,236.71 ms | 2,261.20 ms |
| Minimum latency         | 2,195.46 ms | 2,244.61 ms |
| Maximum latency         | 2,326.53 ms | 2,279.42 ms |
| 95th percentile latency | 2,275.33 ms | 2,279.42 ms |
| 99th percentile latency | 2,295.81 ms | 2,279.42 ms |

Overall Run metrics:

- Runtime: 224,121 ms.
- Throughput: 0.4462 ops/sec.
- Total successful operations: 100.
- Failed operations: 0.

### Interpretation and limitations

Both phases completed with 100% successful operations in the reported YCSB output.

The measured throughput was approximately 0.41 ops/sec during Load and 0.45 ops/sec during Run. The observed average operation latency was approximately 2.2–2.4 seconds.

These results represent a local baseline for the tested configuration. They are not AWS deployment measurements and should not be interpreted as production performance guarantees.

The benchmark used one thread. It therefore measures sequential request behavior and does not establish concurrent-load performance, contention limits, or race-condition guarantees.

The results can serve as a reference point for later milestone comparisons. Performance changes should be evaluated using the same workload and comparable environment.

## 7. Explicitly Out of Scope

The following guarantees are not implemented or claimed in M2:

- Distributed transactions across Shards.
- Atomicity across multiple API requests.
- Replication or quorum-based consistency.
- Automatic conflict resolution.
- Global synchronization across Coordinator and Shards.
- Automatic data migration after membership changes.
- Production-grade concurrent load guarantees.

These capabilities may be evaluated in later milestones if required by the approved architecture.

## 8. Conclusion

M2 provides deterministic key routing, local SQLite persistence, protection against duplicate record creation, and explicit handling of unavailable Shards.

The current tests verify these implemented behaviors. They do not establish production-grade concurrency guarantees or distributed fault tolerance.
