# Concourse: Working Group Charter

## Mission

Provides the Concourse CI/CD platform.

## Goals
* Provides a stable and up to date CI/CD platform.

## Scope
* Maintain public roadmaps for Concourse.
* Provide the community with regular releases of Concourse.
* Provide timely releases to address CVEs.
* Provide the community with technical and end user documentation.
* Collaborate with other working groups to continue to have first-class support with Cloud Foundry.

## Non-Goals

* Require other working groups or projects to use Concourse.

## Roles & Technical Assets

Technical assets for the Concourse working group are contained in the following Github Organizations:

* [github.com/concourse](https://github.com/concourse)

```yaml
name: Concourse
org: concourse
execution_leads:
- name: Derek Richard
  github: drich10
- name: Taylor Silva
  github: taylorsilva
technical_leads:
- name: Derek Richard
  github: drich10
- name: Taylor Silva
  github: taylorsilva
bots:
- name: concourse-otto
  github: concourse-otto
- name: concourse-bot
  github: concourse-bot
areas:
- name: Core
  approvers:
  - name: Indira
    github: ichandrabhatta
  - name: Wayne Adams
    github: wayneadams
  - name: Claire Tinati
    github: Spimtav
  - name: Harish Yayi
    github: yharish991
  - name: Ivan Chalukov
    github: IvanChalukov
  - name: Kump3r
    github: Kump3r
  repositories:
  - concourse/bosh-io-release-resource
  - concourse/bosh-io-stemcell-resource
  - concourse/ci
  - concourse/concourse
  - concourse/concourse-bosh-deployment
  - concourse/concourse-bosh-release
  - concourse/concourse-chart
  - concourse/concourse-docker
  - concourse/dex
  - concourse/docker-image-resource
  - concourse/docs
  - concourse/examples
  - concourse/git-resource
  - concourse/github-release-resource
  - concourse/hg-resource
  - concourse/houdini
  - concourse/infrastructure
  - concourse/mock-resource
  - concourse/oci-build-task
  - concourse/pool-resource
  - concourse/registry-image-resource
  - concourse/resource-types
  - concourse/resource-types-website
  - concourse/retryhttp
  - concourse/rfcs
  - concourse/s3-resource
  - concourse/semver-resource
  - concourse/time-resource
  - concourse/.github
  # Repositories below this line are archived
  - concourse/blog
  - concourse/flag
  - concourse/prod
  - concourse/oxygen-mask
  - concourse/office-hours
  - concourse/governance
  - concourse/datadog-event-resource
  - concourse/hush-house
  - concourse/tracker-resource
  - concourse/baggageclaim
  - concourse/buildroot-images
  - concourse/concourse-pipeline-resource
```
