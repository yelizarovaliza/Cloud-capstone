# Budget Estimate

**AWS Region:** `us-east-1` (N. Virginia)  
**Available AWS Academy Budget:** **$20.00**  
**Estimate Type:** Indicative On-Demand compute estimate  
**Workload:** One Coordinator and two Shards (three EC2 instances total)

## 1. Proposed M2 Architecture

The proposed M2 architecture consists of three EC2 instances:

| Component   | Count | Instance Type |       vCPU |       RAM |
| ----------- | ----: | ------------- | ---------: | --------: |
| Coordinator |     1 | `t2.small`    |          1 |     2 GiB |
| Shard       |     2 | `t2.small`    |          1 |     2 GiB |
| **Total**   | **3** |               | **3 vCPU** | **6 GiB** |

Proposed network placement:

- Coordinator — public subnet.
- Shards — private subnet.
- Shard communication should be restricted to the Coordinator using appropriate Security Group rules.

The current Milestone 1 Terraform network configuration does not yet include Security Groups or EC2 instances.

## 2. Compute Cost Estimation

The reference On-Demand Linux price for one `t2.small` instance in `us-east-1` is approximately **$0.023 per hour**.

For this estimate, a month is assumed to contain 730 hours.

**Calculation:**

```text
3 instances × $0.023/hour × 730 hours

= $50.37 per month
```

| Item                                 | Estimated Cost |
| ------------------------------------ | -------------: |
| One `t2.small` instance per month    |         $16.79 |
| Three `t2.small` instances per month |     **$50.37** |
| Available AWS Academy budget         |     **$20.00** |
| Amount exceeding the budget          |     **$30.37** |

The proposed architecture costs approximately 2.52 times the available budget for a full month of continuous operation.

## 3. Maximum Runtime Within the Budget

The theoretical maximum runtime for all three instances, considering compute costs only:

```text
$20.00 ÷ (3 × $0.023/hour)

= 289.86 hours

= approximately 12.1 days
```

This is an upper-bound estimate. Actual available runtime would be shorter because other AWS resources may also generate costs.

## 4. Additional Costs Not Included

The estimate above covers EC2 compute costs only.

The following costs are not included:

- EBS storage volumes and snapshots.
- Public IPv4 addresses.
- Data transfer.
- Potential CPU surplus-credit charges, depending on instance configuration and workload.
- Taxes and other account-specific charges.

Actual costs depend on resource configuration, usage, and current AWS pricing.

For a more accurate estimate, consult the [AWS Pricing Calculator](https://calculator.aws/) and the [EC2 On-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/) page before deployment.

## 5. Budget Assessment

**The proposed three-instance M2 architecture does not fit within the current $20 budget for a full month of continuous operation.**

Deploying all three instances for the entire month would exceed the available budget by approximately $30.37, even before additional infrastructure costs.

Therefore, the following decision is made:

1. Do not deploy the proposed M2 architecture under the current budget.
2. Keep the Terraform infrastructure definitions available for validation and planning.
3. Do not execute `terraform apply` for billable M2 resources without an approved budget.
4. Reconsider the deployment strategy and resource sizing before M2 implementation.

## 6. Assumptions and Limitations

- The Coordinator is counted as an additional EC2 instance. Therefore, two Shards mean three instances in total.
- `t2.small` is a preliminary sizing assumption, not a performance-tested choice.
- The price of $0.023/hour is an indicative reference rate and may change.
- Account-specific billing and quota information was not accessible through the available AWS Academy permissions.
- The $20 budget is the available credit limit provided for this project.

## 7. Conclusion

The initial M2 architecture requires three EC2 instances and has an estimated compute-only cost of **$50.37 per month**.

Since the available AWS Academy budget is **$20**, the proposed architecture is not financially feasible for continuous monthly operation.

For Milestone 1, Terraform validation and planning are sufficient to demonstrate the infrastructure design without creating billable resources. M2 deployment should be postponed until a budget-compatible solution is approved.
