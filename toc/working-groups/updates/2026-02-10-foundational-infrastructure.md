---
title: "Foundational Infrastructure Working Group Update"
date: 2026-02-10
period: September 2, 2025 - February 10, 2026
---

# Foundational Infrastructure Working Group Update

This update covers activity from September 2, 2025 to February 10, 2026, encompassing 3,097 commits, 1,239 merged pull requests, 84 issues, and 125 releases across 110 repositories.

## In-Progress RFC: Dynamic Disks Support in BOSH

[Maria Shaldybin](https://github.com/mariash) submitted [RFC: Dynamic Disks Support in BOSH](https://github.com/cloudfoundry/community/pull/1401), proposing native support for dynamic disk allocation in BOSH deployments. This RFC addresses operator needs for more flexible storage management and is currently under review by the working group.

## Ubuntu Noble Stemcell Migration

The working group achieved a major milestone with the [Noble cut over](https://github.com/cloudfoundry/bosh/pull/2655) in BOSH Director, transitioning Cloud Foundry's infrastructure foundation to Ubuntu 24.04 LTS. This multi-month effort involved coordinated changes across the entire BOSH ecosystem. [Aram Price](https://github.com/aramprice) led the migration, contributing 209 commits across VM deployment lifecycle repositories.

Cross-CPI Noble migration progressed systematically:
- **AWS**: [Noble stemcell transition](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/198) and [CI pipeline updates](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/193)
- **Azure**: [Noble switch](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/730) with [NTP server configuration updates](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/733)
- **vSphere**: [VsphereGuestInfo settings source](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/pull/467) for Noble stemcells
- **Google Cloud**: [Noble CPI image adoption](https://github.com/cloudfoundry/bosh-package-golang-release/pull/34)

The latest stemcell releases include Ubuntu Noble v1.215 and Ubuntu Jammy v1.1044, with [NVMe output fixes](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/pull/462) ensuring proper instance storage discovery on Noble.

## IPv6 Dual-Stack Networking Progress

Significant progress was made on RFC-0038 IPv6 dual-stack support. [Comprehensive documentation](https://github.com/cloudfoundry/docs-bosh/pull/891) now covers dual-stack networking, prefix delegation, and network interface groups. The AWS CPI received [multistack network and prefix support](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/181), enabling IPv4/IPv6 dual-stack deployments.

Supporting infrastructure changes include:
- BOSH Director [network prefix settings](https://github.com/cloudfoundry/bosh/pull/2641) for dynamic and VIP networks
- [Prefix stringification](https://github.com/cloudfoundry/bosh/pull/2629) for proper network configuration
- [IPv6 acceptance tests](https://github.com/cloudfoundry/bosh-acceptance-tests/pull/53) for AWS prefix and IPv6 allocation
- [IPv6 rsyslog UDP listener support](https://github.com/cloudfoundry/syslog-release/pull/231) for gorouter

## BOSH Infrastructure Modernization

BOSH continues to lead Cloud Foundry's infrastructure modernization with 1,851 commits and 458 pull requests across VM deployment lifecycle repositories. Major releases include BOSH Director v282.1.2, BOSH CLI v7.9.17, and BPM v1.4.24.

Key improvements this period:
- **BOSH Agent**: [NVMe instance storage discovery fixes](https://github.com/cloudfoundry/bosh-agent/pull/400), [configurable VMware tool paths](https://github.com/cloudfoundry/bosh-agent/pull/398), and [VsphereGuestInfo settings source](https://github.com/cloudfoundry/bosh-agent/pull/392)
- **vSphere CPI**: [Device groups support](https://github.com/cloudfoundry/bosh-vsphere-cpi-release/pull/440) and [NSX-T policy migration fixes](https://github.com/cloudfoundry/bosh-vsphere-cpi-release/pull/444)
- **Docker CPI**: 12 releases (v0.0.30 to v0.2.2) with substantial improvements for local development
- **BBL**: 5 releases including [IPv6-compatible NLB support for AWS](https://github.com/cloudfoundry/bosh-bootloader/pull/644)

[Chris Selzo](https://github.com/selzoc) contributed 58 commits while reviewers [Ivaylo Ivanov](https://github.com/ivaylogi98) (40 commits) and [Ned Petrov](https://github.com/neddp) (38 commits) provided strong code review support. [Brian Upton](https://github.com/ystros) contributed 36 commits across disaster recovery and BOSH components.

## Identity and Authentication (UAA)

The UAA ecosystem delivered substantial updates with 276 commits, 282 pull requests, and 4 major releases (v78.4.0 through v78.7.0). [Duane May](https://github.com/duanemay) led modernization efforts with 98 commits spanning dependency updates and security enhancements.

Notable UAA improvements:
- **Database migrations**: [Flyway upgrade](https://github.com/cloudfoundry/uaa/pull/3698) and [refactoring](https://github.com/cloudfoundry/uaa/pull/3712) for long-term maintainability
- **SAML enhancements**: [NameID Format in LogoutRequest](https://github.com/cloudfoundry/uaa/pull/3718) and [metadata EntityID URL fix](https://github.com/cloudfoundry/uaa/pull/3662)
- **OIDC improvements**: [omitIdTokenHintOnLogout flag](https://github.com/cloudfoundry/uaa/pull/3711) for flexible logout handling
- **OAuth fixes**: [Authorization code flow fix](https://github.com/cloudfoundry/uaa/pull/3643) and [JWT client authentication improvements](https://github.com/cloudfoundry/uaa/pull/3577)
- **Performance**: [Group membership index](https://github.com/cloudfoundry/uaa/pull/3679) on identity_zone_id and origin
- **Debugging**: [OpenID scope logging](https://github.com/cloudfoundry/uaa/pull/3727) and [SCIM DateTime filter timezone parsing fix](https://github.com/cloudfoundry/uaa/pull/3700)
- **Extensibility**: [Optional UaaTokenEnhancer injection](https://github.com/cloudfoundry/uaa/pull/3686) and [StatsDClient bean exposure](https://github.com/cloudfoundry/uaa/pull/3716)

The UAA-CLI received [go-uaa library updates](https://github.com/cloudfoundry/go-uaa/pull/133) and the UAAC gem got [Rack 3.2 compatibility](https://github.com/cloudfoundry/cf-uaac/pull/150).

## Credential Management (CredHub)

The CredHub ecosystem delivered 150 commits and 86 merged PRs across credential management repositories. Spring Boot was upgraded through multiple versions (3.5.5 to 3.5.9) along with Flyway (11.11.2 to 11.20.0) and Kotlin (2.2.10 to 2.2.21).

Security and functionality improvements include:
- [Default key_usage for CA certificate generation](https://github.com/cloudfoundry/credhub/pull/1010)
- [Extended key usage for dev TLS certificates](https://github.com/cloudfoundry/credhub/pull/1006)
- [Fix for exclude_upper parameter processing](https://github.com/cloudfoundry/credhub/pull/1031)
- [Migration from unmaintained gopkg.in/yaml.v3](https://github.com/cloudfoundry/credhub-cli/pull/132) to the maintained fork

CredHub CLI releases 2.9.50 through 2.9.53 delivered regular security updates and dependency modernization.

## Disaster Recovery (BBR)

The BBR ecosystem delivered 184 commits and 74 merged PRs, with releases for backup-and-restore-sdk (v1.19.46-48) and bosh-backup-and-restore (v1.9.75). The team modernized CI infrastructure extensively:
- [Concourse 8.0 pipeline updates](https://github.com/cloudfoundry/backup-and-restore-sdk-release/pull/1873)
- [Migration to cfd-lite and tas-lite environments](https://github.com/cloudfoundry/backup-and-restore-sdk-release/pull/1854)
- [Removal of non-OSS CVE scanning tooling](https://github.com/cloudfoundry/backup-and-restore-sdk-release/pull/1868)
- [Shepherd v2 migration](https://github.com/cloudfoundry/bosh-backup-and-restore/pull/1587)

Database compatibility updates include MySQL 8.0.39, PostgreSQL 15.8/13.16, and MariaDB 10.6.19 support.

## Database and Monitoring Infrastructure

MySQL and PostgreSQL database releases demonstrate continuous improvement with 143 commits across integrated database repositories. Notable releases include mysql-monitoring-release v10.30.0 through v10.34.0 and pxc-release updates for MySQL 8.4 compatibility.

The Prometheus BOSH ecosystem delivered 130 commits, 150 pull requests, and 7 releases including prometheus-boshrelease v31.0.0 and v31.1.0. The [bosh_exporter](https://github.com/cloudfoundry/bosh_exporter), [cf_exporter](https://github.com/cloudfoundry/cf_exporter), and [firehose_exporter](https://github.com/cloudfoundry/firehose_exporter) received regular updates for improved observability.

System logging infrastructure received 186 commits with syslog-release advancing through v12.3.10 to v12.3.14 and windows-syslog-release reaching v1.3.11. [IPv6 UDP rsyslog listener support](https://github.com/cloudfoundry/syslog-release/pull/231) enables modern network deployments.

## Community Growth and Role Management

The working group welcomed new approvers and reviewers strengthening technical leadership:
- [Maria Shaldybin](https://github.com/mariash) as [BOSH approver](https://github.com/cloudfoundry/community/pull/1413)
- [Maya Rosecrance](https://github.com/mrosecrance) with [FI approver status](https://github.com/cloudfoundry/community/pull/1391)
- [Rene Dollevoet](https://github.com/lodener) as [Stemcell Release Engineering reviewer](https://github.com/cloudfoundry/community/pull/1406)
- [Harry Metske](https://github.com/metskem) as [Stemcell Release Engineering reviewer](https://github.com/cloudfoundry/community/pull/1398)
- [Matt Kocher](https://github.com/mkocher) added to [VM deployment lifecycle](https://github.com/cloudfoundry/community/pull/1390)

[Hongchol Sinn](https://github.com/hsinn0) expanded CredHub pipeline access through [team member additions](https://github.com/cloudfoundry/community/pull/1427). The working group also completed [inactive member removal](https://github.com/cloudfoundry/community/pull/1383) following RFC-0025 guidelines.

Top non-bot contributors by commit count:
- [Aram Price](https://github.com/aramprice): 209 commits
- [Duane May](https://github.com/duanemay): 98 commits
- [Chris Selzo](https://github.com/selzoc): 58 commits
- [Nishad Mathur](https://github.com/alphasite): 43 commits
- [Ivaylo Ivanov](https://github.com/ivaylogi98): 40 commits
- [Ramon Makkelie](https://github.com/ramonskie): 39 commits
- [Ned Petrov](https://github.com/neddp): 38 commits
- [Brian Upton](https://github.com/ystros): 36 commits
- [Hongchol Sinn](https://github.com/hsinn0): 33 commits
- [Julian Hjortshoj](https://github.com/julian-hj): 31 commits

This growing contributor base ensures sustainable development velocity across the working group's extensive 110-repository ecosystem.
