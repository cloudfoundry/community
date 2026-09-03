# Meta
[meta]: #meta
- Name: Establish a Windows Buildpacks Working Group Area
- Start Date: 2026-07-22
- Author(s): @Gerg
- Status: Accepted
- RFC Pull Request: [community#1567](https://github.com/cloudfoundry/community/pull/1567)
- Related RFCs: [RFC Draft: Deprecate and Remove Windows Support in Binary Buildpack](https://github.com/cloudfoundry/community/blob/rfc-deprecate-windows-support-binary-buildpack/toc/rfc/rfc-0059-deprecate-and-remove-windows-support-in-binary-buildpack.md)

## Summary

Establish a "Windows Buildpacks" area within the App Runtime Interfaces (ARI) working group to maintain Windows compatibility for select buildpacks and the required Windows infrastructure to validate these buildpacks. 

## Problem

The binary buildpack's Windows support has become unmaintained following the departure of previous maintainers. Binary buildpack's release has been packaging a [pinned version](https://github.com/cloudfoundry/binary-buildpack-release/blame/e767ad860c466a4aeffd2cefd01ab773933992eb/config/blobs.yml) of binary buildpack for almost 2 years. A [related RFC](https://github.com/cloudfoundry/community/blob/rfc-deprecate-windows-support-binary-buildpack/toc/rfc/rfc-0059-deprecate-and-remove-windows-support-in-binary-buildpack.md) proposes removing Windows support entirely.

However, deprecating Windows support in the binary buildpack is, in effect, deprecating Windows support for CF as a whole: without a maintained buildpack that can exercise the Windows runtime interface, the Windows support in CF cannot be properly validated. Windows support is a differentiating feature of CF with active community consumers, and this decision warrants more deliberation than a single buildpack RFC.

The `binary-buildpack` and `hwc-buildpack` repositories are currently in the [App Runtime Interfaces "Buildpacks and Stacks" area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-interfaces.md). The buildpack code itself is not the core difficulty;  the binary buildpack in particular is conceptually simple (it stages and runs a pre-compiled executable). The real barrier is maintaining Windows CI: provisioning and operating Windows runtimes and stemcells to run integration tests and validate platform compatibility.

The existing "Buildpacks and Stacks" approvers have buildpack domain expertise but not Windows infrastructure expertise. That infrastructure knowledge exists elsewhere in the community:

- The App Runtime Platform [Garden Containers area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-platform.md) maintains `winc-release`, `windows2019fs-release`, and related Windows container components.
- The Foundational Infrastructure [VM deployment lifecycle area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/foundational-infrastructure.md) maintains `bosh-windows-stemcell-builder`, `stembuild`, and `windows-utilities-release`.

These teams already operate Windows infrastructure for their own CI. This expertise and infrastructure has not been leveraged for Windows buildpack validation.

## Proposal

Add a "Windows Buildpacks" area to the [App Runtime Interfaces working group charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-interfaces.md), and include the relevant buildpack repositories in it from the existing "Buildpacks and Stacks" area. These buildpack repositories will have shared ownership between the core buildpacks maintainers and the Windows buildpacks maintainers.

The unifying concern of this area is that all member repos run on Windows and require Windows test environments to validate. These repos therefore need dedicated ownership from people with Windows infrastructure expertise alongside buildpack domain expertise.

The new area MUST:

- Include approvers who are Windows infrastructure specialists from the App Runtime Platform and/or Foundational Infrastructure working groups.
- Co-own the `binary-buildpack` and `binary-buildpack-release` repositories, maintaining compatibility with the Windows runtime.
- Support Application Runtime Deployments working group with any integration or validation issues relating to the Windows buildpacks

The new area MAY:
- Share Windows CI infrastructure with the App Runtime Platform or Foundational Infrastructure working groups, which already operate Windows Diego cells and stemcells for their own CI.

### HWC Buildpack

The `hwc-buildpack` and `hwc-buildpack-release` repositories face the same maintenance challenges as the binary buildpack and belong in this area for the same reason: they run on Windows and require Windows CI infrastructure to validate. Thus, the HWC buildpack repositories will also be included in the "Windows Buildpacks" area.

## Alternatives

- **Alternative: Deprecate Windows support** (the approach in the related RFC) — this effectively ends CF's Windows story and should only be pursued after community interest has been assessed and no maintainers have come forward.
- **Alternative: Do nothing** — leaves the binary buildpack's Windows code unmaintained and unvalidated.
