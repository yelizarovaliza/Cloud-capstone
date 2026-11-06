# VPC Network Infrastructure

## 1. Overview

The project network infrastructure is defined using Terraform and deployed in the AWS `us-east-1` region.

The network consists of one VPC with a public subnet and a private subnet located in the same Availability Zone.

## 2. Network Addressing

| Component      | CIDR          | Purpose                                                 |
| -------------- | ------------- | ------------------------------------------------------- |
| VPC            | `10.0.0.0/16` | Main project network                                    |
| Public Subnet  | `10.0.1.0/24` | Resources requiring direct internet connectivity        |
| Private Subnet | `10.0.2.0/24` | Internal resources without direct internet connectivity |

Both subnets use Availability Zone `us-east-1a`.

## 3. Network Components

- **VPC:** Main isolated virtual network.
- **Internet Gateway:** Attached to the VPC to provide internet connectivity for the public subnet.
- **Public Route Table:** Contains a default route (`0.0.0.0/0`) through the Internet Gateway.
- **Private Route Table:** Contains only the automatically created local VPC route.
- **Subnet Associations:** Each subnet is associated with its corresponding route table.

A NAT Gateway is intentionally omitted to avoid additional costs.

## 4. Public and Private Subnets

The public subnet has `map_public_ip_on_launch = true` and a route to the Internet Gateway.

The private subnet has `map_public_ip_on_launch = false` and no direct route to an Internet Gateway or NAT Gateway.

## 5. Terraform Validation

The configuration was checked using:

- `terraform fmt`
- `terraform validate`
- `terraform plan`

Validation completed successfully.

Terraform generated the following plan:

`Plan: 8 to add, 0 to change, 0 to destroy.`

No resources have been deployed yet. The infrastructure currently exists as Terraform configuration only.

## 6. Sandbox Limitations

During the initial planning process, Terraform encountered an explicit IAM Deny for `ec2:DescribeAvailabilityZones`.

The restriction was imposed by the AWS Academy Sandbox policy `voc-cancel-cred`.

To avoid this restricted API operation, the Availability Zone was specified explicitly as `us-east-1a`.

After this change, `terraform plan` completed successfully.

## 7. Design Limitations

- Only one Availability Zone is used.
- No NAT Gateway is configured.
- No compute resources or security groups are included at this stage.
- The private subnet does not have direct internet access.

These choices keep the initial network architecture simple and minimize unnecessary costs.
