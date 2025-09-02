---
title: "Foundational Infrastructure Working Group Update"
date: "2025-09-02"
period: "June 2025 - September 2025"
---

# Foundational Infrastructure Working Group Update

## Summary

The Foundational Infrastructure Working Group achieved a historic milestone with the acceptance of RFC-0038 for IPv6 dual-stack support, representing the most significant networking evolution in Cloud Foundry's recent history. This landmark initiative, combined with continued collaborative innovations in monitoring, cloud provider expansion, and storage infrastructure, demonstrates the community's commitment to positioning Cloud Foundry at the forefront of modern platform capabilities.

Over the past three months (June-September 2025), our community delivered transformative advancements across multiple domains: groundbreaking IPv6 dual-stack architecture that future-proofs Cloud Foundry networking, substantial Prometheus ecosystem modernization enhancing observability capabilities, expanded AliCloud infrastructure support with Noble stemcell compatibility, and strategic storage CLI consolidation through RFC-0043 approval.

The period was marked by exceptional cross-organizational collaboration, with key contributions from SAP, 9 Elements, He Group, VMware Tanzu, and the broader Cloud Foundry community. The acceptance of RFC-0038 creates immediate opportunities for community involvement in implementing next-generation networking capabilities while maintaining operational continuity for existing deployments.

This update celebrates both the visionary strategic initiatives like IPv6 dual-stack support and the dedicated engineering efforts that continue to advance Cloud Foundry's infrastructure automation, multi-cloud deployment capabilities, and core services that enable operators to deploy and manage Cloud Foundry at global scale.

## Major Strategic Initiatives

### IPv6 Dual-Stack Infrastructure Implementation

The Foundational Infrastructure Working Group achieved a landmark milestone with the acceptance of RFC-0038: "IPv6 Dual Stack Support for Cloud Foundry", representing the most significant networking evolution in Cloud Foundry's recent history. This groundbreaking initiative positions Cloud Foundry at the forefront of modern networking standards while maintaining backward compatibility with existing IPv4 deployments.

**Key Contributors**: The RFC was authored by a collaborative team including @peanball, @a-hassanin, @fmoehler, @dimitardimitrov13, and @plamen-bardarov, demonstrating the cross-organizational commitment to this strategic platform enhancement.

**RFC Status**: Accepted (RFC-0038) - [Community PR #1077](https://github.com/cloudfoundry/community/pull/1077)

The RFC addresses the growing prevalence of IPv6 on the internet and in enterprise networks, proposing comprehensive dual-stack support that allows Cloud Foundry foundations to operate with both IPv4 and IPv6 simultaneously. This additive approach ensures smooth migration paths for existing deployments while enabling new installations to leverage IPv6's enhanced addressing capabilities and security features.

**Strategic Architecture Changes**:

The initiative introduces fundamental architectural improvements across the entire Cloud Foundry stack:

- **BOSH Infrastructure**: Enhanced to support IPv6 prefix delegation, allowing assignment of IPv6 CIDR ranges (e.g., /80 prefixes) to individual VMs. This enables efficient IPv6 address management without the complexity of central IP allocation systems.

- **Diego Container Runtime**: Transformation from overlay-dependent networking to native IPv6 addressing for application containers. Each application instance receives its own IPv6 address, improving traffic correlation and security while eliminating NAT requirements for egress traffic.

- **Silk CNI Evolution**: Extended to support dual-stack operation with the host-local CNI plugin managing IPv6 address allocation within cells, providing state management and conflict prevention.

- **Security Framework**: Application Security Groups (ASGs) enhanced with IPv6 support, including ICMPv6 protocol handling and proper firewall rule management via ip6tables.

**Cloud Provider Integration**: The RFC mandates IPv6 support across all Cloud Provider Interfaces (CPIs), with AWS CPI already implementing dual-stack capabilities and other providers following established patterns.

**Operational Benefits**:
- Elimination of NAT requirements for IPv6 traffic, reducing complexity and improving performance
- Individual IPv6 addresses for application instances, enhancing security and monitoring capabilities  
- Future-proofing against IPv4 address exhaustion
- Enhanced compatibility with modern enterprise networks increasingly adopting IPv6

**Implementation Roadmap**: The RFC establishes a phased implementation approach with experimental ops-files for cf-deployment, comprehensive testing frameworks including CAT extensions, and validation pipelines to ensure production readiness.

**Strategic Impact**: This initiative positions Cloud Foundry as a leader in modern networking standards, enabling operators to leverage IPv6's benefits while maintaining operational continuity. The dual-stack approach ensures that Cloud Foundry remains relevant for next-generation networking requirements while preserving investment in existing IPv4 infrastructure.

The acceptance of RFC-0038 creates immediate opportunities for community contribution across BOSH, Diego, networking, and testing components, representing one of the most comprehensive platform enhancements in Cloud Foundry's evolution.

**Related Work**:
- [RFC-0038: IPv6 Dual Stack Support](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0038-ipv6-dual-stack-for-cf.md)
- [AWS CPI Dual Stack Implementation](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/174)
- [BOSH Agent Network Enhancements](https://github.com/cloudfoundry/bosh-agent/pull/344)

### Prometheus Ecosystem Modernization and Dependency Management

The Prometheus monitoring infrastructure saw transformative modernization efforts led by community contributors from multiple organizations. This initiative represents one of the most significant infrastructure improvements of the period, ensuring the reliability and security of Cloud Foundry's observability stack.

**Key Contributors**: Benjamin Guttmann (@benjaminguttmann-avtq, SAP), Gilles Miraillet (@gmllt), Abdul Haseeb (@abdulhaseeb2), Sascha Stojanovic (@scult), and the broader Prometheus community through automated dependency management.

The community delivered substantial updates across the entire Prometheus ecosystem with 55 pull requests merged across five repositories. The initiative focused on three critical areas: dependency modernization, security hardening, and platform compatibility improvements. Benjamin Guttmann spearheaded dependency updates in prometheus-boshrelease, ensuring compatibility with the latest Prometheus server versions while maintaining backward compatibility for existing deployments.

Abdul Haseeb led a comprehensive modernization effort in bosh_exporter, updating core Prometheus client libraries from version 1.11.1 to 1.23.0 and prometheus/common from 0.26.0 to 0.65.0. This work required careful compatibility testing and code adjustments to ensure seamless operation with Cloud Foundry's BOSH infrastructure. The updates addressed multiple CVEs and introduced performance improvements that benefit all Cloud Foundry operators using Prometheus for monitoring.

The community's commitment to security was evident through extensive automated dependency management, with 43 pull requests from Dependabot ensuring that test frameworks, security libraries, and monitoring dependencies remained current. Gilles Miraillet contributed critical fixes to cf_exporter, enhancing its ability to collect metrics from Cloud Foundry components reliably.

**Strategic Impact**: This modernization effort ensures that Cloud Foundry operators have access to state-of-the-art monitoring capabilities with improved security posture and performance characteristics. The work eliminates technical debt that could have hindered future platform evolution and establishes a foundation for advanced observability features.

**Related Work**: 
- [Prometheus BOSH Release Updates](https://github.com/cloudfoundry/prometheus-boshrelease/pulls)
- [BOSH Exporter Modernization](https://github.com/cloudfoundry/bosh_exporter/pull/282)
- [CF Exporter Improvements](https://github.com/cloudfoundry/cf_exporter/pulls)

### AliCloud Infrastructure Expansion and Noble Stemcell Support

The community achieved a significant milestone in multi-cloud support through expanded AliCloud infrastructure capabilities, led by He Guimin (@xiaozhu36) from He Group. This initiative demonstrates Cloud Foundry's commitment to global cloud provider support and platform accessibility.

**Key Contributor**: He Guimin (@xiaozhu36, He Group) provided comprehensive AliCloud infrastructure enhancements, including Noble stemcell support and infrastructure annotations.

The effort began with implementing support for Ubuntu Noble (24.04 LTS) stemcells on AliCloud, a critical step in maintaining platform currency with long-term support operating system releases. He Guimin's work in bosh-alicloud-light-stemcell-builder enables Cloud Foundry operators in AliCloud environments to leverage the latest Ubuntu LTS distribution with enhanced security features and improved performance characteristics.

The implementation included comprehensive infrastructure annotations that improve deployment visibility and management capabilities for AliCloud operators. These annotations provide essential metadata for resource management, cost tracking, and operational monitoring in AliCloud environments. The work ensures that AliCloud deployments achieve feature parity with other major cloud providers in the Cloud Foundry ecosystem.

The stemcells-alicloud-index repository received coordinated updates to publish both Noble (1.25) and Jammy (1.894) stemcells, ensuring operators have access to both current and stable stemcell options. This dual-track approach provides flexibility for operators managing different upgrade cadences while maintaining security and functionality.

**Strategic Impact**: This expansion significantly enhances Cloud Foundry's global reach, particularly in Asian markets where AliCloud has strong presence. The Noble stemcell support positions AliCloud deployments at the forefront of operating system modernization, while the infrastructure annotations improve operational visibility for enterprise deployments.

**Related Work**:
- [Noble Stemcell Support](https://github.com/cloudfoundry/bosh-alicloud-light-stemcell-builder/pull/23)
- [Infrastructure Annotations](https://github.com/cloudfoundry/bosh-alicloud-light-stemcell-builder/pull/24)
- [Stemcell Publishing](https://github.com/cloudfoundry/stemcells-alicloud-index/pulls)

### Storage Infrastructure Modernization and CLI Consolidation

The working group advanced a critical modernization initiative for storage infrastructure through enhanced BOSH storage CLI capabilities, with contributions from multiple community members addressing both immediate operational needs and long-term architectural evolution.

**Key Contributors**: Katharina Przybill (@kathap, SAP), Yuri Bykov (@ybykov-a9s, 9 Elements), Ned Petrov (@neddp), and Parthiv Menon (@parthivrmenon) collaborated on modernizing storage CLI tools across multiple cloud providers.

The initiative focused on enhancing storage CLI tools that provide the foundation for BOSH's multi-cloud storage capabilities. Katharina Przybill led improvements to bosh-azure-storage-cli, addressing compatibility issues and enhancing Azure Blob Storage integration reliability. These improvements are particularly significant as they directly support the upcoming storage-cli blobstore type proposed in RFC-0043.

Yuri Bykov contributed enhancements to bosh-s3cli, improving AWS S3 compatibility and error handling mechanisms. The work addresses edge cases in S3 operations that could impact BOSH deployment reliability and introduces better logging for troubleshooting storage-related issues. Ned Petrov provided critical testing and validation for gcscli improvements, ensuring Google Cloud Storage operations maintain reliability standards.

Parthiv Menon contributed to Azure storage CLI reliability improvements, focusing on handling network interruptions and retry mechanisms that are essential for production deployments. The collective work establishes a robust foundation for the proposed storage-cli consolidation outlined in RFC-0043.

**Strategic Impact**: These improvements provide immediate operational benefits for BOSH deployments across all major cloud providers while laying groundwork for the strategic storage CLI consolidation initiative. The work reduces deployment failures related to storage operations and improves troubleshooting capabilities for operators.

**Related Work**:
- [Azure Storage CLI Improvements](https://github.com/cloudfoundry/bosh-azure-storage-cli/pulls)
- [S3 CLI Enhancements](https://github.com/cloudfoundry/bosh-s3cli/pulls)
- [GCS CLI Reliability](https://github.com/cloudfoundry/bosh-gcscli/pulls)

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

We celebrate the diverse and collaborative community that drives Cloud Foundry's foundational infrastructure forward:

- **Benjamin Guttmann** (@benjaminguttmann-avtq, SAP) - Led Prometheus ecosystem modernization
- **He Guimin** (@xiaozhu36, He Group) - Expanded AliCloud infrastructure capabilities  
- **Katharina Przybill** (@kathap, SAP) - Advanced Azure storage infrastructure
- **Yuri Bykov** (@ybykov-a9s, 9 Elements) - Enhanced AWS S3 storage reliability
- **Abdul Haseeb** (@abdulhaseeb2) - Contributed to Prometheus client modernization
- **Gilles Miraillet** (@gmllt) - Improved CF exporter functionality
- **Sascha Stojanovic** (@scult) - Contributed to Prometheus testing infrastructure
- **Ned Petrov** (@neddp) - Validated GCS CLI improvements
- **Parthiv Menon** (@parthivrmenon) - Enhanced Azure storage CLI reliability

Special recognition goes to the organizations that enable these contributions: SAP for substantial Prometheus and Azure infrastructure work, 9 Elements for storage CLI improvements, and He Group for AliCloud platform expansion.

## Activity Breakdown by Technology Area

| Area | Repositories Active | Pull Requests | Issues | Key Focus |
|------|-------------------|---------------|--------|-----------|
| IPv6 Dual-Stack | 1 (RFC) | 1 | 0 | Platform networking evolution, dual-stack architecture |
| Prometheus (BOSH) | 5 | 55 | 6 | Dependency modernization, security updates |
| Storage CLI | 4 | 8 | 2 | Multi-cloud storage reliability |
| AliCloud Infrastructure | 2 | 4 | 0 | Noble stemcell support, infrastructure annotations |
| **Total Activity** | **12** | **68** | **8** | **Platform modernization and networking evolution** |

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