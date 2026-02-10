---
title: "Foundational Infrastructure Working Group Update"
date: 2026-02-10
period: September 2, 2025 - February 10, 2026
---

# Foundational Infrastructure Working Group Update

## RFC Implementation: Administrative Access to CFF Infrastructure

The working group completed [RFC: Administrative Access to CFF Infrastructure](https://github.com/cloudfoundry/community/pull/1415), granting TOC members administrative rights to CFF-managed resources beyond GitHub. This enables more effective governance and operational oversight across foundation infrastructure.

Additionally, [RFC-0045: Update Stack States from LOCKED to RESTRICTED](https://github.com/cloudfoundry/community/pull/1405) was merged, with [Florian Braun](https://github.com/FloThinksPi) leading the specification that clarifies stack lifecycle management. The [CF on KinD RFC](https://github.com/cloudfoundry/community/pull/1389) by [Johannes Haass](https://github.com/c0d1ngm0nk3y) provides a streamlined local development experience.

## Ubuntu Noble Stemcell Migration

The working group achieved a major milestone with the [Noble cut over](https://github.com/cloudfoundry/bosh/pull/2655) in BOSH Director, transitioning infrastructure to Ubuntu 24.04 LTS. [Aram Price](https://github.com/aramprice) coordinated 209 commits across the VM deployment lifecycle, ensuring seamless Noble adoption.

Cross-CPI Noble migration progressed through [AWS CPI Noble transition](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/198), [Azure CPI Noble switch](https://github.com/cloudfoundry/bosh-azure-cpi-release/pull/730), and [Noble stemcell VsphereGuestInfo support](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/pull/467). The latest stemcell releases include Ubuntu Noble v1.215 and Ubuntu Jammy v1.1044.

## BOSH Infrastructure Modernization

BOSH continues to lead Cloud Foundry's infrastructure modernization with 1,851 commits and 458 pull requests across VM deployment lifecycle repositories. [Chris Selzo](https://github.com/selzoc) contributed 58 commits while [Nishad Mathur](https://github.com/alphasite) and reviewers [Ivaylo Ivanov](https://github.com/ivaylogi98) and [Ned Petrov](https://github.com/neddp) strengthened code review capacity.

The BOSH Agent received critical improvements including [NVMe instance storage discovery fixes](https://github.com/cloudfoundry/bosh-agent/pull/400) and [configurable VMware tool paths](https://github.com/cloudfoundry/bosh-agent/pull/398). [IPv6 dual-stack documentation](https://github.com/cloudfoundry/docs-bosh/pull/891) advances RFC-0038 implementation with comprehensive networking guidance.

## Identity and Authentication Strategic Advances

The UAA ecosystem delivered substantial updates with 276 commits and 10 releases including [UAA v78.7.0](https://github.com/cloudfoundry/uaa/releases/tag/v78.7.0). [Duane May](https://github.com/duanemay) led modernization efforts with 98 commits spanning dependency updates and security enhancements across UAA repositories.

Major upgrades include the [Flyway database migration upgrade](https://github.com/cloudfoundry/uaa/pull/3698) and [Flyway refactoring](https://github.com/cloudfoundry/uaa/pull/3712) that position UAA for long-term maintainability. The [OpenID scope logging improvements](https://github.com/cloudfoundry/uaa/pull/3727) enhance debugging capabilities for operators.

## Community Growth and Role Management

The working group welcomed [Maria Shaldybin](https://github.com/mariash) as a [new BOSH approver](https://github.com/cloudfoundry/community/pull/1413) and [Maya Rosecrance](https://github.com/mrosecrance) received [FI approver status](https://github.com/cloudfoundry/community/pull/1391), strengthening technical leadership. [Hongchol Sinn](https://github.com/hsinn0) expanded CredHub pipeline access through [team member additions](https://github.com/cloudfoundry/community/pull/1427).

[Julian Hjortshoj](https://github.com/julian-hj) contributed 31 commits and updated [branch protection configurations](https://github.com/cloudfoundry/community/pull/1418). This growing contributor base ensures sustainable development velocity across BOSH's extensive 110-repository ecosystem.

## Database and Monitoring Infrastructure

MySQL and PostgreSQL database releases demonstrate continuous improvement with 143 commits and the [v10.34.0 monitoring release](https://github.com/cloudfoundry/mysql-monitoring-release/releases/tag/v10.34.0). The Prometheus BOSH ecosystem delivered 130 commits and 7 releases, enhancing infrastructure observability.

The CredHub ecosystem maintains robust credential management with 150 commits, including the critical [migration from unmaintained gopkg.in/yaml.v3](https://github.com/cloudfoundry/credhub-cli/pull/132) to the maintained fork. System logging infrastructure received 186 commits across rsyslog and event-log components.
