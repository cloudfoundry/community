# Meta
[meta]: #meta
- Name: Support Resolute Raccoon (26.04) as the CF Linux Operating System
- Start Date: 2026-05-08
- Author(s): @mkocher
- Status: Draft
- RFC Pull Request: [#1498](https://github.com/cloudfoundry/community/pull/1498)
- Related RFCs: [rfc-0001-jammy-os](rfc-0001-jammy-os.md), [rfc-0026-noble-os](rfc-0026-noble-os.md)
- Affected Component(s): bosh-linux-stemcell-builder, cf-deployment, assorted releases

## Summary

The CF community should add support for Ubuntu Resolute Raccoon (26.04 LTS) as the next CF Linux operating system. This RFC proposes producing a Resolute-based BOSH stemcell, validating it across the CF component ecosystem, and providing a clear migration path for release authors and operators—particularly for the removal of the `runit` package, which is likely the most impactful change the stemcell itself introduces.

## Problem

Ubuntu 26.04 LTS ("Resolute Raccoon") is the next long-term support release. Starting the Resolute stemcell effort now gives the community sufficient runway to:

- Deliver post-quantum cryptography capabilities (ML-KEM, ML-DSA, SLH-DSA via OpenSSL and OpenSSH) that are available in Resolute but not in Noble.
- Allow release authors to address breaking changes in an orderly fashion.

The CF community skipped Ubuntu Focal in favour of Jammy ([rfc-0001](rfc-0001-jammy-os.md)), which created significant time pressure and made it nearly impossible to introduce backward-incompatible cleanups. While Noble Numbat (24.04) stemcells exist ([rfc-0026](rfc-0026-noble-os.md)), adoption across the CF ecosystem has been slow, just recently becoming the default in cf-deployment. Adopting a Resolute stemcell now will allow platform engineers to migrate directly from Jammy to Resolute while staying under support.

## Proposal

The CF community should create a BOSH stemcell based on Ubuntu Resolute Raccoon (26.04 LTS) now.

---

### Changes in Ubuntu 26.04 That May Affect BOSH Releases

#### `coreutils`: GNU → Rust (`uutils`)

Ubuntu 26.04 ships [`rust-coreutils`](https://github.com/uutils/coreutils) (the uutils Rust port) as the default provider of core OS utilities (`ls`, `cat`, `echo`, `base64`, etc.). GNU coreutils remains available as `gnu-coreutils` for releases that need it. Scripts relying on GNU-specific flags or output formats may behave differently and are the most likely source of subtle BOSH job breakage. One known example is a bug in the `install` utility: [uutils/coreutils#11469](https://github.com/uutils/coreutils/issues/11469). Release authors should consider gnu-coreutils deprecated and expect it to be removed in the next stemcell line.

#### `sudo`: C implementation → `sudo-rs` (Rust)

[`sudo-rs`](https://github.com/memorysafety/sudo-rs), a Rust rewrite of sudo, is the default `sudo` provider in Resolute. The classic C implementation remains available as `sudo.ws`. `sudo-rs` does not yet support all flags of the classic implementation. BOSH releases that parse `sudo` version strings or rely on options not implemented in `sudo-rs` may need updates.

#### GCC 13 → 15

The default GCC version is 15. GCC 15 promotes several previously advisory warnings to hard errors. Known affected releases include [capi-release](https://github.com/cloudfoundry/capi-release/pull/637) and [garden-runc-release](https://github.com/cloudfoundry/garden-runc-release/pull/391).

#### systemd 255 → 259

This version bump drops significant legacy compatibility. Key impacts for CF:

- cgroup v1 support is removed.
- Ubuntu 26.04 is the **last** LTS to retain System V init-script compatibility in systemd.
- `/tmp` is now a `tmpfs` by default (via the `tmp.mount` unit).
- Warden stemcells do not currently work on Apple Silicon under Rosetta 2 due to this systemd bump ([bosh-linux-stemcell-builder#577](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/issues/577)).

#### OpenSSH 9.6p1 → 10.2p1

- DSA host keys are no longer generated and DSA client keys will not be accepted.
- Post-quantum key exchange (`mlkem768x25519-sha256`) is enabled by default; connections using non-post-quantum algorithms will log a warning.

#### APT 2.7 → 3.1

`apt-key` is removed. GPG keys must be placed directly in `/usr/share/keyrings/` as binary keyring files. Any BOSH release that calls `apt-key add` will fail and must be updated.

#### Python 3.12 → 3.14

System Python is now 3.14. This is a fairly large jump for Python and removes some previously included modules, however Python is not particularly heavily used in bosh releases.

#### Libraries Removed from the Base Image

The following libraries present in the Noble base image will no longer be installed in Resolute. BOSH releases that link against these at compile time or expect them at runtime will need to either bundle the library, install it explicitly, or update to the replacement:

| Package | Notes |
|---|---|
| `libargon2-1` | Removed with no replacement in the base image |
| `libicu-dev`, `icu-devtools` | ICU (Unicode/UTF-8) development headers and tools removed; the runtime library (`libicu78`) is still present |
| `libssh-4` | Replaced by `libssh2-1t64` — note these are different upstream projects ([libssh](https://www.libssh.org/) vs [libssh2](https://www.libssh2.org/)) and are not API-compatible |

---

### Stemcell Change: Removal of `runit`

**This is the most significant breaking change the stemcell itself introduces—independent of Ubuntu 26.04.**

The `runit` package is removed from the Resolute stemcell. The stemcell no longer uses runit, but the package has historically provided the `chpst` utility, which many BOSH releases use to drop process privileges at startup (e.g., `exec chpst -u vcap:vcap ...`). Any BOSH release that calls `chpst` on its live execution path will fail to start on a Resolute stemcell.

AI was used to perform a search across the `cloudfoundry` GitHub organization aand it identified the following usages and provided these suggested fixes:

| Release | Script | Notes |
|---|---|---|
| [cloudfoundry/bosh](https://github.com/cloudfoundry/bosh) | `director/worker_ctl.erb` | Director background workers; recomend migrating to BPM. |
| [cloudfoundry/bosh-dns-release](https://github.com/cloudfoundry/bosh-dns-release) | `bosh-dns/bosh_dns_ctl.erb` | DNS daemon; deployed to **every BOSH VM** — highest blast radius. Recommend BPM with `setcap` moved to pre-start. |
| [cloudfoundry/bosh-dns-release](https://github.com/cloudfoundry/bosh-dns-release) | `bosh-dns/bosh_dns_health_ctl.erb` | DNS health server; trivial BPM addition alongside the above. |
| [cloudfoundry/syslog-release](https://github.com/cloudfoundry/syslog-release) | `syslog_forwarder/blackbox_ctl.erb` | Runs as `syslog:vcap`, not `vcap:vcap`. Use `runuser -u syslog` to preserve the user identity; BPM requires care here. |
| [cloudfoundry/config-server-release](https://github.com/cloudfoundry/config-server-release) | `config_server/ctl.erb` | Straightforward BPM migration; Go binary with no special requirements. |
| [cloudfoundry/bosh-system-metrics-server-release](https://github.com/cloudfoundry/bosh-system-metrics-server-release) | `system-metrics-server/ctl.erb` | Straightforward BPM migration; Go binary with no special requirements. |
| [cloudfoundry/system-metrics-release](https://github.com/cloudfoundry/system-metrics-release) | `loggr-system-metrics-agent/ctl.erb` | **BPM likely not viable** (code includes comment stating that BPM breaks disk usage metrics). Use `su`/`runuser`. |
| [cloudfoundry/nfs-volume-release](https://github.com/cloudfoundry/nfs-volume-release) | `nfsv3driver/nfsv3driver_ctl.erb` | `chpst` is called with no flags — it is a pure pass-through. Remove it entirely. |
| [cloudfoundry/smb-volume-release](https://github.com/cloudfoundry/smb-volume-release) | `smbdriver/smbdriver_ctl.erb` | `chpst -u root:root` — redundant since the script already runs as root. Remove it. |
| [cloudfoundry/capi-release](https://github.com/cloudfoundry/capi-release) | Pre-start and post-start scripts for `cloud_controller_ng`, `cloud_controller_clock`, `cloud_controller_worker`, `cc_deployment_updater` | Multiple usages for directory creation, DB migrations, seeding, and validation. Use `su -s /bin/bash vcap -c` for script invocations; `mkdir`+`chown` for directory operations. |
| [cloudfoundry/capi-release](https://github.com/cloudfoundry/capi-release) | `nfs_mounter/handle_nfs_blobstore.sh.erb` | Creates a directory and test file on an NFS share as `vcap`. Replace with `mkdir`+`chown vcap:vcap`. |

#### Migration Paths for `chpst`

Release authors have several drop-in replacements:

1. **Migrate to [BPM](https://github.com/cloudfoundry/bpm-release)** *(recommended long-term)*: BPM runs processes as `vcap` by default and handles privilege separation natively. Move any operation that requires root (e.g., `setcap`, filesystem setup) to a `pre-start` script and run the main process via BPM. This is the preferred architectural approach.

2. **Use `su -s /bin/bash vcap -c "..."`** *(recommended short-term)*: This is a one-line replacement available on every BOSH VM that unblocks Resolute immediately. `runuser -u vcap -- ...` is an equivalent alternative.

3. **Use `sudo -u vcap`**: Available since `sudo` (now `sudo-rs`) is installed on every BOSH VM.

4. **Use `setpriv` or `gosu`**: Standard privilege-dropping utilities available in Ubuntu without runit.

For jobs that use a non-`vcap` run user (e.g., `syslog-release` runs as `syslog:vcap`), the `su`/`runuser` approach is the safest short-term migration because BPM's `run.user` support needs additional validation in that context.

---

### What the Resolute Stemcell Is NOT Changing

- **`monit` remains supported**: All BOSH jobs currently managed by monit will continue to work on the Resolute stemcell. Introducing a `monit` alternative is a worthy goal and something the RFC author plans to write an RFC for. However it does not need to be coupled with the release of the Resolute stemcell as it will be an additive change. At that point `monit` deprecation should be announced and it should be removed in the next stemcell line.

- **No x86-64-v3 microarchitecture requirement**: Ubuntu 26.04 cloud images adopt the `x86-64-v3` CPU microarchitecture level by default, which drops support for older cloud instance families (certain AWS M3/M4, C3/C4, R3/R4 generations, and some GCP N1 CPU platforms, among others). The CF Resolute stemcell will **not** adopt this restriction. Operators may have hardware or reserved instances in the older instance families, and the compatibility tradeoff does not justify the change at this time.

---

## Workstreams

### Foundational Infrastructure WG

The Foundational Infrastructure Working Group owns `bosh-linux-stemcell-builder` and the resulting BOSH stemcells. Work includes:

- Extend `bosh-linux-stemcell-builder` for Ubuntu Resolute Raccoon 26.04
- Validate that the BOSH agent works correctly on the new OS
- Set up CI pipelines producing `0.x` alpha stemcell builds
- Publish `0.x` alpha stemcells to [bosh.io](https://bosh.io) for community-wide validation
- Validate that a BOSH Director deploys successfully and BOSH Acceptance Tests pass
- Publish release notes and a migration guide alongside the `1.x` GA release
- Publish the `1.x` GA stemcell on [bosh.io](https://bosh.io)

### App Runtime Deployments WG

Once the `0.x` alpha stemcell is validated against the BOSH Director:

- Set up cf-deployment validation against the Resolute alpha stemcell
- Distribute issues discovered during validation to the relevant component Working Groups for resolution
- Provide an ops-file enabling operators to opt in to the Resolute stemcell
- Decide on and communicate a timeline for making Resolute the default stemcell in cf-deployment

### All CF Release Authors

- Resolve any `chpst` usages (see migration paths above) before the `1.x` GA stemcell is published
- Validate compilation against GCC 15 and address any new errors
- Audit `apt-key`, cgroup v1, and `sudo`-flag usage in job scripts