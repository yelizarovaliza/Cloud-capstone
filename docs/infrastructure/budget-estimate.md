# Budget Estimate

**AWS Region:** `us-east-1` (N. Virginia)

**Availability Zone:** `us-east-1a`

**Available AWS Academy Budget:** **$20.00**

**Estimate Type:** Indicative On-Demand estimate

**Workload:** One Coordinator and two Shards (three EC2 instances total)

**Assessment Date:** November 24, 2026

## 1. Proposed M2 Architecture

The proposed M2 architecture consists of three EC2 instances:

| Component   | Count | Instance Type |       vCPU |       RAM |
| ----------- | ----: | ------------- | ---------: | --------: |
| Coordinator |     1 | `t2.small`    |          1 |     2 GiB |
| Shard       |     2 | `t2.small`    |          1 |     2 GiB |
| **Total**   | **3** |               | **3 vCPU** | **6 GiB** |

Proposed network placement:

- Coordinator — existing public subnet.
- Shards — dedicated private subnet.
- Coordinator API traffic is restricted through its Security Group.
- Shard API traffic is permitted only from the Coordinator Security Group.

The infrastructure configuration reuses the AWS Academy Default VPC and an existing public subnet. Terraform defines the additional private subnet, route table, and Security Groups.

## 2. Compute Cost Estimation

The reference On-Demand Linux price for one `t2.small` instance in `us-east-1` is approximately **$0.023 per hour**.

A month is assumed to contain 730 hours.

**Calculation:**

```text
3 instances × $0.023/hour × 730 hours

= $50.37 per month
```

| Item                                 | Estimated Cost |
| ------------------------------------ | -------------: |
| One `t2.small` per month             |         $16.79 |
| Three `t2.small` instances per month |     **$50.37** |
| Available AWS Academy budget         |     **$20.00** |
| Monthly budget overrun               |     **$30.37** |

The proposed architecture costs approximately 2.52 times the available budget for a full month of continuous operation.

Therefore, continuous monthly operation is not financially feasible within the current budget.

## 3. Maximum Runtime Within the Budget

Considering EC2 compute costs only, the theoretical maximum runtime is:

```text
$20.00 ÷ (3 × $0.023/hour)

= 289.86 hours

= approximately 12.1 days
```

This is an upper-bound estimate because it excludes storage, public IPv4 addresses, data transfer, and other possible charges.

A shorter deployment period is required to preserve a budget reserve.

## 4. Additional Infrastructure Costs

The following assumptions are used for a short-term deployment estimate:

| Resource    | Assumption                    |  Reference Price |
| ----------- | ----------------------------- | ---------------: |
| EC2         | 3 × `t2.small`                | $0.023/hour each |
| Public IPv4 | 1 address for the Coordinator |      $0.005/hour |
| EBS gp3     | 3 volumes × 8 GiB = 24 GiB    |   $0.08/GB-month |
| NAT Gateway | Not deployed                  |            $0.00 |

The Shards are placed in a private subnet and do not require public IPv4 addresses.

The EBS volume size of 8 GiB per instance is an estimation assumption and must be confirmed in the eventual EC2 launch configuration.

## 5. Time-Limited Deployment Estimate

A five-day deployment window is proposed for infrastructure deployment, integration testing, and demonstration.

### 5.1. Five-Day Cost Calculation

**EC2 compute:**

```text
3 × $0.023 × 24 hours × 5 days

= $8.28
```

**Public IPv4:**

```text
1 × $0.005 × 24 hours × 5 days

= $0.60
```

**EBS gp3 storage:**

```text
24 GiB × $0.08 × (5 / 30)

= $0.32
```

**Estimated total:**

```text
$8.28 + $0.60 + $0.32

= $9.20
```

| Cost Component       | Five-Day Estimate |
| -------------------- | ----------------: |
| EC2 compute          |             $8.28 |
| Public IPv4          |             $0.60 |
| EBS gp3 storage      |             $0.32 |
| **Estimated total**  |         **$9.20** |
| Available budget     |            $20.00 |
| **Remaining budget** |        **$10.80** |

### 5.2. Alternative Runtime Scenarios

| Deployment Duration | Estimated Cost | Remaining Budget |
| ------------------- | -------------: | ---------------: |
| 5 days              |          $9.20 |           $10.80 |
| 7 days              |         $12.88 |            $7.12 |
| 10 days             |         $18.40 |            $1.60 |

These estimates assume that all three instances and the public IPv4 address remain active throughout the selected period. EBS storage is charged for the provisioned storage duration.

The five-day scenario is recommended because it leaves a larger reserve for unmodeled costs.

## 6. Availability and Deployment Feasibility

### 6.1. Instance Type Availability

The AWS CLI command `describe-instance-type-offerings` was executed successfully for `us-east-1a`.

The result confirmed:

| Instance Type | Availability Zone | Result            |
| ------------- | ----------------- | ----------------- |
| `t2.small`    | `us-east-1a`      | Listed as offered |

This confirms that the instance type is offered in the selected Availability Zone. It does not guarantee available EC2 capacity at launch time.

Account-specific service quotas and all required IAM permissions must still be confirmed.

### 6.2. Availability Limitations

The proposed architecture has the following limitations:

- All three instances are located in one Availability Zone.
- Multi-AZ deployment is not included.
- Shard replication is not implemented.
- There is no automatic failover or data migration.
- Coordinator failure makes the public API unavailable.
- Shard failure makes records assigned to that Shard unavailable.
- The private subnet has no NAT Gateway or direct Internet route.

Because the Shards are placed in a private subnet, application dependencies must be prepared before deployment. Prebuilt application artifacts or an appropriately prepared AMI are required if the instances cannot download dependencies at startup.

This architecture is intended for a limited educational demonstration, not production high availability.

## 7. Cost Assumptions and Exclusions

The estimate is indicative and does not include:

- Data transfer charges.
- EBS snapshots and additional storage.
- Additional CloudWatch usage.
- Potential T2 CPU surplus-credit charges, depending on instance mode and workload.
- Taxes and other account-specific charges.
- Costs from resources that remain allocated after the test period.

The estimate uses reference AWS On-Demand prices and does not guarantee the final AWS Academy billing result.

Official pricing references:

- [Amazon EC2 On-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
- [Amazon EC2 T2 Instance Types](https://aws.amazon.com/ec2/instance-types/t2/)
- [Amazon VPC Pricing — Public IPv4](https://aws.amazon.com/vpc/pricing/)
- [Amazon EBS Pricing](https://aws.amazon.com/ebs/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)

After testing, EC2 instances must be terminated and unused EBS volumes and snapshots must be removed. Stopping an instance alone does not stop EBS storage charges.

## 8. Budget Decision

The full-month deployment of three `t2.small` instances is not feasible within the available $20 budget.

However, the estimated five-day deployment scenario costs approximately **$9.20**, including the assumed EC2 compute, one public IPv4 address, and EBS gp3 storage.

The following decision is proposed:

1. Retain three `t2.small` instances as the preliminary M2 configuration.
2. Use a maximum five-day deployment window for testing and demonstration.
3. Monitor AWS Academy budget consumption during deployment.
4. Do not deploy billable resources until IAM permissions and deployment prerequisites are confirmed.
5. Do not execute `terraform apply` without explicit deployment approval.
6. Terminate instances and remove unused billable resources after testing.

## 9. Conclusion

The initial M2 architecture costs approximately **$50.37 per month** for EC2 compute alone, exceeding the available AWS Academy budget of $20.

A time-limited deployment provides a more practical alternative. Under the stated assumptions, a five-day deployment is estimated at **$9.20**, leaving approximately **$10.80** as a reserve.

Therefore, the proposed M2 architecture is conditionally feasible for a short educational deployment, subject to IAM permissions, EC2 capacity, dependency preparation, and budget monitoring.

Terraform validation and planning can continue without creating billable resources. Actual deployment remains subject to the required approval.
