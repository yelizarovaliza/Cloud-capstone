
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "existing_vpc_id" {
  description = "Existing AWS Academy Default VPC ID"
  type        = string
  default     = "vpc-0d83c8e68a98370e1"
}

variable "existing_public_subnet_id" {
  description = "Existing public subnet for the Coordinator"
  type        = string
  default     = "subnet-0af45210ea4706e53"
}

variable "private_subnet_cidr" {
  description = "CIDR for the new private Shard subnet"
  type        = string
  default     = "172.31.96.0/20"
}

variable "availability_zone" {
  description = "Availability Zone for the private subnet"
  type        = string
  default     = "us-east-1a"
}

variable "coordinator_port" {
  type    = number
  default = 8000
}

variable "shard_port_start" {
  type    = number
  default = 8001
}

variable "shard_port_end" {
  type    = number
  default = 8002
}

variable "coordinator_client_cidr" {
  description = "CIDR allowed to access the public Coordinator API"
  type        = string

  validation {
    condition     = can(cidrhost(var.coordinator_client_cidr, 0))
    error_message = "Provide a valid IPv4 CIDR, for example 203.0.113.10/32."
  }
}
