# Meta 
[meta]: #meta 
- Name: Deprecate and Remove Windows Support in Binary Buildpack 
- Start Date: 2025-01-15 
- Author(s): @tnikolova82, @ivanovac, @beyhan 
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs: [RFC-0050 Java Buildpack Migration to Golang](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0050-java-buildpack-migration-to-golang.md) 
 
## Summary 
 
Deprecate and immediately remove Windows support from the Cloud Foundry Binary Buildpack. [`v1.1.21`](https://github.com/cloudfoundry/binary-buildpack-release/releases/tag/v1.1.21) will be the last release shipping Windows support. The next release will be Linux-only. 
 
## Problem 
 
- The Windows support in the Binary Buildpack is effectively unmaintained following the departure of its core maintainer from the CF community. 
- It is one of the only buildpacks (alongside [`hwc-buildpack`](https://github.com/cloudfoundry/hwc-buildpack)) supporting Windows, and the current maintainers have no Windows experience to support this use case. 
- No one has stepped up to maintain the Windows portion despite calls for help. 
- Shipping a Windows binary that maintainers cannot audit, patch, or verify is a risk that should not be prolonged. 
 
## What is being deprecated 
 
The Binary Buildpack's Windows support enables deploying pre-compiled Windows executables (e.g. `.exe`, `.bat` entrypoints) to Cloud Foundry Windows Diego cells. Concretely, the following pieces are being removed: 
 
- The `binary-buildpack-windows` package: the BOSH release currently ships two packages — a Linux-compiled buildpack binary and a separate Windows-compiled buildpack binary. When CF schedules an app onto a Windows cell, the Windows variant is used as the buildpack runtime to detect, supply, and launch the app's binary. Only the Linux package will remain. 
- The `windows` stack entry in `binary-buildpack-release`'s `manifest.yml` and the corresponding job/packaging specs that wire the Windows package into the BOSH release. 
- Windows-specific buildpack code in [`binary-buildpack`](https://github.com/cloudfoundry/binary-buildpack), including: 
  - Files guarded by `//go:build windows` build tags (e.g. Windows-specific `finalize`/`supply` and launcher logic). 
  - Handling for Windows-style start commands and executable extensions (`.exe`, `.bat`). 
  - Windows-targeted packaging scripts and any `GOOS=windows` cross-compilation in build tooling. 
- Windows CI: GitHub Actions / Concourse jobs that cross-compile, unit test, and integration-test the buildpack against Windows cells (including any `cflinuxfs*` ↔ `windows*` matrix entries). 
- Windows integration test fixtures: sample apps containing Windows binaries used to validate end-to-end staging and running on Windows cells. 
 
After removal, the buildpack will only detect and stage apps targeting Linux stacks (e.g. `cflinuxfs4`). Operators with Windows workloads that ship plain executables will need to pin to `v1.1.21` or fork.
 
## Proposal 
 
- Designate [`v1.1.21`](https://github.com/cloudfoundry/binary-buildpack-release/releases/tag/v1.1.21) as the final release with Windows support. It will receive no further updates, including security patches, for the Windows stack. 
- Immediately (no transition period) remove all Windows-specific code, CI, and packaging from [`binary-buildpack`](https://github.com/cloudfoundry/binary-buildpack) and `binary-buildpack-release`, and cut a Linux-only `v2.0.0`. 
- Add deprecation notices to repos' `README.md`, CF documentation, and announce on `#buildpacks` Slack. 
- Affected users may pin to `v1.1.21` or self-maintain a fork.
## Rationale and Alternatives 
 
- Why immediate removal (no 6-month transition)? 
  - The Windows code path is already de-facto unmaintained and a transition period changes nothing operationally, since no fixes are being produced anyway. 
  - Continuing to publish Windows artifacts during a grace period creates a false impression of support and prolongs security risk. 
  - `v1.1.21` remains available for any operator who needs to keep using Windows, where pinning is a one-line change. 
- Sustainability & security: maintainers cannot credibly support a platform they have no expertise on. Additionally, an explicitly removed path is safer than a quietly unmaintained one. 
- Alternatives considered: 
  - Find new maintainers — attempted, none came forward. 
  - Do nothing — leaves users without patches or clarity. 
 
## Implementation 
 
1. Announce deprecation and removal. 
2. Strip all Windows-specific code.
4. Cut a Linux-only `v2.0.0` of `binary-buildpack-release`. 
5. Update CF documentation to reference `v1.1.21` as the last Windows-supporting release. 
 