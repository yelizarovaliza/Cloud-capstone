# Spec Delta

## Purpose

Defines automated validation, application build, controlled deployment, and verification for Milestone 2.

## ADDED Requirements

### Requirement: Continuous integration checks
CI SHALL run repository formatting, unit tests, integration tests, OpenAPI validation, Docker build, Terraform formatting, Terraform validate, and Terraform plan.

#### Scenario: Pull request validation
- **WHEN** application, OpenAPI, or infrastructure changes are submitted
- **THEN** CI reports pass or fail for every applicable check

### Requirement: Terraform plan artifacts
CI SHALL retain Terraform plans for review but SHALL NOT expose credentials or sensitive state in logs or repository files.

#### Scenario: Plan review
- **WHEN** infrastructure CI completes
- **THEN** an approved reviewer can inspect the plan and proposed resources

### Requirement: Controlled deployment
Application and infrastructure deployment SHALL require explicit protected-environment approval and SHALL remain separate where practical.

#### Scenario: Manual approval
- **WHEN** CI reaches deployment
- **THEN** deployment waits for an authorized reviewer

### Requirement: Secrets management
The pipeline SHALL retrieve AWS credentials and registry credentials only from approved secret storage and SHALL use least-available scopes.

#### Scenario: Secret scan
- **WHEN** source and pipeline configuration are scanned
- **THEN** no credential, token, or private key is present

### Requirement: Deployment verification
A deployment SHALL report success only after health checks and read-after-write smoke tests pass.

#### Scenario: Failed verification
- **WHEN** health or smoke verification fails
- **THEN** CI marks deployment failed and triggers the documented rollback or stop procedure
