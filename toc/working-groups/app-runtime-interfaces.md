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
- Provide a CF API suitable for the different CF deployment scenarios: from small to very large foundations, VM-based, support for major IaaS providers.
- Provide the community with pipelines and test suites to validate functionality, compatibility and performance of the CF API.
- Provide the community with technical API documentation, end user documentation and operator documentation.
- Collaborate with the other Working Groups and evolve the cf-push experience.
- Where it is appropriate, integrate higher-level API extensions into CF API directly.


## Non-Goals

- Provide the community with 'all' language specific CF clients libraries.

## Roles & Technical Assets

Components from the App Autoscaler, CAPI, CLI, Java Tools, MultiApps, and Notifications projects.

```yaml
name: App Runtime Interfaces
execution_leads:
- name: Greg Cobb
  github: gerg
technical_leads:
- name: Greg Cobb
  github: gerg
bots:
- name: App Autoscaler CI Bot
  github: app-autoscaler-ci-bot
- name: Cloud Foundry Buildpacks Team Robot
  github: cf-buildpacks-eng
- name: capi-bot
  github: capi-bot
areas:
- name: Autoscaler
  approvers:
  - name: Arsalan Khan
    github: asalan316
  - name: Silvestre Zabala
    github: silvestre
  - name: Jörg Weisbarth
    github: joergdw
  - name: Oliver Mautschke
    github: olivermautschke
  reviewers:
  - name: Susanne Salzmann
    github: salzmannsusan
  repositories:
  - cloudfoundry/app-autoscaler-release
  - cloudfoundry/app-autoscaler-cli-plugin
  - cloudfoundry/app-autoscaler-env-bbl-state
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Buildpacks Docs
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Victoria Campbell
    github: TisVictress
  repositories:
  - cloudfoundry/docs-buildpacks
  - cloudfoundry/example-sidecar-buildpack

- name: Buildpacks Go
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/go-buildpack
  - cloudfoundry/go-buildpack-release

- name: Buildpacks Java
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  reviewers:
  - name: Anthony Dahanne
    github: anthonydahanne
  repositories:
  - cloudfoundry/ibm-websphere-liberty-buildpack
  - cloudfoundry/java-buildpack
  - cloudfoundry/java-buildpack-auto-reconfiguration
  - cloudfoundry/java-buildpack-client-certificate-mapper
  - cloudfoundry/java-buildpack-container-customizer
  - cloudfoundry/java-buildpack-dependency-builder
  - cloudfoundry/java-buildpack-memory-calculator
  - cloudfoundry/java-buildpack-metric-writer
  - cloudfoundry/java-buildpack-release
  - cloudfoundry/java-buildpack-security-provider
  - cloudfoundry/java-buildpack-support
  - cloudfoundry/java-buildpack-system-test
  - cloudfoundry/java-test-applications
  - cloudfoundry/jvmkill

- name: Buildpacks .Net Core
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/dotnet-core-buildpack
  - cloudfoundry/dotnet-core-buildpack-release

- name: Buildpacks .NET Framework
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Victoria Campbell
    github: TisVictress
  repositories:
  - cloudfoundry/hwc-buildpack
  - cloudfoundry/hwc-buildpack-release

- name: Buildpacks Node.js
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Tim Hitchener
    github: thitch97
  - name: Victoria Campbell
    github: TisVictress
  repositories:
  - cloudfoundry/nodejs-buildpack
  - cloudfoundry/nodejs-buildpack-release

- name: Buildpacks PHP
  approvers:
  - name: Tim Hitchener
    github: thitch97
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Arjun Sreedharan
    github: arjun024
  repositories:
  - cloudfoundry/php-buildpack
  - cloudfoundry/php-buildpack-release

- name: Buildpacks Python
  approvers:
  - name: Tim Hitchener
    github: thitch97
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/pip-pop
  - cloudfoundry/python-buildpack
  - cloudfoundry/python-buildpack-release

- name: Buildpacks R
  approvers:
  - name: Tim Hitchener
    github: thitch97
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/r-buildpack
  - cloudfoundry/r-buildpack-release

- name: Buildpacks Ruby
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/ruby-buildpack
  - cloudfoundry/ruby-buildpack-release

- name: Buildpacks Stacks
  approvers:
  - name: Brayan Henao
    github: brayanhenao
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/cflinuxfs3
  - cloudfoundry/cflinuxfs3-release
  - cloudfoundry/cflinuxfs4
  - cloudfoundry/cflinuxfs4-compat-release
  - cloudfoundry/cflinuxfs4-release
  - cloudfoundry/stack-auditor

- name: Buildpacks Tooling
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  repositories:
  - cloudfoundry/binary-builder
  - cloudfoundry/brats
  - cloudfoundry/buildpack-packager
  - cloudfoundry/buildpacks-ci
  - cloudfoundry/buildpacks-envs
  - cloudfoundry/buildpacks-feature-eng-ci
  - cloudfoundry/buildpacks-github-config
  - cloudfoundry/buildpacks-workstation
  - cloudfoundry/core-deps-ci
  - cloudfoundry/dagger
  - cloudfoundry/libbuildpack
  - cloudfoundry/public-buildpacks-ci-robots
  - cloudfoundry/switchblade

- name: Buildpacks Utilities
  approvers:
  - name: Ryan Moran
    github: ryanmoran
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Tim Hitchener
    github: thitch97
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  reviewers:
  - name: Anthony Dahanne
    github: anthonydahanne
  repositories:
  - cloudfoundry/apt-buildpack
  - cloudfoundry/binary-buildpack
  - cloudfoundry/binary-buildpack-release

- name: Buildpacks Web Servers
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Victoria Campbell
    github: tisvictress
  repositories:
  - cloudfoundry/nginx-buildpack
  - cloudfoundry/nginx-buildpack-release
  - cloudfoundry/staticfile-buildpack
  - cloudfoundry/staticfile-buildpack-release

- name: CAPI
  approvers:
  - name: Tom Viehman
    github: tjvman
  - name: Florian Braun
    github: FloThinksPi
  - name: Philipp Thun
    github: philippthun
  - name: Merric de Launey
    github: MerricdeLauney
  - name: Johannes Haass
    github: johha
  - name: Michael Oleske
    github: moleske
  - name: Seth Boyles
    github: sethboyles
  - name: Sven Krieger
    github: svkrieger
  reviewers:
  - name: Alex Rocha
    github: xandroc
  - name: David Alvarado
    github: dalvarado
  - name: Katharina Przybill
    github: kathap
  - name: Will Gant
    github: will-gant
  - name: Evan Farrar
    github: evanfarrar
  - name: Daniel Felipe Ochoa
    github: danielfor
  - name: Shwetha Gururaj
    github: gururajsh
  repositories:
  - cloudfoundry/cloud_controller_ng
  - cloudfoundry/capi-release
  - cloudfoundry/capi-dockerfiles
  - cloudfoundry/capi-bara-tests
  - cloudfoundry/capi-ci
  - cloudfoundry/capi-ci-private
  - cloudfoundry/capi-env-pool
  - cloudfoundry/capi-team-checklists
  - cloudfoundry/cf-performance-tests
  - cloudfoundry/cf-performance-tests-pipeline
  - cloudfoundry/tps
  - cloudfoundry/cc-uploader
  - cloudfoundry/sync-integration-tests
  - cloudfoundry/go-cf-api
  - cloudfoundry/go-cf-api-release
  - cloudfoundry/blobstore_url_signer
  - cloudfoundry/capi-workspace
  - cloudfoundry/delayed_job_sequel
  - cloudfoundry/stack-auditor
  - cloudfoundry/steno
  - cloudfoundry/runtimeschema
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: CLI
  approvers:
  - name: Al Berez
    github: a-b
  - name: Juan Diego González
    github: jdgonzaleza
  - name: Ryker Reed
    github: reedr3
  reviewers:
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Christhian
    github: ccjaimes
  - name: Pete Levine
    github: PeteLevineA
  - name: Michael Oleske
    github: moleske
  - name: Shwetha Guraraj
    github: gururajsh
  repositories:
  - cloudfoundry/cli
  - cloudfoundry/cli-i18n
  - cloudfoundry/cli-ci
  - cloudfoundry/cli-plugin-repo
  - cloudfoundry/claw
  - cloudfoundry/cli-docs-scripts
  - cloudfoundry/cli-workstation
  - cloudfoundry/cli-private
  - cloudfoundry/cli-pools
  - cloudfoundry/jsonry
  - cloudfoundry/stack-auditor
  - cloudfoundry/ykk
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Docs
  approvers:
  - name: Chloe Hollingsworth
    github: cshollingsworth
  - name: Anita Flegg
    github: anita-flegg
  - name: Samia Nneji
    github: snneji
  - name: Ben Klein
    github: fifthposition
  - name: Ajayan Borys
    github: HenryBorys
  - name: Bob Graczyk
    github: bobbygeeze
  - name: Kelly OHara
    github: kohara88
  - name: Jason Andrew
    github: VMWare-JasonAndrew 
  repositories:
  - cloudfoundry/docs-buildpacks
  - cloudfoundry/docs-cf-cli
  - cloudfoundry/docs-cloudfoundry-concepts
  - cloudfoundry/docs-dev-guide
  - cloudfoundry/docs-services
  - cloudfoundry/docs-dotnet-core-tutorial
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Java Tools
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  reviewers:
  - name: Anthony Dahanne
    github: anthonydahanne  
  repositories:
  - cloudfoundry/cf-java-client
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: MultiApps
  approvers:
  - name: Alexander Tsvetkov
    github: nictas
  - name: Ivan Dimitrov
    github: IvanBorislavovDimitrov
  - name: Kristian Atanasov
    github: theghost5800
  - name: Boyan Velinov
    github: boyan-velinov
  - name: Rangel Ivanov
    github: radito3
  - name: Dido
    github: ddonchev
  - name: Ikasarov
    github: ikasarov
  - name: Abil Dermendzhiev
    github: abdermendz
  - name: Velizar Kalapov
    github: vkalapov
  - name: Nikolay Valchev
    github: nvvalchev
  repositories:
  - cloudfoundry/multiapps-controller
  - cloudfoundry/multiapps-cli-plugin
  - cloudfoundry/multiapps
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Notifications
  bots:
  - name: VMware notifications release bot
    github: cf-frontend
  approvers:
  - name: David Stevenson
    github: dsboulder
  repositories:
  - cloudfoundry/notifications-release
  - cloudfoundry/notifications
  - cloudfoundry/app-runtime-interfaces-infrastructure

```
