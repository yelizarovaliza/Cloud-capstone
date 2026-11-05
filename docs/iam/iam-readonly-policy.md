# IAM Read-Only Policy

## 1. Objective

The objective is to define a custom AWS IAM policy that grants read-only access to selected AWS resources without allowing users to create, modify, or delete them.

The policy is defined using Terraform as Infrastructure as Code (IaC).

## 2. Policy Overview

**Policy name:** `ProjectReadOnlyPolicy`

**Terraform resource:** `aws_iam_policy.project_read_only`

The policy covers the following AWS services:

| Service        | Allowed operations                                                     |
| -------------- | ---------------------------------------------------------------------- |
| EC2            | Describe resources                                                     |
| CloudFormation | Describe stacks, events and resources; retrieve templates; list stacks |
| DynamoDB       | List tables, describe tables, read items, query and scan               |
| IAM            | Get and list roles and policies                                        |

All statements use `Effect = "Allow"`.

No resource creation, modification, or deletion actions are included.

## 3. Infrastructure as Code

The policy is defined in:

`infrastructure/iam/main.tf`

Terraform uses `jsonencode()` to generate the IAM JSON policy document.

The AWS provider is configured to use the `us-east-1` region.

## 4. Validation Results

The following Terraform commands were executed:

| Command              | Result     |
| -------------------- | ---------- |
| `terraform init`     | Successful |
| `terraform fmt`      | Executed   |
| `terraform validate` | Successful |
| `terraform plan`     | Successful |

Terraform validation returned:

`Success! The configuration is valid.`

The execution plan showed:

- 1 resource to add
- 0 resources to change
- 0 resources to destroy

The resource planned for creation was `aws_iam_policy.project_read_only`.

## 5. Sandbox Limitations

The policy was defined and validated as Terraform code.

It was not deployed because the AWS Academy environment has restricted IAM permissions. The active role is `voclabs`, and an explicit deny was confirmed for the `iam:GetRole` action.

Therefore, successful policy creation and attachment could not be verified in the sandbox.

## 6. Security Considerations

- The policy does not include write or delete actions.
- Some read operations use wildcard resources because AWS requires or supports resource-level restrictions differently for different actions.
- DynamoDB `Scan` and `Query` allow reading table data, not just metadata.
- This policy is a custom managed policy and is not attached to any role by the current Terraform configuration.
- The effective permissions of a user or role may still be restricted by other IAM policies or organizational controls.

## 7. Conclusion

A custom IAM read-only policy has been defined using Terraform.

Its syntax and planned resource creation were successfully validated. Actual deployment remains unverified due to AWS Academy sandbox restrictions.
