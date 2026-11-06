# IAM Role and Trust Policy

## 1. Objective

The objective is to define an IAM Role that can be assumed by another IAM principal and has read-only access to selected AWS resources.

## 2. Role Configuration

**Role name:** `ProjectReadOnlyRole`

**Terraform resource:** `aws_iam_role.project_read_only_role`

The role uses a Trust Policy with:

- `Effect = Allow`
- `Principal = trusted_principal_arn`
- `Action = sts:AssumeRole`

The trusted principal ARN is configured through a Terraform variable.

The current ARN in `terraform.tfvars` is a placeholder and must be replaced before deployment.

## 3. Permissions Attachment

The custom `ProjectReadOnlyPolicy` is attached to the role using:

`aws_iam_role_policy_attachment`

This separates the role's trust configuration from its permissions.

## 4. Validation Results

| Command              | Result     |
| -------------------- | ---------- |
| `terraform fmt`      | Executed   |
| `terraform validate` | Successful |
| `terraform plan`     | Successful |

Terraform planned the following resources:

- 1 IAM Policy
- 1 IAM Role
- 1 IAM Role Policy Attachment

Plan summary:

`3 to add, 0 to change, 0 to destroy`

## 5. Sandbox Limitations

The IAM resources were described and validated using Terraform but were not deployed.

The AWS Academy environment restricts IAM inspection operations. Actual creation and attachment permissions have not been verified.

## 6. Conclusion

The IAM Role, Trust Policy, and managed policy attachment have been defined as Infrastructure as Code.

The configuration is syntactically valid, and Terraform successfully generated the expected execution plan.
