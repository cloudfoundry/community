---
title: "Foundational Infrastructure Working Group Update"
date: "2025-09-02"
period: "June 2025 - September 2025"
---

# Foundational Infrastructure Working Group Update

## Summary

The Foundational Infrastructure Working Group achieved significant progress in strategic vision and concrete implementation. The group transitioned from RFC acceptance to active IPv6 dual-stack development while advancing identity management and storage infrastructure modernization.

Key collaborative contributions came from [Adrian Hoelzl](https://github.com/adrianhoelzl-sap) (SAP) leading UAA architectural improvements and [Benjamin Guttmann](https://github.com/benjaminguttmann-avtq) (SAP) spearheading Prometheus ecosystem modernization. Community members advanced storage infrastructure through AWS SDK v2 migration and cross-working group governance enhancements.

## Major Strategic Initiatives

### Identity and Credential Management Modernization

The Foundational Infrastructure Working Group demonstrated sustained commitment to enterprise security through strategic UAA identity management system enhancements. [Adrian Hoelzl](https://github.com/adrianhoelzl-sap) from SAP led [comprehensive ExternalLoginAuthenticationManager component refactoring](https://github.com/cloudfoundry/uaa/pull/3607), addressing technical debt in external identity provider integrations.

The refactoring enhances UAA's complex authentication scenario handling in enterprise environments, providing better error handling and improved logging. These improvements support Cloud Foundry operators in regulated industries through [security dependency updates](https://github.com/cloudfoundry/uaa/pull/3605), reducing operational complexity for large-scale deployments.

### IPv6 Dual-Stack Implementation in Active Development

Following [RFC-0038: IPv6 Dual Stack Support for Cloud Foundry](https://github.com/cloudfoundry/community/pull/1077) acceptance, the Foundational Infrastructure Working Group transitioned from strategic planning to active IPv6 dual-stack implementation across core BOSH infrastructure. This groundbreaking RFC represents the most significant networking evolution in Cloud Foundry's recent history, establishing comprehensive IPv6 dual-stack support across the entire platform.

Active development spans [BOSH core IPv6 prefix allocation](https://github.com/cloudfoundry/bosh/pull/2611), [AWS CPI multistack networks](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/181), and [comprehensive IPv6 testing frameworks](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/53). The implementation demonstrates significant progress toward production-ready IPv6 dual-stack support, positioning Cloud Foundry at modern networking standards through [NIC groups testing](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/54).

### Prometheus Ecosystem Modernization and Dependency Management

The Prometheus monitoring infrastructure saw transformative modernization efforts from community contributors across multiple organizations. [Benjamin Guttmann](https://github.com/benjaminguttmann-avtq) from SAP spearheaded [prometheus-boshrelease dependency updates](https://github.com/cloudfoundry/prometheus-boshrelease/pulls), while [Abdul Haseeb](https://github.com/abdulhaseeb2) led [comprehensive bosh_exporter modernization](https://github.com/cloudfoundry/bosh_exporter/pull/282), updating Prometheus client libraries from version 1.11.1 to 1.23.0.

This modernization ensures Cloud Foundry operators access state-of-the-art monitoring capabilities with improved security posture and performance characteristics. The work addresses multiple CVEs and introduces performance improvements for all operators using Prometheus through [CF exporter improvements](https://github.com/cloudfoundry/cf_exporter/pulls).

### Storage CLI Modernization and AWS SDK Evolution

Building on [RFC-0043: Cloud Controller Blobstore Storage-CLI Integration](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0043-cc-blobstore-storage-cli.md), the working group advanced critical storage infrastructure modernization through strategic AWS SDK upgrades. This groundbreaking RFC establishes a new "Storage CLI" area within the Foundational Infrastructure Working Group, creating collaboration framework between BOSH and CAPI teams.

Active development is underway to [upgrade BOSH S3 CLI from AWS SDK v1 to v2](https://github.com/cloudfoundry/bosh-s3cli/pull/53), addressing security and performance concerns. The modernization supports Storage CLI consolidation initiative, while [Storage CLI governance formalization](https://github.com/cloudfoundry/community/pull/1292) demonstrates strategic infrastructure importance across Cloud Foundry domains.

### Shared Infrastructure and CI/CD Modernization

The working group's infrastructure expertise extends to platform-wide operational improvements through [RFC-0041: Shared Concourse Infrastructure](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0041-shared-concourse.md), which establishes shared Concourse infrastructure for Cloud Foundry working groups. This RFC reduces operational overhead and cloud costs while improving CI/CD capabilities across the community.

The proposal directly impacts the Foundational Infrastructure Working Group's CI/CD operations and enables more efficient resource utilization. The RFC's focus on credential management using Vault aligns with the working group's expertise in identity and credential management systems.

---

*This report celebrates the collaborative achievements of the Cloud Foundry community. To contribute to future infrastructure initiatives, visit our working group repositories or join our community discussions.*