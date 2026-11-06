# ADR-003: CIDR Addressing Scheme

**Status:** Accepted

## Context

The project requires an AWS VPC with separate public and private subnets. The addressing scheme should be simple, scalable, and avoid overlapping IP ranges.

## Decision

Use the following CIDR blocks:

| Network        | CIDR          |
| -------------- | ------------- |
| VPC            | `10.0.0.0/16` |
| Public Subnet  | `10.0.1.0/24` |
| Private Subnet | `10.0.2.0/24` |

Both subnets are located in `us-east-1a`.

## Rationale

- The `10.0.0.0/16` range provides sufficient private IPv4 address space for future expansion.
- Separate `/24` ranges make network segmentation straightforward.
- Public and private subnet ranges do not overlap.
- Additional subnets can be introduced later without redesigning the entire VPC.

## Consequences

The project has a simple and clearly segmented network structure. The selected addressing scheme supports future expansion while keeping the initial implementation manageable.
