# Cloud Capstone — AWS Infrastructure Foundation

## 1. Project Overview

This repository contains the infrastructure foundation for the Cloud Architecture Capstone project.

The main goal of Milestone 1 is to prepare a reproducible AWS infrastructure using **Terraform**, investigate the available AWS Academy permissions, define the network architecture, and estimate the resources and costs required for Milestone 2.

The planned application architecture for Milestone 2 consists of:

- **Coordinator** — receives client requests and routes them to the appropriate Shard.
- **Shard 1** — stores and processes part of the distributed data.
- **Shard 2** — stores and processes another part of the distributed data.

The infrastructure is designed to separate public-facing components from internal services.

### Current Project Status

| Component                             | Status                                          |
| ------------------------------------- | ----------------------------------------------- |
| Terraform tool selection              | Completed                                       |
| Architecture Decision Records         | Created                                         |
| IAM Terraform configuration           | Implemented and validated                       |
| Network Terraform configuration       | Implemented and validated                       |
| IAM permissions investigation         | Partially completed due to Academy restrictions |
| Service Quotas investigation          | Attempted; account-specific values unavailable  |
| M2 budget estimation                  | Completed                                       |
| OpenSpec proposal                     | Documented                                      |
| AWS deployment                        | Not performed                                   |
| Deployment and teardown demonstration | Not performed                                   |

**Important:** Terraform validation and planning have been completed, but no AWS resources have been created using `terraform apply`.

---

## 2. Technology Stack

| Technology                | Purpose                                  |
| ------------------------- | ---------------------------------------- |
| Amazon Web Services (AWS) | Cloud infrastructure provider            |
| AWS Academy Learner Lab   | Restricted AWS learning environment      |
| Terraform                 | Infrastructure as Code                   |
| AWS CLI                   | AWS account and permission investigation |
| PowerShell                | Command-line environment                 |
| Git                       | Version control                          |

### Tested Versions

| Tool                       | Version                 |
| -------------------------- | ----------------------- |
| Terraform                  | 1.16.6                  |
| AWS CLI                    | 2.36.45                 |
| AWS Provider for Terraform | 6.72.0                  |
| Operating System           | Windows 10 / Windows 11 |

The Terraform AWS provider version is constrained in the Terraform configuration. The `.terraform.lock.hcl` files preserve the selected provider version for reproducible initialization.

---

## 3. Repository Structure

```text
Cloud-capstone/
│
├── README.md
├── ai-architecture-review.md
├── budget-estimate.md
│
├── docs/
│   ├── adr/
│   │   ├── adr-001-iac-tool.md
│   │   ├── adr-002-stack-layout.md
│   │   └── adr-003-cidr.md
│   │
│   ├── iam/
│   │   ├── iam-readonly-policy.md
│   │   ├── iam-role.md
│   │   └── labrole-analysis.md
│   │
│   └── infrastructure/
│       ├── service-quotas.md
│       └── vpc-network.md
│
├── infrastructure/
│   ├── .gitignore
│   │
│   ├── iam/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── .terraform.lock.hcl
│   │
│   └── network/
│       ├── main.tf
│       ├── variables.tf
│       ├── output.tf
│       └── .terraform.lock.hcl
│
└── openspec/
    └── proposal.md
```

### Directory Description

- `docs/adr/` — architecture decisions and their rationale.
- `docs/iam/` — IAM policy, role, and AWS Academy permission investigation.
- `docs/infrastructure/` — network architecture and service quota documentation.
- `infrastructure/iam/` — Terraform configuration for IAM resources.
- `infrastructure/network/` — Terraform configuration for VPC and networking resources.
- `openspec/` — proposal describing the Milestone 1 scope and acceptance criteria.
- `budget-estimate.md` — M2 cost estimation.
- `ai-architecture-review.md` — architecture review and recommendations.

---

## 4. Prerequisites

Before reproducing the project, install:

1. Terraform CLI.
2. AWS CLI v2.
3. Git.
4. Access to an AWS Academy Learner Lab environment.

Verify the installations:

```powershell
terraform -version
aws --version
git --version
```

The commands in this README are written for PowerShell.

---

## 5. AWS Environment Configuration

The project uses AWS Academy Learner Lab in the `us-east-1` region.

### 5.1. Start the Learner Lab

1. Open AWS Academy.
2. Start the Learner Lab session.
3. Open AWS Details.
4. Find the temporary AWS CLI credentials.
5. Configure the AWS CLI using the credentials provided by the lab.

Use the credential configuration method provided by AWS Academy. Do not commit credentials or session tokens to the repository.

Temporary credentials expire when the lab session expires or the credential validity period ends. Refresh them when necessary.

### 5.2. Verify AWS Access

Run:

```powershell
aws sts get-caller-identity
```

A successful response confirms that the current AWS CLI session is authenticated.

The active role observed during this project was `voclabs`.

The role should not automatically be treated as equivalent to an assignment-specific `LabRole`.

### 5.3. Check the AWS Region

```powershell
aws configure get region
```

The intended project region is:

```text
us-east-1
```

If necessary, configure the region:

```powershell
aws configure set region us-east-1
```

This command does not replace temporary AWS Academy credentials.

---

## 6. Terraform Infrastructure

The project uses two independent Terraform stacks:

- IAM
- Network

Each stack has its own configuration and Terraform state.

This separation makes it easier to validate, plan, and manage infrastructure components independently.

### 6.1. Initialize and Validate the IAM Stack

Navigate to the IAM directory:

```powershell
cd infrastructure/iam
```

Initialize Terraform:

```powershell
terraform init
```

Validate the configuration:

```powershell
terraform validate
```

Expected result:

```text
Success! The configuration is valid.
```

Generate an execution plan:

```powershell
terraform plan
```

Expected plan from the Milestone 1 review:

```text
Plan: 3 to add, 0 to change, 0 to destroy.
```

The three planned resources are:

1. Custom IAM policy.
2. IAM role.
3. IAM role-policy attachment.

#### IAM Configuration Notes

The IAM role uses a configurable trusted principal ARN.

The current `terraform.tfvars` contains a placeholder ARN. It must be replaced with a valid, approved principal before any deployment.

Do not run `terraform apply` with the placeholder value.

The AWS Academy environment may also deny IAM operations required for deployment.

More information:

- `docs/iam/iam-readonly-policy.md`
- `docs/iam/iam-role.md`
- `docs/iam/labrole-analysis.md`

### 6.2. Initialize and Validate the Network Stack

Navigate to the network directory:

```powershell
cd ../network
```

Initialize Terraform:

```powershell
terraform init
```

Validate the configuration:

```powershell
terraform validate
```

Expected result:

```text
Success! The configuration is valid.
```

Generate an execution plan:

```powershell
terraform plan
```

Expected plan from the Milestone 1 review:

```text
Plan: 8 to add, 0 to change, 0 to destroy.
```

The eight planned resources are:

1. One VPC.
2. One public subnet.
3. One private subnet.
4. One Internet Gateway.
5. One public route table.
6. One private route table.
7. One public subnet route-table association.
8. One private subnet route-table association.

---

## 7. Network Architecture

The network stack defines the following architecture:

| Resource            | Configuration                          |
| ------------------- | -------------------------------------- |
| AWS Region          | `us-east-1`                            |
| Availability Zone   | `us-east-1a`                           |
| VPC CIDR            | `10.0.0.0/16`                          |
| Public Subnet       | `10.0.1.0/24`                          |
| Private Subnet      | `10.0.2.0/24`                          |
| Internet Gateway    | Attached to the VPC                    |
| Public Route Table  | Default route through Internet Gateway |
| Private Route Table | No default internet route              |

### Public Subnet

The public subnet is intended for components that may require external connectivity.

The planned M2 Coordinator may be placed here if public access is required.

### Private Subnet

The private subnet is intended for internal application components.

The two Shards are planned to run in this subnet.

The private route table does not contain a default route to the Internet Gateway. No NAT Gateway is included in the current design.

### Network Limitations

- Both subnets are located in one Availability Zone.
- No NAT Gateway is configured.
- Security Groups have not yet been defined.
- No EC2 instances are deployed.
- The network exists only as Terraform configuration and a reviewed execution plan.

The network design is therefore a foundational lab architecture, not a production-ready highly available environment.

More information: `docs/infrastructure/vpc-network.md`.

---

## 8. AWS Academy Permissions and Service Quotas

The AWS Academy environment imposes restrictions on some IAM and infrastructure operations.

The following results were observed during investigation:

| Operation                                    | Result       |
| -------------------------------------------- | ------------ |
| `sts:GetCallerIdentity`                      | Successful   |
| `iam:GetRole` for `voclabs`                  | AccessDenied |
| `iam:ListAttachedRolePolicies` for `voclabs` | Successful   |
| Service Quotas API access                    | AccessDenied |
| Service Quotas Console access                | AccessDenied |
| `ec2:DescribeAvailabilityZones`              | AccessDenied |

The attached-policy listing for `voclabs` showed `ReadOnlyAccess`.

These results describe the observed session permissions. They do not establish the complete effective permissions of the role.

### Service Quota Notes

Account-specific quota values could not be retrieved.

General AWS quota defaults are documented in:

`docs/infrastructure/service-quotas.md`

AccessDenied must not be interpreted as evidence that a quota has been exceeded.

The network stack uses an explicitly configured Availability Zone (`us-east-1a`) because Availability Zone discovery was denied.

---

## 9. M2 Architecture and Budget

The planned M2 topology consists of:

- One Coordinator.
- Two Shards.
- Three EC2 instances in total.

The preliminary instance type is `t2.small`.

| Component   | Count |  vCPU |       RAM |
| ----------- | ----: | ----: | --------: |
| Coordinator |     1 |     1 |     2 GiB |
| Shards      |     2 |     2 |     4 GiB |
| **Total**   | **3** | **3** | **6 GiB** |

### Cost Estimate

The reference On-Demand rate used for the estimate is `$0.023/hour` per `t2.small` instance.

```text
3 × $0.023 × 730 hours = $50.37/month
```

Available AWS Academy budget:

```text
$20.00
```

The proposed three-instance configuration exceeds the available budget by approximately `$30.37` for a full month of continuous compute usage.

This calculation excludes EBS storage, public IPv4, data transfer, and other possible charges.

**Deployment decision:** The proposed M2 configuration must not be deployed under the current $20 budget without an approved alternative.

See `budget-estimate.md` for the full calculation and assumptions.

---

## 10. Terraform State and Repository Safety

Terraform state may contain infrastructure identifiers and sensitive information.

The repository includes an `infrastructure/.gitignore` file intended to exclude:

- `.terraform/` directories.
- Terraform state files.
- Terraform plan files.
- Local `.tfvars` files, except explicitly allowed example files.
- Terraform crash logs.

The `.terraform.lock.hcl` files should remain committed to preserve provider version selections.

Never commit:

- AWS access keys.
- AWS secret keys.
- AWS session tokens.
- Passwords.
- Sensitive Terraform state files.
- Real credentials or private configuration values.

For a shared or team deployment, use an appropriately secured remote Terraform backend with state locking. The current stacks do not establish a remote backend.

---

## 11. Reproducing the Milestone 1 Checks

The following commands reproduce the validation and planning checks without creating AWS resources.

From the repository root:

### IAM

```powershell
cd infrastructure/iam
terraform init
terraform validate
terraform plan
```

### Network

```powershell
cd ../network
terraform init
terraform validate
terraform plan
```

Expected results from the reviewed configuration:

| Stack   | Validation | Planned Resources |
| ------- | ---------- | ----------------: |
| IAM     | Successful |          3 to add |
| Network | Successful |          8 to add |

Terraform plan output can change if configuration, provider versions, variables, or the AWS environment change.

A successful plan does not mean that resources have been deployed.

---

## 12. Deployment and Teardown Status

No Terraform deployment has been performed for this milestone.

The following commands are documented for reference only and must not be executed without resolving the deployment blockers and confirming budget approval.

```powershell
terraform apply
```

To remove resources from a stack that has actually been deployed:

```powershell
terraform destroy
```

The current IAM stack is not deployment-ready because its trust principal is a placeholder.

The proposed M2 architecture is not within the current $20 budget.

Consequently:

- No deployment duration has been measured.
- No teardown duration has been measured.
- No recreation duration has been measured.
- No real first-attempt deployment failures have been recorded.

These measurements must be collected during an authorized, budget-approved deployment rather than estimated or invented.

---

## 13. Architecture Decision Records

The project decisions are documented in `docs/adr/`.

| ADR     | Decision                                      |
| ------- | --------------------------------------------- |
| ADR-001 | Terraform as the Infrastructure as Code tool  |
| ADR-002 | Separate Terraform stacks for IAM and Network |
| ADR-003 | VPC and subnet CIDR addressing                |

These records describe the rationale behind the infrastructure structure and configuration.

---

## 14. Milestone 1 Deliverables

| Deliverable                 | Location                                |
| --------------------------- | --------------------------------------- |
| Terraform IAM stack         | `infrastructure/iam/`                   |
| Terraform network stack     | `infrastructure/network/`               |
| IaC tool decision           | `docs/adr/adr-001-iac-tool.md`          |
| Stack layout decision       | `docs/adr/adr-002-stack-layout.md`      |
| CIDR decision               | `docs/adr/adr-003-cidr.md`              |
| IAM policy documentation    | `docs/iam/iam-readonly-policy.md`       |
| IAM role documentation      | `docs/iam/iam-role.md`                  |
| Academy role investigation  | `docs/iam/labrole-analysis.md`          |
| Network documentation       | `docs/infrastructure/vpc-network.md`    |
| Service quota investigation | `docs/infrastructure/service-quotas.md` |
| M2 budget estimate          | `budget-estimate.md`                    |
| AI architecture review      | `ai-architecture-review.md`             |
| OpenSpec proposal           | `openspec/proposal.md`                  |

---

## 15. Known Limitations and Next Steps

The following tasks remain before the infrastructure can be considered fully demonstrated:

1. Obtain authorized evidence for the exact `LabRole` required by the assignment.
2. Obtain account-specific Service Quotas information if access becomes available.
3. Confirm a real trusted principal for the IAM role.
4. Define and review Security Group rules for Coordinator-to-Shard communication.
5. Reconsider the M2 deployment architecture to fit the available budget.
6. Perform deployment, teardown, and recreation only after permission and budget approval.
7. Record actual deployment duration and any first-attempt errors.

The current repository provides a validated Terraform baseline and supporting documentation for Milestone 1. It does not claim that AWS infrastructure has already been deployed.

---

## 16. References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
- [Amazon VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [AWS Service Quotas](https://docs.aws.amazon.com/servicequotas/)
- [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [Amazon EC2 On-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
- [AWS Pricing Calculator](https://calculator.aws/)

---

**Project:** Cloud-capstone  
**Milestone:** 1 — AWS Infrastructure Foundation  
**Region:** `us-east-1`  
**Infrastructure as Code:** Terraform
