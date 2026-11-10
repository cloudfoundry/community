# Meta
[meta]: #meta
- Name: Collaboration and Ownership of Kubernetes Release Assets
- Start Date: 2026-09-14
- Author(s): @beyhan, @c0d1ngm0nk3y, @loewenstein-sap, @modulo11, @mvach, @nicolasbender, @pbusko
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs: [RFC-0049 CF on KinD](rfc-0049-cf-on-kind.md)
- Affected Component(s): App Runtime Interfaces, App Runtime Platform, Foundational Infrastructure, App Runtime Deployments (see the appendix for the per-component list)

## Summary

Running Cloud Foundry on Kubernetes requires a Helm chart and one or more container images per component. Today these Kubernetes assets are maintained in the central `cloudfoundry/cf-k8s-releases` repository.

We propose requiring working groups to communicate breaking or otherwise important changes to their BOSH components through GitHub issues in `cf-k8s-releases`. Working groups are encouraged to contribute Kubernetes asset updates directly to that repository. Groups that want to maintain their own pipelines and fully control their Kubernetes assets may take ownership and move them to a repository of their choice.

## Problem

A component's Kubernetes packaging is built from its source, but the team maintaining that packaging is often different from the team developing the component. Without timely communication, component changes can leave Kubernetes assets outdated or broken.

A clear notification process and opportunities for direct contribution would improve coordination. Working groups that want to maintain their Kubernetes assets independently also need a clear ownership-transfer path.

## Proposal

### Change notifications

All working groups must notify the maintainers of `cf-k8s-releases` through GitHub issues in that repository about breaking or otherwise important changes to their BOSH components. Notifications should describe the change and identify the affected release so maintainers can assess the impact on Kubernetes assets.

Relevant changes may include changes to configuration, dependencies, build requirements, or runtime behavior.

### Contributions to the central repository

Working groups are encouraged to contribute corresponding Helm chart, Dockerfile, and release workflow updates directly to `cf-k8s-releases`.

The repository remains the home for assets whose ownership has not been transferred. Its maintainers continue to maintain and publish those assets, supported by notifications and contributions from the component-owning working groups.

### Optional ownership transfer

Working groups that want full control over their Kubernetes assets and release pipelines may move those assets from `cf-k8s-releases` to a repository of their choice. This may be the corresponding BOSH release repository or another repository selected by the working group.

Taking ownership means accepting full responsibility for maintaining, building, and publishing the assets and keeping them aligned with the component.

Ownership transfers happen independently for each component, at the working group's chosen pace. There is no requirement for all assets to move out of `cf-k8s-releases`.

### Publishing continuity

An ownership transfer must preserve existing chart and image names and registry locations. Charts continue to be published to `oci://ghcr.io/cloudfoundry/helm` and images to `ghcr.io/cloudfoundry/k8s`.

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
