
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_policy" "project_read_only" {
  name        = "ProjectReadOnlyPolicy"
  description = "Read-only access to selected project resources"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid      = "ReadOnlyEC2"
        Effect   = "Allow"
        Action   = ["ec2:Describe*"]
        Resource = "*"
      },
      {
        Sid    = "ReadOnlyCloudFormation"
        Effect = "Allow"
        Action = [
          "cloudformation:DescribeStacks",
          "cloudformation:DescribeStackResources",
          "cloudformation:DescribeStackEvents",
          "cloudformation:GetTemplate",
          "cloudformation:ListStacks",
          "cloudformation:ListStackResources"
        ]
        Resource = "*"
      },
      {
        Sid      = "ListDynamoDBTables"
        Effect   = "Allow"
        Action   = ["dynamodb:ListTables"]
        Resource = "*"
      },
      {
        Sid    = "ReadDynamoDBData"
        Effect = "Allow"
        Action = [
          "dynamodb:DescribeTable",
          "dynamodb:GetItem",
          "dynamodb:BatchGetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          "arn:aws:dynamodb:*:*:table/*",
          "arn:aws:dynamodb:*:*:table/*/index/*"
        ]
      },
      {
        Sid    = "ReadOnlyIAM"
        Effect = "Allow"
        Action = [
          "iam:GetRole",
          "iam:ListRoles",
          "iam:GetPolicy",
          "iam:GetPolicyVersion",
          "iam:ListPolicies",
          "iam:ListPolicyVersions",
          "iam:ListAttachedRolePolicies",
          "iam:ListRolePolicies",
          "iam:GetRolePolicy"
        ]
        Resource = "*"
      }
    ]
  })
}
