
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

# Reuse existing AWS Academy Default VPC.
data "aws_vpc" "existing" {
  id = var.existing_vpc_id
}

# Reuse existing public subnet for the Coordinator.
data "aws_subnet" "coordinator" {
  id = var.existing_public_subnet_id
}

# Private subnet shared by both Shards.
resource "aws_subnet" "private" {
  vpc_id                  = data.aws_vpc.existing.id
  cidr_block              = var.private_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = false

  tags = {
    Name = "CloudCapstone-Private-Subnet"
    Type = "Private"
  }
}

# Isolated route table: only the implicit local VPC route.
resource "aws_route_table" "private" {
  vpc_id = data.aws_vpc.existing.id

  tags = {
    Name = "CloudCapstone-Private-Route-Table"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# Coordinator Security Group.
resource "aws_security_group" "coordinator" {
  name        = "CloudCapstone-Coordinator-SG"
  description = "Controls access to the Coordinator API"
  vpc_id      = data.aws_vpc.existing.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "CloudCapstone-Coordinator-SG"
  }
}

# Shards Security Group.
resource "aws_security_group" "shards" {
  name        = "CloudCapstone-Shards-SG"
  description = "Allows internal traffic from the Coordinator"
  vpc_id      = data.aws_vpc.existing.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "CloudCapstone-Shards-SG"
  }
}

# Client access to the Coordinator API.
resource "aws_vpc_security_group_ingress_rule" "coordinator_from_client" {
  security_group_id = aws_security_group.coordinator.id

  cidr_ipv4   = var.coordinator_client_cidr
  from_port   = var.coordinator_port
  to_port     = var.coordinator_port
  ip_protocol = "tcp"

  description = "Client access to Coordinator API"
}

# Shards register with the Coordinator over the private VPC network.
resource "aws_vpc_security_group_ingress_rule" "coordinator_from_shards" {
  security_group_id            = aws_security_group.coordinator.id
  referenced_security_group_id = aws_security_group.shards.id

  from_port   = var.coordinator_port
  to_port     = var.coordinator_port
  ip_protocol = "tcp"

  description = "Shard registration with Coordinator"
}

# Only the Coordinator can initiate inbound connections to Shards.
resource "aws_vpc_security_group_ingress_rule" "shards_from_coordinator" {
  security_group_id            = aws_security_group.shards.id
  referenced_security_group_id = aws_security_group.coordinator.id

  from_port   = var.shard_port_start
  to_port     = var.shard_port_end
  ip_protocol = "tcp"

  description = "Coordinator to Shards internal API"
}
