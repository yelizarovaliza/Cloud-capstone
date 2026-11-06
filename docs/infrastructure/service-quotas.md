# AWS Service Quotas Review

## Overview

The project requires three separate EC2 instances: one Coordinator and two Shards. The infrastructure is planned for the `us-east-1` region.

During the quota investigation, access to AWS Service Quotas was denied through both AWS CLI and AWS Management Console.

The active AWS Academy role does not have permission to perform `servicequotas:ListServiceQuotas`. Therefore, account-specific applied quotas and current utilization could not be verified.

## Relevant Service Quotas

| Service | Quota                            | AWS published default | Account-specific value |
| ------- | -------------------------------- | --------------------: | ---------------------- |
| EC2     | Running On-Demand Standard vCPUs |               5 vCPUs | Not accessible         |
| VPC     | VPCs per Region                  |                     5 | Not accessible         |
| VPC     | Subnets per VPC                  |                   200 | Not accessible         |
| VPC     | Internet gateways per Region     |                     5 | Not accessible         |

_Published defaults are reference values, not verified quotas for the AWS Academy account._

## Project Resource Requirements

| Resource          | Planned quantity |
| ----------------- | ---------------: |
| EC2 instances     |                3 |
| VPCs              |                1 |
| Subnets           |                2 |
| Internet Gateways |                1 |
| NAT Gateways      |                0 |

The EC2 vCPU requirement cannot be calculated until instance types are selected.

## Sandbox Limitations

The following access restriction was observed:

- AWS CLI `service-quotas list-service-quotas` returned `AccessDeniedException`.
- AWS Management Console also denied access to AWS service quota information.
- The active Academy role does not have permission for `servicequotas:ListServiceQuotas`.

This is an IAM permission restriction, not evidence that any service quota has been exceeded.

## Conclusion

The infrastructure design uses a small number of resources and does not require quota increases based on the published default limits currently identified.

However, actual account-specific quotas and utilization remain unverified due to AWS Academy restrictions. They should be checked in an unrestricted AWS account before deployment.

No quota increase requests were submitted.

## EC2 Instance Type Selection

The project uses three separate `t2.small` EC2 instances:

- 1 Coordinator instance.
- 2 Shard instances.

Each instance provides 1 vCPU and 2 GiB of memory.

The total planned compute capacity is 3 vCPUs and 6 GiB of RAM.

### Rationale

`t2.small` was selected as a cost-conscious option for the initial educational prototype.

The configuration provides more memory than `t2.micro` while keeping the total vCPU requirement below the published default of 5 vCPUs for the EC2 Running On-Demand Standard quota.

T2 instances use burstable CPU performance, which is suitable for development and moderate workloads. Actual performance must be evaluated during Milestone 2 testing.

### Estimated Compute Cost

The reference Linux On-Demand price in `us-east-1` is approximately $0.023 per instance-hour.

For three instances running continuously for 730 hours:

`3 × $0.023 × 730 = $50.37/month`

This estimate excludes EBS storage, public IPv4 addresses, data transfer, and potential additional charges.

### Deployment Considerations

- Coordinator is planned for the public subnet.
- Both Shards are planned for the private subnet.
- Shards should accept application traffic only from the Coordinator.
- The selected instance type must be verified as available in the target Availability Zone before deployment.
- The actual AWS Academy quota and deployment permissions remain unverified.

The configuration is intended for an educational prototype, not production workloads.
