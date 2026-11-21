# Spec Delta

## Purpose

Defines YCSB workload selection and the reproducible Milestone 2 baseline metrics.

## ADDED Requirements

### Requirement: YCSB integration
The project SHALL provide a YCSB-compatible binding or adapter that invokes the public API or an approved YCSB-supported interface.

#### Scenario: Client smoke run
- **WHEN** YCSB loads a small record count
- **THEN** CREATE and READ operations complete without transport or protocol errors

### Requirement: Workload documentation
The benchmark SHALL record workload class, read/write proportions, record count, operation count, and concurrency.

#### Scenario: Reproducible configuration
- **WHEN** the documented configuration is reused
- **THEN** the runner can start the same logical workload with the same data size and concurrency

### Requirement: Baseline metrics
The M2 baseline SHALL preserve throughput, average latency, p95 latency, p99 latency, and error rate.

#### Scenario: Completed benchmark
- **WHEN** YCSB reports a benchmark run
- **THEN** all required metrics and run metadata are written to the baseline report

### Requirement: Environment metadata
The benchmark report SHALL record region, deployment mode, instance or host sizing, service versions, date, and run identifier.

#### Scenario: Report review
- **WHEN** a later milestone compares against M2
- **THEN** it can identify whether hardware and workload conditions are comparable

### Requirement: Evidence labeling
The benchmark SHALL label metrics as measured or not measured and SHALL NOT invent AWS or performance results.

#### Scenario: No live execution
- **WHEN** AWS deployment or YCSB execution is blocked
- **THEN** the report records no measured baseline and documents the blocker
