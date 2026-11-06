
variable "aws_region" {
  description = "AWS region where infrastructure is managed"
  type        = string
}

variable "trusted_principal_arn" {
  description = "ARN of the external IAM principal allowed to assume the role"
  type        = string
}