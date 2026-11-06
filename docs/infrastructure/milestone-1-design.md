# Milestone 1 Design Document

## 1. Purpose

This document describes the Milestone 1 AWS infrastructure foundation for the Cloud Capstone project. The objective is to define a minimal, reviewable, and reproducible AWS base layer before application services are added in Milestone 2.

## 2. Design Goals

- Keep the initial design simple and budget-aware.
- Use Terraform as the single infrastructure-as-code tool.
- Separate IAM and network responsibilities into distinct stacks.
- Use a public/private subnet model to support the planned Coordinator and Shards topology.
- Document the constraints and limitations of the AWS Academy lab environment.

## 3. Constraints

- AWS region: `us-east-1`
- VPC CIDR: `10.0.0.0/16`
- Public subnet: `10.0.1.0/24`
- Private subnet: `10.0.2.0/24`
- Availability Zone: `us-east-1a`
- Current Academy role observed: `voclabs`
- IAM trust principal is a placeholder and is not deployable as-is.
- No live AWS deployment has occurred.

## 4. Proposed Architecture

```text
VPC: 10.0.0.0/16
├── Public subnet: 10.0.1.0/24
│   └── Internet Gateway route to 0.0.0.0/0
│
├── Private subnet: 10.0.2.0/24
│   └── No direct Internet Gateway or NAT route
│
└── Route tables
    ├── Public route table
    └── Private route table
```

## 5. Component Summary

### IAM Stack

The IAM stack contains a custom policy and role intended to support project investigation and read-oriented access. The role is configured to trust an external principal ARN that must be replaced before deployment.

The current configuration includes:

- `aws_iam_policy.project_read_only`
- `aws_iam_role.project_read_only_role`
- `aws_iam_role_policy_attachment.project_read_only_attachment`

### Network Stack

The network stack contains the base VPC networking needed for future application resources. The design includes:

- `aws_vpc.main`
- `aws_subnet.public`
- `aws_subnet.private`
- `aws_internet_gateway.main`
- `aws_route_table.public`
- `aws_route_table.private`
- `aws_route_table_association.public`
- `aws_route_table_association.private`

## 6. M2 Application Context

The proposed application footprint for Milestone 2 is:

- 1 Coordinator instance
- 2 Shard instances
- Coordinator in the public subnet
- Shards in the private subnet

The design intentionally keeps public and private communication boundaries clear while not deploying any compute resources in Milestone 1.

## 7. Cost and Quota Considerations

The project budget is capped at approximately $20 for the AWS Academy environment. The compute-only cost for three `t2.small` instances is approximately $50.37/month in `us-east-1`.

This does not meet the current budget expectation, and no deployment should be attempted until the funding and quota constraints are reviewed. In addition, account-specific quota data was not accessible from the current AWS Academy account, so the design remains constrained to documented defaults rather than confirmed account values.

## 8. Validation Status

Terraform configuration and planning were validated successfully for the repository state as of this milestone. However, the validation is limited to configuration correctness and execution planning; it does not indicate that any AWS resources were created.

## 9. Outstanding Decisions

Before any live deployment, the following decisions must be resolved:

- replacement of the IAM trust principal placeholder
- confirmation of required AWS Academy permissions
- review of Service Quotas and region availability
- confirmation of budget alignment with the lab allocation
- decision whether deployment demonstration is allowed under current restrictions

## 10. Design Conclusion

Milestone 1 is a documentation-first infrastructure foundation. It is intentionally conservative, cost-aware, and limited to Terraform configuration and validation while the project confirms the AWS Academy environment is able to support live deployment.
