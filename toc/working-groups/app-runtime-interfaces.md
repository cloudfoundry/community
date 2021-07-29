# App Runtime Interfaces: Working Group Charter

## Mission

Provides APIs for the CF App Runtime and community clients for end users.


## Goals

- End users can build against a stable, reliable, performing and well documented CF API.
- End users can chose from a range of CF API clients according to their needs: cli, UI and client libraries for selected programming languages.
- Community Contributors and especially the App Runtime Deployments WG can integrate a tested CF API release into the different CF distributions.


## Scope

- Provide the community with regular releases of the CF API, clients and higher-level CF API related services.
- Maintain public roadmaps for the CF API and the CF cli. Ensure a wise balance between stable APIs and clients, feature enhancements and deprecations.
- Provide a CF API suitable for the different CF deployment scenarios: from small to very large foundations, VM- and k8s-based, support for major IaaS providers.
- Provide the community with pipelines and test suites to validate functionality, compatibility and performance of the CF API.
- Provide the community with technical API documentation, end user documentation and operator documentation.
- Collaborate with the other Working Groups and evolve the cf-push experience.


## Non-Goals

- Provide the community with 'all' language specific CF clients libraries.


## Open Questions

- Include https://github.com/cloudfoundry-community/cf-python-client as a second language binding that is under active development?
- Ownership of CF API related test projects like capi-bara-tests, cf-performance-tests, cf-smoke-tests, cf-acceptance-tests


## Proposed Membership

- Technical Lead(s): TBD
- Execution Lead(s): TBD
- Approvers: TBD


## Technical Assets

Components from the App Autoscaler, CAPI, CLI, Java Tools, MultiApps, Notifications, and Stratos projects.

Autoscaler:
- https://github.com/cloudfoundry/app-autoscaler-release
- https://github.com/cloudfoundry/app-autoscaler
- https://github.com/cloudfoundry/app-autoscaler-ci
- https://github.com/cloudfoundry/app-autoscaler-cli-plugin

CAPI:
- https://github.com/cloudfoundry/cloud_controller_ng
- https://github.com/cloudfoundry/capi-release
- https://github.com/cloudfoundry/capi-dockerfiles
- https://github.com/cloudfoundry/capi-bara-tests
- https://github.com/cloudfoundry/capi-k8s-release
- https://github.com/cloudfoundry/capi-ci
- https://github.com/cloudfoundry-incubator/cf-performance-tests

CLI
- https://github.com/cloudfoundry/cli
- https://github.com/cloudfoundry/cli-i18n
- https://github.com/cloudfoundry/cli-ci
- https://github.com/cloudfoundry/cli-plugin-repo

Java Tools
- https://github.com/cloudfoundry/cf-java-client

MultiApps
- https://github.com/cloudfoundry-incubator/multiapps-controller
- https://github.com/cloudfoundry-incubator/multiapps-cli-plugin
- https://github.com/cloudfoundry-incubator/multiapps

Notifications
- https://github.com/cloudfoundry-incubator/notifications-release
- https://github.com/cloudfoundry-incubator/notifications
- https://github.com/cloudfoundry-incubator/notifications-sendgrid-receiver

Stratos
- https://github.com/cloudfoundry/stratos
- https://github.com/cloudfoundry/stratos-buildpack


Public, active pipelines for building and releasing the components CF deployments, to be run on CFF community infrastructure.
