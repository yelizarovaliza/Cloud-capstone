output "read_only_policy_arn" {
  description = "ARN of the ProjectReadOnlyPolicy"
  value       = aws_iam_policy.project_read_only.arn
}

output "read_only_role_arn" {
  description = "ARN of the ProjectReadOnlyRole"
  value       = aws_iam_role.project_read_only_role.arn
}