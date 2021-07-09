# App Runtime Deployments: Working Group Charter

## Mission

Provide reference deployments of the CF App Runtime to CF community end users, CF community contributors, and CF commercial vendors.


## Goals

- Community end users can install, evaluate, and operate the CF App Runtime on their preferred infrastructure targets.
- Community end users can understand clear limits of operational scope for reference deployments.
- Community contributors can integrate their component changes into the appropriate reference deployments and verify correct behavior for both new and existing CF App Runtime functionality.
- Vendors and service providers can base their own commercial distributions and offerings of the CF App Runtime on a common starting point for the applicable infrastructure.


## Scope

- Package and release reference CF App Runtime deployments for different platforms, such as BOSH and Kubernetes.
- Maintain public roadmaps for each reference deployment.
- Collaborate with other Working Groups to ensure that App Runtime components are integrated regularly into the community deployments.
- Provide the community with tooling and reference pipelines needed to build and release the CF reference deployments.
- Provide the community with test suites to assess functionality and behavioral compatibility of a CF deployment.
- Publicly operate the tooling and reference pipelines to build and release CF reference deployments regularly.
- Provide sensible defaults and sufficient configurability in the reference deployments for the needs of the community, contributors, and commercializing vendors while maintaining reasonable scope for the working group operation.
- Ensure upgrade pathways for reference deployments, with disruptive changes communicated clearly.


## Non-Goals

- Provide significant extensions or other major projects in the CF App Runtime reference deployments, such as managed services or extension clients.


## Open Questions (to be considered before WG formation)

- How much API and behavioral consistency should there be between official CF deployments?
- How much of that consistency should be the responsibility of this working group, when that consistency may lie within the domain of another working group (for example, one that owns Buildpacks)?


## Proposed Leadership

TBD


## Technical Assets

Existing CF App Runtime deployments: cf-deployment, KubeCF, cf-for-k8s.

Repositories:
- https://github.com/cloudfoundry/cf-deployment
- https://github.com/cloudfoundry/cf-acceptance-tests
- https://github.com/cloudfoundry/cf-smoke-tests
- https://github.com/cloudfoundry/cf-smoke-tests-release
- https://github.com/cloudfoundry/cf-for-k8s
- https://github.com/cloudfoundry-incubator/kubecf

Public, active pipelines for building and releasing CF deployments.


