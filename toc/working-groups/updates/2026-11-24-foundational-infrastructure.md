---
title: "Foundational Infrastructure Working Group Update"
date: 2026-11-24
period: June 23 - November 24, 2026
---

# Foundational Infrastructure Working Group Update

The biggest change since the [June 22 draft](https://github.com/cloudfoundry/community/blob/e1010e6c03e20b32269bb52cd30320ed27b9fd96/toc/working-groups/updates/2026-06-22-foundational-infrastructure.md) is that BOSH can now target air-gapped Google Distributed Cloud with upstream artifacts. ARM64 build support is also landing, and operators have new BOSH, networking, database, and identity releases to test.

## BOSH and cloud infrastructure

- **Air-gapped Google Distributed Cloud:** [RFC-0063](../../rfc/rfc-0063-gdc-cpi-and-stemcell-builder.md) was accepted, and Google and SAP established a [new FI area](https://github.com/cloudfoundry/community/pull/1648) to maintain the CPI. The upstream [GDC CPI v0.1.4](https://bosh.io/releases/github.com/cloudfoundry/bosh-gdc-cpi-release?version=0.1.4) is published on bosh.io, and the stemcell builder shipped [GDC support for Ubuntu Noble](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/releases/tag/ubuntu-noble/v1.664). Two [backup maintainers](https://github.com/cloudfoundry/community/pull/1716) joined the area. The [implementation tracker](https://github.com/cloudfoundry/community/issues/1654) remains open.
- **ARM64 and Ubuntu 26.04:** With [RFC-0062](../../rfc/rfc-0062-arm64-support.md) accepted, [ARM64 stemcell builds](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/pull/768) and [BOSH Agent builds](https://github.com/cloudfoundry/bosh-agent/pull/493) merged. [Director packaging and CI](https://github.com/cloudfoundry/bosh/pull/2845) are still under review; this is not yet end-to-end ARM64 support. Separately, [BOSH Director v283.0.0](https://github.com/cloudfoundry/bosh/releases/tag/v283.0.0) added Ubuntu Resolute compatibility and removed CPI v1 support. Operators upgrading from v282 should verify that their CPI supports v2.
- **Dynamic disks and dual-stack networking:** BOSH Director [v283.1.2](https://github.com/cloudfoundry/bosh/releases/tag/v283.1.2) shipped the create, attach, and list endpoints for dynamic disks. The [CLI commands](https://github.com/cloudfoundry/bosh-cli/pull/728) and [operator documentation](https://github.com/cloudfoundry/docs-bosh/pull/927) merged; [RFC-0053 delivery tracking](https://github.com/cloudfoundry/community/issues/1460) is still open. [Azure CPI v53.1.9](https://github.com/cloudfoundry/bosh-azure-cpi-release/releases/tag/v53.1.9) shipped VM dual-stack support, and [AWS CPI v107.3.5](https://github.com/cloudfoundry/bosh-aws-cpi-release/releases/tag/v107.3.5) added primary IPv6 addresses on network interfaces.

## Identity, storage, and recovery

- **Identity:** UAA shipped [mTLS token endpoint hardening in v79.10.0](https://github.com/cloudfoundry/uaa/releases/tag/v79.10.0) and [subject matching for federated clients in v79.11.0](https://github.com/cloudfoundry/uaa/releases/tag/v79.11.0); [UAA Release v79.12.0](https://github.com/cloudfoundry/uaa-release/releases/tag/v79.12.0) also updated Java and Tomcat. The cross-group [workload service accounts RFC](../../rfc/rfc-0065-service-accounts.md) was accepted; the [Cloud Controller implementation](https://github.com/cloudfoundry/cloud_controller_ng/pull/5520) and [RFC amendments](https://github.com/cloudfoundry/community/pull/1709) are still open. CredHub merged [duration validation for certificate regeneration](https://github.com/cloudfoundry/credhub/pull/1234).
- **Storage and recovery:** The [Cloud Controller storage CLI tracker](https://github.com/cloudfoundry/community/issues/1274) closed after all five backends were documented as delivered in `cf-deployment`. The separate [BOSH Director storage CLI integration](https://github.com/cloudfoundry/bosh/pull/2665) is still a draft. [Postgres Release v57.0.0](https://github.com/cloudfoundry/postgres-release/releases/tag/v57.0.0) added compatibility for PostgreSQL 16–18 on Ubuntu Resolute, and [Backup and Restore SDK v1.20.4](https://github.com/cloudfoundry/backup-and-restore-sdk-release/releases/tag/v1.20.4) added PostgreSQL 18 support.

## Topics for operator feedback

- Review the proposals for [BPM-managed jobs without Monit](https://github.com/cloudfoundry/community/pull/1706), [a structured Health Monitor event log](https://github.com/cloudfoundry/community/pull/1671), and [deprecating the Warden and VirtualBox CPIs](https://github.com/cloudfoundry/community/pull/1702). Feedback on existing Monit, Health Monitor plugin, or CPI dependencies would help scope the migration work.
- Follow [RFC-0064](https://github.com/cloudfoundry/community/issues/1697) for opt-in OpenTelemetry collection of platform logs. Under the accepted design, syslog remains the default and operators can run both during migration.

*Scope: Public GitHub activity across 118 charter-listed repositories, plus community RFCs and linked cross-group work. Four private charter repositories were excluded. Snapshot: November 24, 2026 at 08:05 UTC.*
