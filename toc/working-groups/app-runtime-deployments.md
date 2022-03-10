# App Runtime Deployments: Working Group Charter

## Mission

Provide reference deployments of the CF App Runtime to CF community end users, CF community contributors, and CF commercial vendors.


## Goals

- Community end users can install, evaluate, and operate the CF App Runtime on their preferred infrastructure targets.
- Community end users can understand clear limits of operational scope for reference deployments.
- Community contributors can integrate their component changes into the appropriate reference deployments and verify correct behavior for both new and existing CF App Runtime functionality.
- Vendors and service providers can base their own commercial distributions and offerings of the CF App Runtime on a common starting point for the applicable infrastructure.


## Scope

- Package and release reference CF App Runtime deployments for different platforms, such as BOSH and, maybe in future, Kubernetes.
- Maintain public roadmaps for each reference deployment.
- Collaborate with other Working Groups to ensure that App Runtime components are integrated regularly into the community deployments.
- Provide the community with tooling and reference pipelines needed to build and release the CF reference deployments.
- Provide the community with test suites to assess functionality and behavioral compatibility of a CF deployment. Collaborate with other Working Groups on the test suites.
- Publicly operate the tooling and reference pipelines to build and release CF reference deployments regularly.
- Provide sensible defaults and sufficient configurability in the reference deployments for the needs of the community, contributors, and commercializing vendors while maintaining reasonable scope for the working group operation.
- Ensure upgrade pathways for reference deployments, with disruptive changes communicated clearly.


## Non-Goals

- Provide significant extensions or other major projects in the CF App Runtime reference deployments, such as managed services or extension clients.

## Roles & Technical Assets
Existing CF App Runtime deployments, namely cf-deployment.

```yaml
name: App Runtime Deployments
execution_leads:
- name: Jochen Ehret
  github: jochenehret
technical_leads:
- name: Jochen Ehret
  github: jochenehret
areas:
- name: CF Deployment
  approvers:
  - github: davewalter
    name: Dave Walter
  - github: ctlong
    name: Carson Long
  - github: tjvman
    name: Tom Viehman
  - github: philippthun
    name: Philipp Thun
  - github: johha
    name: Johannes Haass
  - github: svkrieger
    name: Sven Krieger
  - github: iaftab-alam
    name: Aftab Alam
  - github: jimconner
    name: Jim Conner
  - github: andrewdriver123
    name: Andrew Driver
  - github: combor
    name: Piotr Komborski
  - github: shaun7pan
    name: Shaun Pan
  repositories:
  - cloudfoundry/cf-deployment
  - cloudfoundry/cf-deployment-concourse-tasks
  - cloudfoundry/cf-acceptance-tests
  - cloudfoundry/cf-smoke-tests
  - cloudfoundry/cf-smoke-tests-release
  - cloudfoundry/uptimer
  - cloudfoundry/runtime-ci
```
