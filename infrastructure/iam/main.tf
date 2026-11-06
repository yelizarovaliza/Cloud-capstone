
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



# IAM Role
resource "aws_iam_role" "project_read_only_role" {
  name = "ProjectReadOnlyRole"

  description = "Role for accessing project resources in read-only mode"

  # Defines who can assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          AWS = var.trusted_principal_arn
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach the custom read-only policy to the role
resource "aws_iam_role_policy_attachment" "project_read_only_attachment" {
  role       = aws_iam_role.project_read_only_role.name
  policy_arn = aws_iam_policy.project_read_only.arn
}
