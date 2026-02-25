# Meta
[meta]: #meta
- Name: AWS European Sovereign Cloud Account for BOSH Stemcell Publishing
- Start Date: 2026-02-25
- Author(s): @I766702
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

This RFC proposes creating a new AWS account within AWS European Sovereign Cloud to publish BOSH stemcells to isolated European Sovereign Cloud regions, enabling Cloud Foundry deployments for government and highly regulated customers with data sovereignty requirements.


## Problem

AWS European Sovereign Cloud is physically and logically isolated from standard AWS regions. Standard AWS accounts cannot access or publish resources to European Sovereign Cloud regions, and resources cannot be replicated between them.

Without BOSH stemcells available in AWS European Sovereign Cloud regions, Cloud Foundry cannot be deployed in these environments, preventing adoption by government agencies and regulated industries with strict data residency and compliance requirements.


## Proposal

Create a new AWS account within the AWS European Sovereign Cloud partition to enable BOSH stemcell publishing to European Sovereign Cloud regions.

### Pipeline

The existing stemcell build and publishing pipeline must be extended to support AWS European Sovereign Cloud regions.

### Account Setup

- Establish AWS European Sovereign Cloud account owned by the Cloud Foundry Foundation
- Administrative access controlled by Foundational Infrastructure Working Group
- Implement least-privilege IAM access controls for automation and administrators

### Stemcell Publishing

- Extend existing CI/CD pipeline to publish stemcells to AWS European Sovereign Cloud regions
- Use the same stemcell build process (no content changes required)
- Publish stemcells to S3 buckets and as AMIs in all available European Sovereign Cloud regions
- Maintain version parity with standard AWS commercial region stemcells

### Infrastructure

- S3 buckets for heavy stemcells with lifecycle policies per RFC-0010 (3-year retention)
- IAM service accounts for CI/CD automation
- CloudTrail audit logging enabled
- Encryption at rest for all stored stemcells
- Basic monitoring and cost alerting

### Documentation

- Update stemcell download documentation to include European Sovereign Cloud regions
- Create operational runbooks for publishing process
- Document BOSH cloud config examples for European Sovereign Cloud


## Open Questions

1. Are there specific compliance certifications (FedRAMP, ITAR) required for the stemcell publishing process?
2. How will the AWS European Sovereign Cloud account costs be funded?
3. Should stemcells include signing or attestation for integrity verification?


## Alternatives Considered

### No Action
Do not publish stemcells to AWS European Sovereign Cloud. This limits Cloud Foundry adoption by government and regulated customers with sovereignty requirements.

### Customer-Managed Publishing
Provide tools for customers to build and publish their own stemcells. This creates a high barrier to entry and results in fragmented stemcell versions across environments.

### Partner-Based Distribution
Partner with AWS or commercial vendors to handle stemcell publication. This creates vendor dependencies and may not align with the open-source distribution model.


## Rationale

Foundation-managed stemcell publishing ensures consistency, maintains quality control, enables broad accessibility, and aligns with the open-source mission while expanding Cloud Foundry to government and regulated sectors.


## References

- [AWS European Sovereign Cloud Overview](https://aws.amazon.com/sovereign-cloud/)
- [RFC-0010: Stemcell Cleanup](rfc-0010-stemcell-cleanup.md)
- [BOSH Stemcells Documentation](https://bosh.io/stemcells/)
- [AWS European Sovereign Cloud Regions Documentation](https://docs.aws.amazon.com/sovereign-cloud/)
