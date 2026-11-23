# ADR-007: Reuse of the AWS Academy Default VPC

- **Status:** Proposed
- **Date:** 2026-11-23
- **Decision:** Reuse the existing AWS Academy Default VPC for M2 deployment.

## 1. Context

The M1 network design specified a dedicated VPC with CIDR
10.0.0.0/16 and separate public and private subnets.

The M1 network was not deployed in the AWS Academy environment.
The current AWS Academy account provides an existing Default VPC
with CIDR 172.31.0.0/16 and six default public subnets.

Creating a separate VPC would duplicate network infrastructure
and introduce additional permission and deployment requirements.

## 2. Decision Drivers

- Compatibility with AWS Academy sandbox restrictions.
- Reuse of existing network resources.
- Avoidance of unnecessary infrastructure costs.
- Separation of public Coordinator and private Shards.
- Minimal changes to the existing M1 architecture.

## 3. Decision

For Milestone 2, reuse the existing Default VPC:

- Coordinator API: TCP 8000.
- Shard internal APIs: TCP 8001–8002.
- VPC: `vpc-0d83c8e68a98370e1`
- VPC CIDR: `172.31.0.0/16`
- Region: `us-east-1`

Use the existing public subnet in `us-east-1a`:

- Subnet: `subnet-0af45210ea4706e53`
- CIDR: `172.31.80.0/20`

Create one private subnet for both Shards:

- CIDR: `172.31.96.0/20`
- Availability Zone: `us-east-1a`
- Public IP assignment: disabled

The private subnet will use a dedicated route table
without an Internet Gateway default route.

The Coordinator will use a public-facing Security Group.
Shard inbound traffic will be restricted to the Coordinator
Security Group.

## 4. Alternatives Considered

### Dedicated VPC from M1

Advantages:

- Full control over network configuration.
- Independent project network.

Disadvantages:

- Requires creating additional infrastructure.
- May encounter AWS Academy permission restrictions.
- Duplicates the available Default VPC.

### Reuse Default VPC

Advantages:

- Uses existing infrastructure.
- Avoids creating another VPC and Internet Gateway.
- Reduces deployment complexity.

Disadvantages:

- Uses the Academy-provided address range.
- Shares the VPC with the sandbox environment.
- Requires careful Security Group isolation.

## 5. Consequences

- ADR-003 remains as the historical M1 CIDR decision.
- This ADR supersedes the M1 network addressing decision
  for the M2 AWS Academy deployment only.
- The private Shards have no direct Internet route.
- Deployment remains subject to IAM permissions and budget approval.
- No resources are considered deployed until Terraform apply
  is explicitly approved and verified.
