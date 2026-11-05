# IAM Role Analysis

## 1. Objective

The purpose of this analysis is to investigate IAM permissions in the AWS Academy sandbox, understand how permission policies are attached to IAM roles, and learn how to interpret policy documents.

The assignment specifically mentions the `LabRole` role. However, since it was not available for inspection, another accessible role was selected for practical analysis.

## 2. Role identification

| Property                               | Observed value                     |
| -------------------------------------- | ---------------------------------- |
| AWS environment                        | AWS Academy sandbox                |
| Role analyzed                          | `EMR_EC2_DefaultRole`              |
| Expected role from assignment          | `LabRole`                          |
| `LabRole` available for inspection     | No                                 |
| Selected role available for inspection | Yes                                |
| Attached managed policy                | `AmazonElasticMapReduceforEC2Role` |

**Important:** `EMR_EC2_DefaultRole` is used here as an example for learning IAM policy analysis. It is not assumed to be equivalent to `LabRole`.

## 3. Attached policy

The role has one attached managed policy:

`AmazonElasticMapReduceforEC2Role`

The policy uses the following version:

`2012-10-17`

Its statement has:

- `Effect: Allow`
- `Resource: "*"`
- A list of permitted AWS actions.

### 3.1. Policy JSON

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": "*",
      "Action": [
        "cloudwatch:*",
        "dynamodb:*",
        "ec2:Describe*",
        "elasticmapreduce:Describe*",
        "elasticmapreduce:ListBootstrapActions",
        "elasticmapreduce:ListClusters",
        "elasticmapreduce:ListInstanceGroups",
        "elasticmapreduce:ListInstances",
        "elasticmapreduce:ListSteps",
        "kinesis:CreateStream",
        "kinesis:DeleteStream",
        "kinesis:DescribeStream",
        "kinesis:GetRecords",
        "kinesis:GetShardIterator",
        "kinesis:MergeShards",
        "kinesis:PutRecord",
        "kinesis:SplitShard",
        "rds:Describe*",
        "s3:*",
        "sdb:*",
        "sns:*",
        "sqs:*",
        "glue:CreateDatabase",
        "glue:UpdateDatabase",
        "glue:DeleteDatabase",
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:CreateTable",
        "glue:UpdateTable",
        "glue:DeleteTable",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetTableVersions",
        "glue:CreatePartition",
        "glue:BatchCreatePartition",
        "glue:UpdatePartition",
        "glue:DeletePartition",
        "glue:BatchDeletePartition",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:BatchGetPartition",
        "glue:CreateUserDefinedFunction",
        "glue:UpdateUserDefinedFunction",
        "glue:DeleteUserDefinedFunction",
        "glue:GetUserDefinedFunction",
        "glue:GetUserDefinedFunctions"
      ]
    }
  ]
}
```

## 4. Understanding the policy structure

| JSON element | Meaning                                        | Observed value                                         |
| ------------ | ---------------------------------------------- | ------------------------------------------------------ |
| `Version`    | Policy language version                        | `2012-10-17`                                           |
| `Statement`  | Permission rules                               | One statement                                          |
| `Effect`     | Whether the statement allows or denies actions | `Allow`                                                |
| `Action`     | AWS operations covered by the statement        | Multiple services and actions                          |
| `Resource`   | Resources to which the statement applies       | `*` — all resources within the scope of this statement |

### 4.1. Effect

The policy uses:

`"Effect": "Allow"`

This means the listed actions are allowed by this policy statement, subject to other applicable permission controls.

There is no explicit `Deny` statement in the policy document provided.

### 4.2. Resource

The policy uses:

`"Resource": "*"`

The wildcard means the statement is not restricted to specific resource ARNs. It applies to all resources for actions that support resource-level permissions.

Some AWS actions do not support resource-level restrictions and require `"*"`.

### 4.3. Action

The `Action` array contains permissions for several AWS services.

The policy combines broad permissions, such as `s3:*`, with more specific permissions, such as `ec2:Describe*`.

## 5. Permissions analysis by AWS service

| AWS service       | Actions in the policy                                                                                    | Interpretation                                             |
| ----------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| CloudWatch        | `cloudwatch:*`                                                                                           | All CloudWatch actions covered by this policy              |
| DynamoDB          | `dynamodb:*`                                                                                             | All DynamoDB actions covered by this policy                |
| EC2               | `ec2:Describe*`                                                                                          | Describe and inspect EC2 resources                         |
| Elastic MapReduce | `elasticmapreduce:Describe*`, `elasticmapreduce:List*` (specific listed actions)                         | Inspect EMR resources and list cluster-related information |
| Kinesis           | Create, delete, describe streams; read records; get shard iterators; merge and split shards; put records | Both management and data operations                        |
| RDS               | `rds:Describe*`                                                                                          | Inspect RDS resources                                      |
| S3                | `s3:*`                                                                                                   | All S3 actions covered by this policy                      |
| SimpleDB          | `sdb:*`                                                                                                  | All SimpleDB actions covered by this policy                |
| SNS               | `sns:*`                                                                                                  | All SNS actions covered by this policy                     |
| SQS               | `sqs:*`                                                                                                  | All SQS actions covered by this policy                     |
| Glue              | Create, update, delete, and get databases, tables, partitions, and user-defined functions                | Both read and modification operations                      |

**Note:** The EMR permissions include specific list actions, not a general `elasticmapreduce:List*` wildcard. The table groups them for readability; the exact actions are preserved in the JSON above.

## 6. Key findings

1. The policy grants permissions using `Allow`.
2. The policy uses `"Resource": "*"`, rather than specifying individual resource ARNs.
3. Some services have broad permissions, such as `s3:*`, `dynamodb:*`, and `cloudwatch:*`.
4. Other services have narrower permissions. For example, EC2 and RDS permissions are limited to `Describe*` actions.
5. The policy includes both read-oriented and modification-oriented operations.
6. There is no explicit `Deny` statement in the provided policy document.
7. This is not a read-only policy because it allows operations such as creating, updating, and deleting resources.

## 7. Security observations

The policy is relatively broad in scope because several services have wildcard actions and the statement uses `"Resource": "*"`.

For example:

- `s3:*` grants all S3 actions covered by the policy.
- `dynamodb:*` grants all DynamoDB actions covered by the policy.
- `cloudwatch:*` grants all CloudWatch actions covered by the policy.

This is broader than the principle of least privilege, which recommends granting only the permissions required for a specific task.

However, this policy document alone does not establish the role's complete effective permissions. Other controls may further restrict access, including explicit Deny statements in other applicable policies, permissions boundaries, session policies, and AWS Organizations service control policies.

## 8. Limitations of the analysis

The analysis is based on the policy document attached to `EMR_EC2_DefaultRole`.

The following information has not yet been independently verified:

- Whether the role has additional inline policies.
- The role's trust relationship.
- Whether other policies or permission boundaries affect its effective permissions.
- Whether the sandbox applies additional restrictions.

The original assignment asks for an analysis of `LabRole`. Since that role could not be inspected, this analysis uses `EMR_EC2_DefaultRole` as a practical example instead.

## 9. Next steps

1. Inspect the role's trust relationship.
2. Check whether additional inline policies are attached.
3. Learn how to distinguish identity-based policies from trust policies.
4. Return to the assignment's `LabRole` requirements and document any sandbox limitations.
5. Prepare a separate read-only IAM policy as required by Milestone 1.

### AWS Academy Sandbox Restrictions

The active AWS Academy role is `voclabs`.

The following command was tested:

```powershell
aws iam get-role --role-name voclabs
```

Result: AccessDenied.

AWS explicitly denied the iam:GetRole action through an
identity-based policy.

This confirms that the sandbox restricts users from inspecting
the configuration of their active IAM role.

The restriction is documented as an environment limitation.
No attempt was made to bypass it.
