---
title: "Foundational Infrastructure Working Group Update"
date: "2025-09-02"
period: "June 2025 - September 2025"
---

# Foundational Infrastructure Working Group Update

## Summary

The Foundational Infrastructure Working Group achieved significant progress in both strategic vision and concrete implementation, transitioning from RFC acceptance to active development of IPv6 dual-stack support while advancing critical identity management and storage infrastructure modernization. This period demonstrates the community's ability to execute on ambitious architectural initiatives while maintaining operational excellence across core platform services.

The most significant achievement was the transition of IPv6 dual-stack support from strategic planning to active implementation, with substantial development progress across BOSH core infrastructure, AWS Cloud Provider Interface, and comprehensive testing frameworks. Parallel efforts in UAA identity management modernization and Storage CLI AWS SDK evolution demonstrate the working group's commitment to both next-generation capabilities and current operational excellence.

Key collaborative contributions came from SAP through UAA architectural improvements and continued Prometheus ecosystem modernization, while community members advanced storage infrastructure through AWS SDK v2 migration and cross-working group governance enhancements. The period showcases effective coordination between strategic initiatives and practical implementation work.

This update celebrates the working group's transformation from RFC planning to active development execution, positioning Cloud Foundry's foundational infrastructure at the forefront of modern networking standards while strengthening identity management and storage capabilities that serve the entire platform ecosystem.

## Major Strategic Initiatives

### Identity and Credential Management Modernization

The Foundational Infrastructure Working Group demonstrated sustained commitment to enterprise security through strategic enhancements to the UAA identity management system, representing critical improvements to Cloud Foundry's authentication and authorization infrastructure. Adrian Hoelzl (@adrianhoelzl-sap, SAP) led architectural improvements with a comprehensive refactoring of the ExternalLoginAuthenticationManager component, addressing technical debt in UAA's integration with external identity providers and improving code maintainability for enterprise deployments relying on SAML, LDAP, and OAuth2 integrations.

The refactoring initiative enhances UAA's ability to handle complex authentication scenarios common in enterprise environments, providing better error handling, improved logging for troubleshooting authentication issues, and enhanced compatibility with modern identity standards. These improvements directly support Cloud Foundry operators in highly regulated industries where robust identity management is paramount, reducing operational complexity for platform teams managing large-scale deployments while maintaining the security standards expected in enterprise environments.

**Related Work**:
- [UAA ExternalLoginAuthenticationManager Refactoring](https://github.com/cloudfoundry/uaa/pull/3607)
- [UAA Security Dependency Updates](https://github.com/cloudfoundry/uaa/pull/3605)

### IPv6 Dual-Stack Implementation in Active Development

Following the acceptance of RFC-0038: "IPv6 Dual Stack Support for Cloud Foundry", the Foundational Infrastructure Working Group has transitioned from strategic planning to active implementation, with substantial development progress across core BOSH infrastructure components. The community has made significant progress implementing the IPv6 dual-stack architecture, with active pull requests spanning BOSH core infrastructure (PR #2611 for IPv6 prefix allocation), AWS Cloud Provider Interface (PR #181 for multistack networks and prefix support), and comprehensive testing frameworks including dedicated acceptance tests for IPv6 functionality.

The active implementation demonstrates significant progress toward production-ready IPv6 dual-stack support, with coordinated development across BOSH core, cloud provider interfaces, and testing infrastructure ensuring enterprise reliability standards. This transition from RFC acceptance to active implementation showcases the working group's ability to execute on strategic initiatives, positioning Cloud Foundry at the forefront of modern networking standards while maintaining operational continuity for existing deployments.

**Related Work**:
- [BOSH IPv6 Prefix Allocation Implementation](https://github.com/cloudfoundry/bosh/pull/2611)
- [AWS CPI Multistack Support](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/181)
- [IPv6 Prefix Allocation Tests](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/53)
- [NIC Groups Testing](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/54)

### Prometheus Ecosystem Modernization and Dependency Management

The Prometheus monitoring infrastructure saw transformative modernization efforts led by community contributors from multiple organizations, representing one of the most significant infrastructure improvements of the period. Benjamin Guttmann (@benjaminguttmann-avtq, SAP) spearheaded dependency updates in prometheus-boshrelease, while Abdul Haseeb led comprehensive modernization in bosh_exporter, updating core Prometheus client libraries from version 1.11.1 to 1.23.0. The community delivered 55 pull requests across five repositories, with 43 automated dependency management updates ensuring security libraries and monitoring dependencies remained current.

This modernization effort ensures that Cloud Foundry operators have access to state-of-the-art monitoring capabilities with improved security posture and performance characteristics, eliminating technical debt that could have hindered future platform evolution. The work addresses multiple CVEs, introduces performance improvements benefiting all Cloud Foundry operators using Prometheus, and establishes a foundation for advanced observability features that support enterprise-grade monitoring requirements.

**Related Work**: 
- [Prometheus BOSH Release Updates](https://github.com/cloudfoundry/prometheus-boshrelease/pulls)
- [BOSH Exporter Modernization](https://github.com/cloudfoundry/bosh_exporter/pull/282)
- [CF Exporter Improvements](https://github.com/cloudfoundry/cf_exporter/pulls)

### Storage CLI Modernization and AWS SDK Evolution

The working group advanced critical storage infrastructure modernization through strategic AWS SDK upgrades and enhanced Storage CLI capabilities, building on the foundation established by RFC-0043's Storage CLI area creation. Active development is underway to upgrade the BOSH S3 CLI from AWS SDK for Go v1 to v2, representing a major modernization effort that addresses security, performance, and maintainability concerns while providing enhanced security features, improved performance characteristics, and better support for modern AWS services.

This modernization work directly supports the Storage CLI consolidation initiative outlined in RFC-0043, ensuring that the consolidated storage CLI will be built on current, well-supported foundations rather than legacy dependencies. The SDK upgrade improves the reliability of S3 operations critical to BOSH deployments, including stemcell distribution and release management, while the formalization of Storage CLI governance through cross-working group collaboration demonstrates the strategic importance of storage infrastructure across multiple Cloud Foundry domains.

**Related Work**:
- [AWS SDK v2 Migration](https://github.com/cloudfoundry/bosh-s3cli/pull/53)
- [Storage CLI Governance](https://github.com/cloudfoundry/community/pull/1292)
- [RFC-0043: Storage CLI Integration](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0043-cc-blobstore-storage-cli.md)

## Community Impact Areas

### Cross-Organizational Collaboration

The period demonstrated exceptional cross-organizational collaboration, with contributors from SAP, 9 Elements, He Group, and VMware Tanzu working together on shared infrastructure challenges. This collaboration model exemplifies the open-source values of the Cloud Foundry community and ensures that improvements benefit all platform users regardless of their organizational affiliation.

### Multi-Cloud Infrastructure Maturity

Significant progress was made in achieving feature parity across cloud providers, particularly with the AliCloud Noble stemcell support and storage CLI improvements across AWS, Azure, and Google Cloud Platform. This work ensures that Cloud Foundry operators can choose cloud providers based on business requirements rather than platform limitations.

### Security and Compliance Enhancement

The Prometheus dependency modernization and storage CLI improvements collectively address numerous CVEs and enhance the security posture of Cloud Foundry deployments. The community's proactive approach to dependency management demonstrates commitment to enterprise-grade security standards.

### Operational Excellence

Infrastructure annotations, improved error handling, and enhanced logging capabilities across multiple components improve the operational experience for Cloud Foundry platform teams. These improvements reduce troubleshooting time and provide better visibility into platform health.

## Community Contributors Recognition

We celebrate the diverse community that drives strategic infrastructure evolution and operational excellence:

**IPv6 Dual-Stack Implementation Leaders**:
- **RFC Authors**: @peanball, @a-hassanin, @fmoehler, @dimitardimitrov13, @plamen-bardarov - Strategic vision and architecture
- **Implementation Contributors**: Active development across BOSH core, AWS CPI, and testing infrastructure

**Identity and Security Excellence**:
- **Adrian Hoelzl** (@adrianhoelzl-sap, SAP) - UAA external authentication architecture improvements
- **Benjamin Guttmann** (@benjaminguttmann-avtq, SAP) - Prometheus ecosystem modernization leadership

**Storage Infrastructure Modernization**:
- **Community Contributors** - AWS SDK v2 migration and storage CLI evolution
- **Cross-WG Collaboration** - ARI and FI working group Storage CLI governance

**Prometheus Ecosystem Maintainers**:
- **Abdul Haseeb** (@abdulhaseeb2) - Prometheus client modernization
- **Gilles Miraillet** (@gmllt) - CF exporter functionality improvements
- **Sascha Stojanovic** (@scult) - Testing infrastructure contributions

**Organizational Recognition**: Special acknowledgment to SAP for substantial contributions across UAA, Prometheus, and strategic initiatives, demonstrating sustained commitment to Cloud Foundry's foundational infrastructure evolution.

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

## Looking Forward: Opportunities for Community Involvement

### IPv6 Dual-Stack Implementation Initiative

The acceptance of RFC-0038 creates immediate and high-impact opportunities for community members to contribute to the most significant networking evolution in Cloud Foundry's history. The implementation requires coordinated work across multiple components:

**BOSH Infrastructure Enhancements**:
- IPv6 prefix delegation implementation in BOSH Director
- Cloud Provider Interface (CPI) extensions for AWS, Azure, GCP, and other providers following the AWS dual-stack pattern
- BOSH Agent enhancements for IPv6 CIDR assignment and network interface configuration
- Ubuntu Noble stemcell IPv6 enablement and testing

**Diego Container Runtime Evolution**:
- Silk CNI dual-stack support with host-local IPAM IPv6 integration
- Application Security Groups (ASGs) extension for IPv6 and ICMPv6 protocol support
- Container identity certificate enhancements for IPv6 addresses
- Environment variable extensions for CF_INSTANCE_IP IPv6 equivalents

**Networking and Routing Components**:
- Gorouter IPv6 endpoint and traffic handling verification
- TCP-Router and Routing API IPv6 address support
- Policy Server IPv6 network policy management
- Application Security Group CLI and API IPv6 configuration support

**Testing and Validation Framework**:
- Cloud Foundry Acceptance Tests (CATs) IPv6 test suite development
- bosh-bootstrap (bbl) IPv6/dual-stack environment configuration
- cf-deployment experimental ops-files and validation pipelines
- Integration testing across the complete dual-stack workflow

### Storage CLI Consolidation Initiative

The approved RFC-0043 creates immediate opportunities for community members to contribute to the new Storage CLI area. The initiative requires:
- Consolidation of existing BOSH storage CLIs into a unified repository
- Implementation of Cloud Controller-specific commands (copy, list, properties)
- Enhanced configuration parameter support for enterprise deployments
- Cross-team collaboration between BOSH and CAPI communities

### Prometheus Observability Enhancement

Building on the substantial dependency modernization work, opportunities exist for:
- Advanced metric collection improvements for Cloud Foundry-specific workloads  
- Integration with OpenTelemetry collectors as outlined in RFC-0018
- Performance optimization for large-scale Cloud Foundry deployments
- Custom dashboard and alerting rule development for operational scenarios

### Multi-Cloud Infrastructure Expansion

The success of AliCloud Noble stemcell support creates templates for:
- Additional cloud provider integration following established patterns
- Stemcell support for emerging cloud platforms
- Infrastructure annotation standardization across all supported providers
- Enhanced deployment automation for hybrid and multi-cloud scenarios

### Identity and Credential Management Evolution

Opportunities exist in UAA and CredHub modernization:
- Integration with modern identity standards and protocols
- Enhanced security features for enterprise compliance requirements
- Performance improvements for large-scale identity operations
- Migration tools for operators transitioning between authentication systems

The Foundational Infrastructure Working Group continues to provide the robust, secure, and flexible foundation that enables Cloud Foundry's position as the premier platform for enterprise application deployment and management. We invite community members to join these initiatives and contribute to the next phase of Cloud Foundry's infrastructure evolution.

---

*This report celebrates the collaborative achievements of the Cloud Foundry community. To contribute to future infrastructure initiatives, visit our working group repositories or join our community discussions.*