# Spec Delta

## Purpose

Defines Milestone 2 infrastructure placement, network controls, IAM constraints, and deployment safety.

## ADDED Requirements

### Requirement: M1 network reuse
M2 SHALL reuse the M1 VPC and CIDR values unless a formally approved ADR changes them.

#### Scenario: Infrastructure review
- **WHEN** a Terraform plan is reviewed
- **THEN** it retains `10.0.0.0/16`, `10.0.1.0/24`, `10.0.2.0/24`, `us-east-1`, and `us-east-1a` unless an approved replacement is documented

### Requirement: Component placement
The Coordinator SHALL be client-reachable and the Shards SHALL use private placement; direct public access to Shards SHALL be denied.

#### Scenario: Placement review
- **WHEN** infrastructure rules are inspected
- **THEN** the Coordinator has the approved public endpoint and Shards have private endpoints

### Requirement: Security group isolation
Security Groups SHALL permit public API traffic only to the Coordinator and SHALL permit Shard traffic only from the Coordinator.

#### Scenario: Internal traffic
- **WHEN** the Coordinator calls a Shard
- **THEN** the matching Security Group rule permits TCP traffic on the documented internal port

#### Scenario: Unauthorized traffic
- **WHEN** a host outside the approved Coordinator Security Group calls a Shard
- **THEN** the network denies the connection

### Requirement: IAM deployment prerequisites
Infrastructure SHALL require an approved trusted principal and SHALL not use the M1 placeholder as a live trust relationship.

#### Scenario: Approval prerequisite
- **WHEN** a deployment is prepared
- **THEN** the approved role/principal and permissions are verified before apply

### Requirement: Budget gate
M2 SHALL NOT deploy a cost configuration exceeding the approved $20 AWS Academy budget without additional written budget approval.

#### Scenario: Budget review
- **WHEN** a planned configuration is evaluated
- **THEN** compute and associated cost estimates are documented and deployment is blocked if the budget or runtime window is not approved

### Requirement: Explicit deployment status
No specification SHALL state that AWS resources exist or that plans were deployed unless apply evidence is attached.

#### Scenario: Documentation update
- **WHEN** infrastructure status is reported
- **THEN** it distinguishes successful validate/plan from actual deployed resources
