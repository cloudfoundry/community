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

The Foundational Infrastructure Working Group demonstrated sustained commitment to enterprise security through strategic UAA identity management system enhancements. [Adrian Hoelzl](https://github.com/adrianhoelzl-sap) from SAP led [comprehensive ExternalLoginAuthenticationManager component refactoring](https://github.com/cloudfoundry/uaa/pull/3607) - cloudfoundry/uaa#3607, addressing technical debt in external identity provider integrations.

The refactoring enhances UAA's complex authentication scenario handling in enterprise environments, providing better error handling and improved logging. These improvements support Cloud Foundry operators in regulated industries through [security dependency updates](https://github.com/cloudfoundry/uaa/pull/3605) - cloudfoundry/uaa#3605, reducing operational complexity for large-scale deployments.

### IPv6 Dual-Stack Implementation in Active Development

Following RFC-0038 acceptance, the Foundational Infrastructure Working Group transitioned from strategic planning to active IPv6 dual-stack implementation across core BOSH infrastructure. Active development spans [BOSH core IPv6 prefix allocation](https://github.com/cloudfoundry/bosh/pull/2611) - cloudfoundry/bosh#2611, [AWS CPI multistack networks](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/181) - cloudfoundry/bosh-aws-cpi-release#181, and [comprehensive IPv6 testing frameworks](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/53) - cloudfoundry/bosh-acceptance-tests#53.

The implementation demonstrates significant progress toward production-ready IPv6 dual-stack support with coordinated development across BOSH core, cloud providers, and testing infrastructure. This RFC-to-implementation transition showcases the working group's execution capability, positioning Cloud Foundry at modern networking standards through [NIC groups testing](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/54) - cloudfoundry/bosh-acceptance-tests#54.

### Prometheus Ecosystem Modernization and Dependency Management

The Prometheus monitoring infrastructure saw transformative modernization efforts from community contributors across multiple organizations. [Benjamin Guttmann](https://github.com/benjaminguttmann-avtq) from SAP spearheaded [prometheus-boshrelease dependency updates](https://github.com/cloudfoundry/prometheus-boshrelease/pulls) - cloudfoundry/prometheus-boshrelease, while [Abdul Haseeb](https://github.com/abdulhaseeb2) led [comprehensive bosh_exporter modernization](https://github.com/cloudfoundry/bosh_exporter/pull/282) - cloudfoundry/bosh_exporter#282, updating Prometheus client libraries from version 1.11.1 to 1.23.0.

This modernization ensures Cloud Foundry operators access state-of-the-art monitoring capabilities with improved security posture and performance characteristics. The work addresses multiple CVEs and introduces performance improvements for all operators using Prometheus through [CF exporter improvements](https://github.com/cloudfoundry/cf_exporter/pulls) - cloudfoundry/cf_exporter.

### Storage CLI Modernization and AWS SDK Evolution

The working group advanced critical storage infrastructure modernization through strategic AWS SDK upgrades and enhanced Storage CLI capabilities. Active development is underway to [upgrade BOSH S3 CLI from AWS SDK v1 to v2](https://github.com/cloudfoundry/bosh-s3cli/pull/53) - cloudfoundry/bosh-s3cli#53, addressing security, performance, and maintainability concerns while providing enhanced features and modern AWS service support.

This modernization supports the Storage CLI consolidation initiative outlined in RFC-0043, ensuring consolidated storage CLI builds on current foundations. The SDK upgrade improves S3 operations reliability for BOSH deployments, while [Storage CLI governance formalization](https://github.com/cloudfoundry/community/pull/1292) - cloudfoundry/community#1292 demonstrates strategic infrastructure importance across Cloud Foundry domains.

## Community Impact Areas

### Cross-Organizational Collaboration

The period demonstrated exceptional cross-organizational collaboration, with contributors from SAP, 9 Elements, He Group, and VMware Tanzu working together on shared infrastructure challenges. This collaboration model exemplifies the open-source values of the Cloud Foundry community and ensures that improvements benefit all platform users regardless of their organizational affiliation.

### Multi-Cloud Infrastructure Maturity

Significant progress was made in achieving feature parity across cloud providers, particularly with the AliCloud Noble stemcell support and storage CLI improvements across AWS, Azure, and Google Cloud Platform. This work ensures that Cloud Foundry operators can choose cloud providers based on business requirements rather than platform limitations.

### Security and Compliance Enhancement

The Prometheus dependency modernization and storage CLI improvements collectively address numerous CVEs and enhance the security posture of Cloud Foundry deployments. The community's proactive approach to dependency management demonstrates commitment to enterprise-grade security standards.

### Operational Excellence

Infrastructure annotations, improved error handling, and enhanced logging capabilities across multiple components improve the operational experience for Cloud Foundry platform teams. These improvements reduce troubleshooting time and provide better visibility into platform health.

## Activity Breakdown by Technology Area

| Area | Repositories Active | Pull Requests | Issues | Key Focus |
|------|-------------------|---------------|--------|-----------|
| IPv6 Dual-Stack Implementation | 3 | 4 | 0 | Active BOSH core, AWS CPI, and testing development |
| Identity Management (UAA) | 1 | 2 | 0 | External authentication refactoring, security updates |
| Storage CLI Modernization | 1 | 1 | 0 | AWS SDK v2 migration, infrastructure evolution |
| Prometheus (BOSH) | 5 | 55 | 6 | Dependency modernization, security updates |
| **Total Activity** | **10** | **62** | **6** | **Platform networking evolution and infrastructure modernization** |

## Recent RFC Developments

### RFC-0038: IPv6 Dual Stack Support for Cloud Foundry

**Status**: Accepted  
**Authors**: @peanball, @a-hassanin, @fmoehler, @dimitardimitrov13, @plamen-bardarov
**RFC Pull Request**: [community#1077](https://github.com/cloudfoundry/community/pull/1077)

This groundbreaking RFC represents the most significant networking evolution in Cloud Foundry's recent history, establishing comprehensive IPv6 dual-stack support across the entire platform. The RFC addresses the growing prevalence of IPv6 in enterprise networks and positions Cloud Foundry at the forefront of modern networking standards.

The proposal introduces fundamental architectural improvements including individual IPv6 addresses for application containers, elimination of NAT requirements for IPv6 traffic, and enhanced security through native addressing. The dual-stack approach ensures smooth migration paths for existing IPv4 deployments while enabling next-generation networking capabilities.

Key technical innovations include BOSH IPv6 prefix delegation, Diego container runtime evolution to native IPv6 addressing, Silk CNI dual-stack operation, and comprehensive Application Security Group IPv6 support. The RFC's acceptance creates immediate opportunities for community contribution across BOSH, Diego, networking, and testing components.

### RFC-0043: Cloud Controller Blobstore Storage-CLI Integration

**Status**: Accepted  
**Authors**: Johannes Haass (@johha), Stephan Merker (@stephanme)

This groundbreaking RFC establishes a new "Storage CLI" area within the Foundational Infrastructure Working Group, creating a framework for collaboration between BOSH and CAPI teams. The RFC proposes replacing the unmaintained fog gem family with BOSH's proven storage CLI tools, addressing critical technical debt in Cloud Controller's blobstore handling.

The RFC represents strategic architectural evolution that consolidates storage infrastructure across Cloud Foundry components, reducing maintenance overhead and improving reliability. The creation of the Storage CLI area enables structured collaboration between traditionally separate working groups, demonstrating the platform's commitment to architectural coherence.

### RFC-0041: Shared Concourse Infrastructure

**Status**: Accepted  
**Author**: Derek Richardson (@drich10)

This RFC establishes shared Concourse infrastructure for Cloud Foundry working groups, reducing operational overhead and cloud costs while improving CI/CD capabilities. The proposal directly impacts the Foundational Infrastructure Working Group's CI/CD operations and enables more efficient resource utilization across the community.

The RFC's focus on credential management using Vault aligns with the working group's expertise in identity and credential management systems, creating opportunities for cross-pollination between Concourse and CredHub teams.

---

*This report celebrates the collaborative achievements of the Cloud Foundry community. To contribute to future infrastructure initiatives, visit our working group repositories or join our community discussions.*