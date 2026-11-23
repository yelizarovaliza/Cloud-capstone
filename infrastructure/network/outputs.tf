
output "vpc_id" {
  description = "Reused Default VPC ID"
  value       = data.aws_vpc.existing.id
}

output "coordinator_public_subnet_id" {
  description = "Existing public subnet for Coordinator"
  value       = data.aws_subnet.coordinator.id
}

output "private_subnet_id" {
  description = "New private subnet for Shards"
  value       = aws_subnet.private.id
}

output "private_route_table_id" {
  description = "Private route table for Shards"
  value       = aws_route_table.private.id
}

output "coordinator_security_group_id" {
  description = "Coordinator Security Group ID"
  value       = aws_security_group.coordinator.id
}

output "shards_security_group_id" {
  description = "Shards Security Group ID"
  value       = aws_security_group.shards.id
}
