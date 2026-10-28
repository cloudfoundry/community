# Meta
[meta]: #meta
- Name: Component Ownership of Kubernetes Release Assets
- Start Date: 2026-09-14
- Author(s): @beyhan, @c0d1ngm0nk3y, @loewenstein-sap, @modulo11, @mvach, @nicolasbender, @pbusko
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs: [RFC-0049 CF on KinD](rfc-0049-cf-on-kind.md)
- Affected Component(s): App Runtime Interfaces, App Runtime Platform, Foundational Infrastructure, App Runtime Deployments (see the appendix for the per-component list)

## Summary

Running Cloud Foundry on Kubernetes requires a Helm chart and one or more container images per component. Today these Kubernetes assets are maintained in the central `cloudfoundry/cf-k8s-releases` repository, owned by a single team. We propose that the team owning each BOSH release also own its Kubernetes assets, moving the Helm chart and Dockerfile into the BOSH release repository and releasing them alongside the BOSH release. Once every BOSH release has taken over its assets, `cloudfoundry/cf-k8s-releases` will be empty and eligible for archival.

## Problem

The Helm charts and Dockerfiles needed to run Cloud Foundry on Kubernetes are currently contained in `cloudfoundry/cf-k8s-releases`, a single repository owned by one team. A component's Kubernetes packaging is built from its source, yet it is maintained by a team that does not develop that component. The people who change the source and the people who maintain its packaging are not the same.

## Proposal

Each component's Kubernetes assets — its Helm chart and its Dockerfile(s) — move into the corresponding BOSH release repository, the one consumed by `cf-deployment`. The team owning that BOSH release owns these assets and releases them as part of its regular release process.

The released artifacts and their consumers are unaffected. Charts continue to be published to `oci://ghcr.io/cloudfoundry/helm` and images to `ghcr.io/cloudfoundry/k8s`, exactly as `cf-k8s-releases` publishes them today.

Releasing a chart and image together with the BOSH release keeps the Kubernetes assets aligned with the release version.

### Migration

The assets for each component are independent, so each team can move its chart, Dockerfile and GitHub Action workflow at its own pace. The migration therefore proceeds one BOSH release at a time, with no single large cutover.

For each component, the handoff preserves continuity: the BOSH release repository begins publishing the same chart and image, under the same names, to the same registries, and `cf-k8s-releases` stops publishing them. At no point are the same assets published from two repositories.

`cf-k8s-releases` empties out as assets migrate. When the last assets have moved, the repository is empty and eligible for archival following the process in [RFC-0007](rfc-0007-repository-ownership.md).

### Validation

End-to-end validation of the assembled deployment remains with the App Runtime Deployments working group, as established in [RFC-0049](rfc-0049-cf-on-kind.md). This RFC does not change where integration testing happens.

## Alternatives

**Separate Kubernetes repositories per component team.** Each team could own a dedicated repository holding only its Kubernetes assets, apart from its BOSH release. This keeps ownership with the right team, but a repository separate from the source it packages lets the assets drift from the BOSH release they track — the divergence the current arrangement already suffers from, now spread across many repositories.

**A central repository under shared ownership.** The assets could stay in a single repository like `cf-k8s-releases`, but with ownership shared across all teams rather than held by one. Shared ownership of a central repository tends to become no ownership: when everyone is responsible, no one is. This carries the divergence risk of a repository separate from the source and adds diffusion of responsibility on top.

## Appendix: Suggested Mapping


| Component (current `cf-k8s-releases` directory) | Target BOSH release repository | Owning working group / area |
|---|---|---|
| capi | `cloudfoundry/capi-release` | App Runtime Interfaces / CAPI |
| diego | `cloudfoundry/diego-release` | App Runtime Platform / Diego |
| uaa | `cloudfoundry/uaa-release` | Foundational Infrastructure / Identity and Auth (UAA) |
| credhub | `pivotal-cf/credhub-release` | Foundational Infrastructure / Credential Management (Credhub) |
| routing | `cloudfoundry/routing-release` | App Runtime Platform / Networking |
| cf-networking | `cloudfoundry/cf-networking-release` | App Runtime Platform / Networking |
| loggregator | `cloudfoundry/loggregator-release` | App Runtime Platform / Logging and Metrics |
| loggregator-agent | `cloudfoundry/loggregator-agent-release` | App Runtime Platform / Logging and Metrics |
| log-cache | `cloudfoundry/log-cache-release` | App Runtime Platform / Logging and Metrics |
| nfs-volume | `cloudfoundry/nfs-volume-release` | App Runtime Platform / Volume Services |
| cflinuxfs4 | `cloudfoundry/cflinuxfs4-release` | App Runtime Interfaces / Buildpacks and Stacks |
| cflinuxfs5 | `cloudfoundry/cflinuxfs5-release` | App Runtime Interfaces / Buildpacks and Stacks |
| binary-buildpack | `cloudfoundry/binary-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| dotnet-core-buildpack | `cloudfoundry/dotnet-core-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| go-buildpack | `cloudfoundry/go-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| java-buildpack | `cloudfoundry/java-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| nginx-buildpack | `cloudfoundry/nginx-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| nodejs-buildpack | `cloudfoundry/nodejs-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| php-buildpack | `cloudfoundry/php-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| python-buildpack | `cloudfoundry/python-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| r-buildpack | `cloudfoundry/r-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| ruby-buildpack | `cloudfoundry/ruby-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| staticfile-buildpack | `cloudfoundry/staticfile-buildpack-release` | App Runtime Interfaces / Buildpacks and Stacks |
| bosh-dns | `cloudfoundry/bosh-dns-release` | Foundational Infrastructure |

### Shared build files

The root `buildpacks.Dockerfile` and `stacks.Dockerfile` in `cf-k8s-releases` are shared build definitions used across all buildpacks and stacks respectively, rather than assets of a single BOSH release. Whether they are split per target repository or handled another way is a detail for the Buildpacks and Stacks area to settle during migration.