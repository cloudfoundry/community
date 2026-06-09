# Meta
[meta]: #meta
- Name: Establish a Windows-Capable Buildpacks Working Group Area
- Start Date: TBD
- Author(s): @Gerg
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs: [RFC Draft: Deprecate and Remove Windows Support in Binary Buildpack](https://github.com/cloudfoundry/community/blob/rfc-deprecate-windows-support-binary-buildpack/toc/rfc/rfc-draft-deprecate-and-remove-windows-support-in-binary-buildpack.md)

## Summary

Establish a "Windows-Capable Buildpacks" area within the App Runtime Interfaces (ARI) working group to maintain buildpacks that run on Windows and require Windows infrastructure to validate. 

## Problem

The binary buildpack's Windows support has become unmaintained following the departure of previous maintainers. A [related RFC](https://github.com/cloudfoundry/community/blob/rfc-deprecate-windows-support-binary-buildpack/toc/rfc/rfc-draft-deprecate-and-remove-windows-support-in-binary-buildpack.md) proposes removing Windows support entirely.

However, deprecating Windows support in the binary buildpack is, in effect, deprecating Windows support for CF as a whole: without a maintained buildpack that can exercise the Windows runtime interface, the Windows support in CF cannot be properly validated. Windows support is a differentiating feature of CF with active community consumers, and this decision warrants more deliberation than a single buildpack RFC.

The `binary-buildpack` and `hwc-buildpack` repositories are currently in the [App Runtime Interfaces "Buildpacks and Stacks" area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-interfaces.md). The buildpack code itself is not the core difficulty — the binary buildpack in particular is conceptually simple (it stages and runs a pre-compiled executable). The real barrier is maintaining Windows CI: provisioning and operating Windows runtimes and stemcells to run integration tests and validate platform compatibility.

The existing "Buildpacks and Stacks" approvers have buildpack domain expertise but not Windows infrastructure expertise. That infrastructure knowledge exists elsewhere in the community:

- The App Runtime Platform [Garden Containers area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-platform.md) maintains `winc-release`, `windows2019fs-release`, and related Windows container components.
- The Foundational Infrastructure [VM deployment lifecycle area](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/foundational-infrastructure.md) maintains `bosh-windows-stemcell-builder`, `stembuild`, and `windows-utilities-release`.

These teams already operate Windows infrastructure for their own CI. This expertise and infrastructure has not been leveraged for Windows buildpack validation.

## Proposal

Add a "Windows-Capable Buildpacks" area to the [App Runtime Interfaces working group charter](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-interfaces.md), and move the relevant buildpack repositories into it from the existing "Buildpacks and Stacks" area.

The unifying concern of this area is that all member repos run on Windows and require Windows test environments to validate, and therefore need dedicated ownership from people with Windows infrastructure expertise alongside buildpack domain expertise.

The new area MUST:

- Include approvers drawn from both current buildpack maintainers (from the existing "Buildpacks and Stacks" area) and Windows infrastructure specialists from the App Runtime Platform and/or Foundational Infrastructure working groups.
- Own the `binary-buildpack` and `binary-buildpack-release` repositories, maintaining support for both Linux and Windows runtimes.

The new area MAY:
- Share Windows CI infrastructure with the App Runtime Platform or Foundational Infrastructure working groups, which already operate Windows Diego cells and stemcells for their own CI.

### HWC Buildpack

The `hwc-buildpack` and `hwc-buildpack-release` repositories face the same maintenance challenges and belong in this area for the same reason: they run on Windows and require Windows CI infrastructure to validate. The TOC SHOULD determine which of the following applies:

1. Include the HWC buildpack repositories in this area, if there is sufficient community interest in maintaining them.
2. Deprecate the HWC buildpack separately via its own RFC, if no maintainers come forward. The binary buildpack alone is sufficient to exercise the Windows runtime interface for validation purposes.

## Alternatives

- **Alternative: Deprecate Windows support** (the approach in the related RFC) — this effectively ends CF's Windows story and should only be pursued after community interest has been assessed and no maintainers have come forward.
- **Alternative: Do nothing** — leaves the binary buildpack's Windows code unmaintained and unvalidated.
