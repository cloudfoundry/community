---
title: "Foundational Infrastructure Working Group Update"
date: 2026-06-22
period: September 2, 2025 - June 22, 2026
---

# Foundational Infrastructure Working Group Update

## RFC-0053: BOSH Dynamic Disks via Volume Services

The working group advanced [RFC-0053](https://github.com/cloudfoundry/community/issues/1460) for dynamic disks, enabling IaaS-managed persistent volumes for Diego containers. [Nishad Mathur](https://github.com/Alphasite) added create, attach, and list endpoints to the [BOSH Director API](https://github.com/cloudfoundry/bosh/pull/2743) and [CLI](https://github.com/cloudfoundry/bosh-cli/pull/728). [Mariash](https://github.com/mariash) contributed agent-side [dynamic disk support](https://github.com/cloudfoundry/bosh-agent/pull/393).

[Ned Petrov](https://github.com/neddp) delivered the update_disk CPI action across [AWS](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/196), [GCP](https://github.com/cloudfoundry/bosh-google-cpi-release/pull/382), and [Azure](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/741). [Ivaylo Ivanov](https://github.com/Ivaylogi98) added NVMe instance storage discovery for [AWS](https://github.com/cloudfoundry/bosh-agent/pull/396) and [AliCloud](https://github.com/cloudfoundry/bosh-alicloud-cpi-release/pull/207).

## RFC-0043: Cloud Controller Storage CLI Integration

Cross-working-group collaboration advanced [RFC-0043](https://github.com/cloudfoundry/community/issues/1274), unifying blobstore backends through BOSH storage CLIs. [Stephan Merkel](https://github.com/stephanme) drove the specification that bridges Foundational Infrastructure and App Runtime Interfaces.

[Gowri Shankar](https://github.com/gowrisankar22) added [storage-cli support](https://github.com/cloudfoundry/bosh/pull/2665) to the BOSH Director's blobstore configuration. [Nishad Mathur](https://github.com/Alphasite) added [S3 checksum properties](https://github.com/cloudfoundry/bosh/pull/2726) and improved blobstore ID handling.

## UAA v79: Spring Boot 4 and Java 25 Modernization

[Georgi Genchev](https://github.com/gdgenchev) led the [Spring Boot 4 migration](https://github.com/cloudfoundry/uaa/pull/3805) for UAA v79.0.0, upgrading from Boot 3 with Jakarta EE 11. [Duane May](https://github.com/duanemay) drove the companion Gradle Kotlin DSL migration, [Java 25 upgrade](https://github.com/cloudfoundry/uaa/pull/3705), and dependency consolidation across 15 releases.

[Filip Hanik](https://github.com/fhanik) strengthened security with [token extension protection](https://github.com/cloudfoundry/uaa/pull/3954) and SAML metadata fixes. [Markus Strehle](https://github.com/strehle) completed the [OpenSAML 5 upgrade](https://github.com/cloudfoundry/uaa/pull/3840) and Flyway legacy migration, shipping v79.1.0 with the [UAA release](https://github.com/cloudfoundry/uaa-release/releases/tag/v79.1.0).

## Disaster Recovery Consolidation into BOSH

[Craig I.](https://github.com/aramprice) championed [PR #1525](https://github.com/cloudfoundry/community/pull/1525) to collapse the Disaster Recovery area into VM deployment lifecycle. This unifies backup and restore governance under BOSH's operational domain.

[Chris Selzo](https://github.com/selzoc) extended the SDK with [PostgreSQL 17](https://github.com/cloudfoundry/backup-and-restore-sdk-release/pull/1894) and MySQL 8.4 blob support. [Brian Upton](https://github.com/ystros) maintained release pipelines as repositories migrated from cloudfoundry-incubator.

## IPv6 Dual-Stack Across Cloud CPIs

[Sascha Heid](https://github.com/s4heid) drove Azure IPv6 dual-stack, bumping the [Azure REST API to 2024-05-01](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/744) with [integration tests](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/747). [Ansh Rupani](https://github.com/anshrupani) delivered AWS multi-stack network and prefix delegation.

[Felix Moehler](https://github.com/fmoehler) added prefix handling to BOSH Director network settings and [RFC-0038 documentation](https://github.com/cloudfoundry/docs-bosh/pull/877). [Ned Petrov](https://github.com/neddp) documented dual-stack networking across all CPIs with acceptance tests.

## Database and Monitoring Infrastructure

[Pascal Zimmermann](https://github.com/ZPascal) delivered [PostgreSQL 18 support](https://github.com/cloudfoundry/postgres-release/pull/90) with configurable password algorithms. [Andrew Garner](https://github.com/abg) hardened PXC with SQL injection fixes and [stricter TLS validation](https://github.com/cloudfoundry/mysql-monitoring-release/pull/21).

[Benjamin Guttmann](https://github.com/benjaminguttmann-avtq) advanced Prometheus with automated Go workflows and [v31.2.0](https://github.com/cloudfoundry/prometheus-boshrelease/releases/tag/v31.2.0). [Colin Shield](https://github.com/colins) expanded to approver across BBR, stemcell, and VM deployment areas.
