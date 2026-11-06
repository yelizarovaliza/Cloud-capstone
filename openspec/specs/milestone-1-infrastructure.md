# OpenSpec Specification: Milestone 1 – AWS Infrastructure Foundation

## Objective

Establish the minimum AWS infrastructure foundation required for the Cloud Capstone project. This milestone is intentionally limited to infrastructure definition, validation, and documentation.

## Functional Requirements

1. The project must define a Terraform IAM stack.
   - Include one custom, read-oriented IAM policy.
   - Include one IAM role.
   - Include a trust relationship using an approved principal ARN placeholder.
   - Attach the policy to the role.

2. The project must define a Terraform network stack.
   - Create a VPC using `10.0.0.0/16`.
   - Create one public subnet using `10.0.1.0/24`.
   - Create one private subnet using `10.0.2.0/24`.
   - Use `us-east-1` and `us-east-1a` as the fixed region and AZ.
   - Create an Internet Gateway and public route table.
   - Keep the private subnet isolated without a NAT Gateway in this phase.

3. The repository must document the AWS Academy operational environment.
   - Active role observed: `voclabs`.
   - Do not assume this is equivalent to `LabRole`.
   - Explain the limits of lab permissions and role assumptions.

4. The repository must document Service Quotas limitations.
   - Capture the inability to access account-specific quota information.
   - Record published default values without claiming account verification.

5. The project must include decision records for:
   - IaC tool selection
   - Terraform stack layout
   - CIDR addressing

6. The project must include the M2 architecture and budget estimate.
   - The design must account for one Coordinator and two Shards.
   - The estimate must document the compute-only cost of `t2.small` instances.

7. The repository must capture the current validation status.
   - Terraform configuration must be validated and planned successfully.
   - Documentation must explicitly state that no AWS resources have been deployed.

## Non-Functional Requirements

- The infrastructure remains intentionally minimal and low-cost.
- The design must be reviewable without requiring production-grade AWS permissions.
- All documentation must avoid claiming successful live AWS deployment.
- The implementation must remain within the scope of documentation and Terraform configuration before any real environment provisioning.

## Design Constraints

- Region: `us-east-1`
- VPC: `10.0.0.0/16`
- Public subnet: `10.0.1.0/24`
- Private subnet: `10.0.2.0/24`
- No NAT Gateway in the foundation design.
- No application resources or compute services are part of this milestone. 
- The trust relationship principal is currently a placeholder.

## Validation Checklist

- [x] Terraform IAM configuration exists.
- [x] Terraform network configuration exists.
- [x] `terraform validate` has been documented as successful.
- [x] `terraform plan` has been documented as successful.
- [x] AWS Academy constraints are documented.
- [x] Service Quotas limitations are documented.
- [x] ADRs exist for tool selection, stack layout, and CIDR design.
- [x] Cost estimate and M2 architecture notes are included.
- [x] No live deployment is claimed.

## Implementation Task Checklist

- [x] Review the current repository structure and infrastructure definitions.
- [x] Inspect Terraform IAM and network stacks.
- [x] Review AWS Academy permission and quota analysis documentation.
- [x] Review architecture decision records and network design details.
- [x] Capture M2 architecture and cost estimate assumptions.
- [x] Draft the Milestone 1 OpenSpec proposal.
- [ ] Replace the IAM trust principal placeholder with an approved ARN before any deployment attempt.
- [ ] Confirm the AWS Academy environment permits the required IAM and EC2 actions.
- [ ] Verify that EC2 instance quota and AZ availability are compatible with the planned `t2.small` design.
- [ ] Reassess cost feasibility against the $20 lab budget before attempting any deployment demonstration.
- [ ] Decide whether to complete a deployment demonstration or keep Milestone 1 purely at the validated configuration stage.

## Risks and Open Issues

- AWS Academy permissions may not permit the required actions for live deployment.
- Service quota data is not accessible from the current account.
- The funding ceiling may prevent continuous use of the projected three-instance architecture.
- The IAM trust policy must be corrected before any real-world use.

## Definition of Done

Milestone 1 is complete for documentation and design validation when the repository consistently documents the Terraform IAM and network foundation, the AWS Academy limitations, the pricing and capacity concerns, and the fact that no live deployment has occurred to date.
