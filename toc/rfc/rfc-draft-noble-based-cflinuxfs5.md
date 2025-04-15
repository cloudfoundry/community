# Meta
[meta]: #meta
- Name: Introduce cflinuxfs5 Stack Based on Ubuntu Noble (24.04)
- Start Date: 2025-04-07
- Author(s): @vpetrinski @plamen-bardarov
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

## Workstream 
### ARD WG workstream proposal:

App Runtime Deployments WG
The ARD WG will integrate the cflinuxfs5 stack into the cf-deployment project and also validate the new stack. The steps will be similar to the cflinuxfs4 adoption (see cloudfoundry/cf-deployment#989):

- Integrate cflinuxfs5-release into the "update-releases" pipeline to enable automatic version updates
- Provide an experimental ops file to integrate cflinuxfs5 and the cflinuxfs5 buildpacks (as available)
- Run CATs against a cflinuxfs5-enabled cf-deployment
- Promote experimental ops file (or integrate directly into cf-deployment.yml)
- Make cflinuxfs5 the default stack (-> major cf-d release)
- The deprecation and removal of cflinuxfs4 will happen at a later time as that stack is being supported for now.
 
