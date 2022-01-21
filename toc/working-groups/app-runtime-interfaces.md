# App Runtime Interfaces: Working Group Charter

## Mission

Provides APIs for the CF App Runtime and community clients for end users.


## Goals

- End users can build against a stable, reliable, performant and well documented CF API.
- End users can build against a stable, reliable, performant and well documented higher-level CF API related services.
- End users can choose from a range of CF API clients according to their needs: cli, UI and client libraries for selected programming languages.
- Community Contributors and especially the App Runtime Deployments WG can integrate a tested CF API release into the different CF distributions.


## Scope

- Provide the community with regular releases of the CF API, clients and higher-level CF API related services.
- Maintain public roadmaps for the CF API and the CF cli. Ensure a wise balance between stable APIs and clients, feature enhancements and deprecations.
- Provide a CF API suitable for the different CF deployment scenarios: from small to very large foundations, VM- and k8s-based, support for major IaaS providers.
- Provide the community with pipelines and test suites to validate functionality, compatibility and performance of the CF API.
- Provide the community with technical API documentation, end user documentation and operator documentation.
- Collaborate with the other Working Groups and evolve the cf-push experience.
- Where it is appropriate, integrate higher-level API extensions into CF API directly.


## Non-Goals

- Provide the community with 'all' language specific CF clients libraries.


## Proposed Membership

- Technical Lead(s): Greg Cobb @gerg
- Execution Lead(s): Greg Cobb @gerg 

### Approvers by Area
Autoscaler
- @garethjevans
- @asalan316
- @silvestre
- @KevinJCross 
- @aadeshmisra
- @bonzofenix
- @joergdw

Buildpacks
- @dmikusa-pivotal
- @pivotal-david-osullivan
- @menehune23
- @arjun024
- @brayanhenao

CAPI
- @tjvman
- @sweinstein22
- @MarcPaquette
- @JenGoldstrich
- @FloThinksPi
- @philippthun
- @andy-paine 
- @MerricdeLauney
- @monamohebbi
 
CLI
- @a-b 
- @jdgonzaleza

Docs
- @mjgutermuth

Java Tools
- @dmikusa-pivotal
- @pivotal-david-osullivan

MultiApps
- @nictas
- @IvanBorislavovDimitrov
- @theghost5800
- @boyan-velinov
- @radito3
- @ddonchev
- @ikasarov
- @abdermendz
- @vkalapov
- @nvvalchev

Notifications
- @dsboulder
- @totherme
- @dlresende
- @fejnartal

## Technical Assets

Components from the App Autoscaler, CAPI, CLI, Java Tools, MultiApps, Notifications, and Stratos projects.

Autoscaler
- https://github.com/cloudfoundry/app-autoscaler-release
- https://github.com/cloudfoundry/app-autoscaler
- https://github.com/cloudfoundry/app-autoscaler-ci
- https://github.com/cloudfoundry/app-autoscaler-cli-plugin

Buildpacks
- https://github.com/cloudfoundry/cflinuxfs3
- https://github.com/cloudfoundry/java-buildpack
- https://github.com/cloudfoundry/java-buildpack-memory-calculator
- https://github.com/cloudfoundry/java-buildpack-release
- https://github.com/cloudfoundry/java-buildpack-system-test
- https://github.com/cloudfoundry/java-buildpack-dependency-builder
- https://github.com/cloudfoundry/java-buildpack-container-customizer
- https://github.com/cloudfoundry/java-test-applications
- https://github.com/cloudfoundry/java-buildpack-support
- https://github.com/cloudfoundry/java-buildpack-security-provider
- https://github.com/cloudfoundry/java-buildpack-metric-writer
- https://github.com/cloudfoundry/java-buildpack-client-certificate-mapper
- https://github.com/cloudfoundry/java-buildpack-auto-reconfiguration
- https://github.com/cloudfoundry/ibm-websphere-liberty-buildpack
- https://github.com/cloudfoundry/nodejs-buildpack
- https://github.com/cloudfoundry/nodejs-buildpack-release
- https://github.com/cloudfoundry/php-buildpack
- https://github.com/cloudfoundry/php-buildpack-release
- https://github.com/cloudfoundry/ruby-buildpack
- https://github.com/cloudfoundry/ruby-buildpack-release
- https://github.com/cloudfoundry/python-buildpack
- https://github.com/cloudfoundry/python-buildpack-release
- https://github.com/cloudfoundry/go-buildpack
- https://github.com/cloudfoundry/go-buildpack-release
- https://github.com/cloudfoundry/binary-buildpack
- https://github.com/cloudfoundry/binary-buildpack-release
- https://github.com/cloudfoundry/nodejs-buildpack
- https://github.com/cloudfoundry/nodejs-buildpack-release
- https://github.com/cloudfoundry/dotnet-core-buildpack
- https://github.com/cloudfoundry/dotnet-core-buildpack-release
- https://github.com/cloudfoundry/hwc-buildpack
- https://github.com/cloudfoundry/hwc-buildpack-release
- https://github.com/cloudfoundry/nginx-buildpack
- https://github.com/cloudfoundry/nginx-buildpack-release
- https://github.com/cloudfoundry/staticfile-buildpack
- https://github.com/cloudfoundry/staticfile-buildpack-release
- https://github.com/cloudfoundry/r-buildpack
- https://github.com/cloudfoundry/r-buildpack-release
- https://github.com/cloudfoundry/apt-buildpack
- https://github.com/cloudfoundry/docs-buildpacks
- https://github.com/cloudfoundry/brats

CAPI
- https://github.com/cloudfoundry/api-docs
- https://github.com/cloudfoundry/cloud_controller_ng
- https://github.com/cloudfoundry/capi-release
- https://github.com/cloudfoundry/capi-dockerfiles
- https://github.com/cloudfoundry/capi-bara-tests
- https://github.com/cloudfoundry/capi-k8s-release
- https://github.com/cloudfoundry/capi-ci
- https://github.com/cloudfoundry-incubator/cf-performance-tests
- https://github.com/cloudfoundry-incubator/cf-performance-tests-pipeline
- https://github.com/cloudfoundry/tps
- https://github.com/cloudfoundry/cc-uploader
- https://github.com/cloudfoundry/sync-integration-tests

CLI
- https://github.com/cloudfoundry/cli
- https://github.com/cloudfoundry/cli-i18n
- https://github.com/cloudfoundry/cli-ci
- https://github.com/cloudfoundry/cli-plugin-repo

Docs
- https://github.com/cloudfoundry/docs-cf-cli
- https://github.com/cloudfoundry/docs-cloudfoundry-concepts
- https://github.com/cloudfoundry/docs-dev-guide
- https://github.com/cloudfoundry/docs-services

Java Tools
- https://github.com/cloudfoundry/cf-java-client

MultiApps
- https://github.com/cloudfoundry-incubator/multiapps-controller
- https://github.com/cloudfoundry-incubator/multiapps-cli-plugin
- https://github.com/cloudfoundry-incubator/multiapps

Notifications
- https://github.com/cloudfoundry-incubator/notifications-release
- https://github.com/cloudfoundry-incubator/notifications


Public, active pipelines for building and releasing the components CF deployments, to be run on CFF community infrastructure.
