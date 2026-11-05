output "read_only_policy_arn" {
  description = "ARN of the ProjectReadOnlyPolicy"
  value       = aws_iam_policy.project_read_only.arn
}