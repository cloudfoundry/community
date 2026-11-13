# Meta
[meta]: #meta
- Name: Collaboration and Ownership of Kubernetes Release Assets
- Start Date: 2026-09-14
- Author(s): @beyhan, @c0d1ngm0nk3y, @loewenstein-sap, @modulo11, @mvach, @nicolasbender, @pbusko
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1630
- Related RFCs: [RFC-0049 CF on KinD](rfc-0049-cf-on-kind.md)
- Affected Component(s): App Runtime Interfaces, App Runtime Platform, Foundational Infrastructure, App Runtime Deployments (see the appendix for the per-component list)

## Summary

Cloud Foundry can be deployed with BOSH (`cf-deployment`) and, following [RFC-0049](rfc-0049-cf-on-kind.md), on Kubernetes (`kind-deployment`). This RFC establishes Kubernetes as a second community-supported deployment option alongside BOSH, and defines how working groups support it.

A renaming from `kind-deployment` to `k8s-deployment` might make this clearer.

Running Cloud Foundry on Kubernetes requires a Helm chart and one or more container images per component. Today these Kubernetes assets are maintained in the central `cloudfoundry/cf-k8s-releases` repository.

We propose a three step approach to gradually share responsibility for these assets with the working groups:

1. Working groups should communicate breaking or otherwise important changes to their BOSH components (e.g. via GitHub issues in cf-k8s-releases).
1. Working groups are encouraged to contribute Kubernetes asset updates directly to that repository.
1. Groups that want to maintain their own pipelines and fully control their Kubernetes assets may take ownership and even move them to a repository of their choice.

## Problem

Cloud Foundry components are developed with BOSH as the only deployment target in mind. With Kubernetes as a second supported option, component changes need to be considered for both.

A component's Kubernetes packaging is built from its source, but the team maintaining that packaging is often different from the team developing the component. Without timely communication, component changes can leave Kubernetes assets outdated or broken.

A clear notification process and opportunities for direct contribution would improve coordination. Working groups that want to maintain their Kubernetes assets independently also need a clear ownership-transfer path.

## Proposal

### Change notifications

All working groups should notify the maintainers of `cf-k8s-releases` (e.g. via GitHub issues in that repository) about breaking or otherwise important changes to their BOSH components. Notifications should describe the change and identify the affected release so maintainers can assess the impact on Kubernetes assets.

Relevant changes may include changes to configuration, dependencies, build requirements, or runtime behavior.

This notification is how working groups take Kubernetes into account as a supported deployment option. It does not block BOSH releases.

### Contributions to the central repository

Working groups are encouraged to contribute corresponding Helm chart, Dockerfile, and release workflow updates directly to `cf-k8s-releases`.

The repository remains the home for assets whose ownership has not been transferred. Its maintainers continue to maintain and publish those assets, supported by notifications and contributions from the component-owning working groups.

### Ownership transfer

Working groups that want full control over their Kubernetes assets and release pipelines may take ownership of those assets. Taking ownership means accepting full responsibility for maintaining, building, and publishing the assets and keeping them aligned with the component.

Ownership transfers happen independently for each component, at the working group's chosen pace. Regardless of which option a working group chooses, an ownership transfer must preserve existing chart and image names and registry locations. Charts should continue to be published to `oci://ghcr.io/cloudfoundry/helm` and images to `ghcr.io/cloudfoundry/k8s`.

A working group may take ownership in one of two ways.

#### Option A: Ownership within the shared repository

The assets stay in `cf-k8s-releases`, and the working group takes ownership of their component's directory through a `CODEOWNERS` entry.

This option keeps the asset layout and publishing pipeline unchanged. It gives the working group control over the content of its component's assets without operating a separate repository or pipeline.

#### Option B: Moving assets to a separate repository

The working group moves the assets out of `cf-k8s-releases` into a repository of their choice within the cloudfoundry org. This may be the corresponding BOSH release repository or another repository selected by the working group. The working group then operates its own release pipeline for those assets.

The working group and `cf-k8s-releases` maintainers coordinate the handoff so that publishing continues from the destination repository and stops in `cf-k8s-releases`. At no point are the same assets published from two repositories.

### Validation

End-to-end validation of the assembled deployment remains with the App Runtime Deployments working group, as established in [RFC-0049](rfc-0049-cf-on-kind.md).

## Alternatives

**Require every working group to take ownership.** Moving all Kubernetes assets into their corresponding BOSH release repositories would bring packaging closer to component development. However, it would require every working group to assume additional maintenance and pipeline responsibilities. The proposed approach allows groups to take ownership when they are ready while improving coordination for centrally maintained assets.

## Appendix: Component Reference

| Component (current `cf-k8s-releases` directory) | Corresponding BOSH release repository | Owning working group / area |
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

The root `buildpacks.Dockerfile` and `stacks.Dockerfile` in `cf-k8s-releases` are shared build definitions used across buildpacks and stacks respectively. If ownership of related assets is transferred, the Buildpacks and Stacks area and `cf-k8s-releases` maintainers coordinate how these shared definitions will be maintained.
