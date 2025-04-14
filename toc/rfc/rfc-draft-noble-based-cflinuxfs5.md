# Meta
[meta]: #meta
- Name: Introduce cflinuxfs5 Stack Based on Ubuntu Noble (24.04)
- Start Date: 2025-04-07
- Author(s): @plamen-bardarov @vpetrinski
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Introduce a new stack, `cflinuxfs5`, based on Ubuntu 24.04 LTS (Noble Numbat), to provide an up-to-date root filesystem for application workloads.
This stack will be added alongside the current `cflinuxfs4` (Jammy-based) stack.

## Problem

The current `cflinuxfs4` stack is based on Ubuntu 22.04 LTS (Jammy). Support ends in 2027
With the release of Ubuntu 24.04 LTS (Noble), newer language runtimes, system libraries, and security updates will increasingly depend on a newer base OS.
`cflinuxfs4` does not provide forward compatibility with these updates, and long-term support planning requires us to begin adopting Noble.

## Proposal

### Produce a new `cflinuxfs5` stack based on Ubuntu Noble.
It will be introduced as a parallel stack. `cflinuxfs5` will be validated against supported buildpacks and application workloads.
The goal is to support both cflinuxfs4 and cflinuxfs5 until the end-of-life (EOL) for Jammy(cflinuxfs4).

It will be based on Ubuntu 24.04 LTS (Noble) and follow the same structure, tooling, and release process as the existing `cflinuxfs4` stack process. The production of `cflinuxfs5` belongs to the App Runtime Interfaces Working Group.

### Create new buildpack versions that are compatible with `cflinuxfs5`
The creation of a new set of buildpacks that are compatible with `cflinuxfs5`. Each buildpack will be tested against the new `cflinuxfs5` rootfs and updated as needed.
Buildpacks are expected to support both `cflinuxfs4` and `cflinuxfs5` during the transition.
Any buildpack-specific incompatibilities with Ubuntu Noble need to be tracked and patched incrementally.
 
