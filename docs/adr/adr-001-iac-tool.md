# ADR-001: Infrastructure as Code Tool Selection

- **Status:** Accepted
- **Date:** 2026-11-05
- **Decision:** Terraform

## 1. Context

The project requires Infrastructure as Code (IaC) to define, provision, and manage cloud infrastructure.

The initial implementation will use AWS Academy sandbox. However, the project should remain extensible beyond AWS and allow infrastructure management across different cloud providers and external services.

## 2. Decision Drivers

The main requirements are:

- Support for multiple cloud providers.
- Consistent configuration language and workflow.
- Reusable infrastructure modules.
- Version control and reproducibility.
- Ability to preview infrastructure changes before applying them.
- Compatibility with the AWS Academy environment.

## 3. Alternatives Considered

### AWS CloudFormation

Advantages:

- Native AWS integration.
- AWS manages stack state.
- Supports change sets and drift detection.

Disadvantages:

- Primarily designed for AWS infrastructure.
- Less suitable as a unified tool for future multi-cloud infrastructure.

### Terraform

Advantages:

- Supports multiple cloud providers through providers.
- Uses a consistent declarative language (HCL).
- Supports reusable modules.
- Provides a plan-before-apply workflow.
- Can manage cloud infrastructure and selected third-party services.

Disadvantages:

- Requires state management.
- Provider plugins must be installed and maintained.
- Some new provider-specific features may not be immediately available.

## 4. Decision

Terraform is selected as the primary IaC tool for the project.

The project will use:

- Terraform configuration files (`.tf`).
- HCL as the configuration language.
- AWS Provider for the initial infrastructure.
- Terraform modules to organize reusable components.
- Terraform state to track managed infrastructure.

## 5. Consequences

Positive:

- Infrastructure definitions can be reused across different cloud providers.
- The project can expand beyond AWS without changing its primary IaC tool.
- Infrastructure changes can be reviewed through `terraform plan`.
- Configuration can be version-controlled in Git.

Trade-offs:

- Terraform state must be protected and managed carefully.
- AWS-specific resources still require AWS-specific Terraform resource definitions.
- AWS Academy permissions may prevent some resources from being created or managed.

## 6. Implementation Plan

1. Configure the AWS Provider.
2. Define IAM policies and roles as Terraform resources.
3. Define VPC and subnet resources.
4. Organize the infrastructure into logical modules or directories.
5. Validate configurations and review execution plans.
6. Document resources that cannot be deployed due to sandbox restrictions.
