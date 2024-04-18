# Meta
[meta]: #meta
- Name: Distribute Public Community Images using Github Packages Container Registry instead of DockerHub
- Start Date: 2024-04-18
- Author(s): @tcdowney
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Move away from DockerHub and distribute official Cloud Foundry container images using the [Github Packages](https://github.com/features/packages) [Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry). This RFC is primarily concerned with public container images that are published for the Cloud Foundry community.

## Terminology

* **Community Image -** A public container image that is intended to be consumed by members of the Cloud Foundry community.  Some examples are the `cloudfoundry/cli` and `cloudfoundry/cflinuxfs4` images that are published by the CLI and Buildpacks teams.
* **Team Image -** A container image that a team publishes for its own internal use (e.g. for use in CI). These images may or may not be public.

## Problem

Currently some working groups distribute container images for consumption by the Cloud Foundry community through the [CloudFoundry DockerHub org](https://hub.docker.com/repositories/cloudfoundry).

Managing DockerHub accounts adds additional overhead to the release processes for these teams. By switching to using Github Packages, teams can use their existing Github accounts to publish images.

It is also unclear what the long-term costs of using DockerHub will be. I believe that the `cloudfoundry` org is currently covered by the [Docker-sponsored Open Source program](https://docs.docker.com/trusted-content/dsos-program/), but [Github Package usage is free for public packages](https://docs.github.com/en/billing/managing-billing-for-github-packages/about-billing-for-github-packages#about-billing-for-github-packages).

## Proposal

### Deprecation Period
A deprecation period of 3 months *MUST* be communicated through the cf-dev mailing list and via the READMEs of the images on DockerHub. References to the DockerHub images *MUST* be updated in documentation and code repository READMEs. Community images will continue to be published to DockerHub during this period. Old Community Images *MUST* not be deleted, but the floating tags (i.e. `latest`) *MUST* be deleted to alert consumers that they are no longer using updated versions of the images.

### Community Images
Teams *MUST* begin publishing new Community Images to the Cloud Foundry Organizations [Github Packages repository](https://github.com/orgs/cloudfoundry/packages) and during the deprecation window teams *MUST* continue to publish images to DockerHub. Once the deprecation period has ended teams *MUST* no longer publish new Community Images to DockerHub. 

### Internal Images
This RFC is primarily concerned with public Community Images, but generally teams *SHOULD* migrate their Team Images off of DockerHub to Github Container Registry or to registries aligned with their existing IaaS accounts (e.g. a team that uses GCP may use Google Artifact Registry).

