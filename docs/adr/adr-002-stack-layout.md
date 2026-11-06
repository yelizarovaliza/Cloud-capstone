# ADR-002: Terraform Stack Layout

**Status:** Accepted

## Context

The project requires Infrastructure as Code for multiple AWS resource groups, including IAM and network infrastructure.

## Decision

Organize Terraform configurations into separate directories based on infrastructure responsibilities:

```text
infrastructure/
├── iam/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
└── network/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

Each directory represents an independently managed Terraform configuration.

## Rationale

- IAM and network resources have different responsibilities.
- Separate configurations simplify validation and planning.
- Changes to one infrastructure area are less likely to affect another.
- The structure can be extended with additional stacks in future milestones.

## Consequences

The project has a modular and maintainable infrastructure layout. Each stack can be initialized, validated, planned, and managed independently.
