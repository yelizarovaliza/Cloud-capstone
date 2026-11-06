# Proposal: Milestone 1 – AWS Infrastructure Foundation

## Status

Accepted for repository documentation and implementation planning. This milestone is scoped to infrastructure definition, validation, and documentation only; it does not include live AWS deployment.

## Summary

Milestone 1 establishes the AWS foundation for the Cloud Capstone project using Terraform. The objective is to define and validate the minimum infrastructure required before application services are introduced in Milestone 2. The design includes an IAM stack and a network stack, with documentation for AWS Academy constraints, quota limitations, and architecture decisions.

## Completed Work

The repository already includes the following completed or validated artifacts:

- Terraform IAM stack defining:
  - custom read-oriented IAM policy
  - IAM role
  - trust relationship placeholder
  - role-policy attachment
- Terraform network stack defining:
  - VPC with CIDR `10.0.0.0/16`
  - public subnet `10.0.1.0/24`
  - private subnet `10.0.2.0/24`
  - Internet Gateway
  - route tables and subnet associations
- ADRs for:
  - IaC tool selection (Terraform)
  - Terraform stack layout
  - CIDR addressing scheme
- Documentation covering:
  - AWS Academy permissions investigation
  - AWS Service Quotas restrictions
  - IAM role analysis and policy interpretation
  - M2 architecture and budget estimate for one Coordinator and two Shards
- Terraform validation and planning performed successfully for the configured stacks

## Scope

1. IAM stack
   - Create a custom read-oriented policy for project investigation and operational review.
   - Create an IAM role with a trusted principal trust policy.
   - Attach the policy to the role.
   - Keep the trust principal as an explicit placeholder until an approved AWS principal ARN is available.

2. Network stack
   - Create a VPC in `us-east-1`.
   - Create one public subnet and one private subnet in `us-east-1a`.
   - Attach an Internet Gateway to the VPC and route public traffic through it.
   - Keep the private subnet isolated without NAT or additional compute resources at this stage.

3. Documentation and analysis
   - Record AWS Academy permission limitations and role assumptions.
   - Document the inability to access account-specific Service Quotas information.
   - Capture architecture decisions, network design constraints, and cost assumptions.

4. Validation
   - Confirm Terraform syntax validity with `terraform validate`.
   - Confirm resource planning with `terraform plan`.
   - Document the exact planned resources and the fact that no live AWS resources were created.

## Constraints and Limitations

- Region is fixed to `us-east-1`.
- VPC CIDR is fixed to `10.0.0.0/16`.
- Public subnet CIDR is fixed to `10.0.1.0/24`.
- Private subnet CIDR is fixed to `10.0.2.0/24`.
- The observed active AWS Academy role was `voclabs`; this is not assumed to be equivalent to `LabRole`.
- AWS Academy restrictions prevent reliable access to account-specific quota information.
- The IAM trust principal is a placeholder and must be replaced before any deployment is attempted.
- No AWS resources have been deployed in this milestone.
- The available AWS Academy budget is $20.
- The proposed three `t2.small` instances cost approximately $50.37/month for compute only, which exceeds the available budget if deployed continuously.

## Non-Goals and Explicitly Out of Scope

- Live deployment with `terraform apply`.
- EC2 instance launch, compute deployment, or application runtime deployment.
- Security groups, NAT Gateway, ALB, or any M2 service traffic topology.
- Production-grade multi-AZ or multi-region networking.
- Any modification of application code or business logic.
- Any claim that infrastructure is currently running in AWS.

## Architecture Overview

The Milestone 1 design is intentionally minimal and cost-conscious:

- One VPC forms the project boundary.
- One public subnet hosts resources requiring direct internet access.
- One private subnet hosts internal resources without direct internet access.
- One Internet Gateway is attached to the VPC to support public connectivity.
- Route tables separate public and private network behavior.
- No NAT Gateway is configured to reduce cost and avoid unnecessary complexity.

This design supports the planned M2 architecture of a Coordinator and two Shards, while keeping the initial foundation simple and reviewable.

## Acceptance Criteria

1. The repository contains Terraform IAM and network stacks in separate directories.
2. The stacks are documented with their intended purpose, resources, and public/private network boundaries.
3. Architecture Decision Records exist for the tool, stack structure, and CIDR strategy.
4. AWS Academy permissions and Service Quotas restrictions are documented with clear caveats.
5. Terraform configuration is validated and planned successfully without claiming any deployed AWS resources.
6. The Milestone 1 design explicitly calls out remaining work and current limitations before any live environment provisioning occurs.

## Remaining Tasks

The following tasks remain before a live deployment could be considered:

1. Replace the IAM trust principal placeholder with a valid approved principal ARN.
2. Confirm whether the AWS Academy environment permits the required IAM and EC2 operations.
3. Validate that `t2.small` instances are compatible with the account quota and availability zone constraints.
4. Reassess budget feasibility in the context of the $20 lab budget.
5. Determine whether the project can proceed to a deployment demonstration or is limited to configuration-only validation.

## Decision

Proceed with Milestone 1 as a Terraform-defined, documentation-backed infrastructure foundation that intentionally avoids live AWS deployment until the Academy permissions, trust principal, and cost constraints are resolved.
