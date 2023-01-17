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

## Roles & Technical Assets
Components from the App Autoscaler, CAPI, CLI, Java Tools, MultiApps, Notifications, and Stratos projects.

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
  - name: Kevin Cross
    github: KevinJCross
  - name: Alan Morán
    github: bonzofenix
  - name: Jörg Weisbarth
    github: joergdw
  - name: Marcin Kubica
    github: marcinkubica
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

- name: Buildpacks
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  - name: Arjun Sreedharan
    github: arjun024
  - name: Brayan Henao
    github: brayanhenao
  - name: Ryan Moran
    github: ryanmoran
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Forest Eckhardt
    github: ForestEckhardt
  repositories:
  - cloudfoundry/cflinuxfs3
  - cloudfoundry/cflinuxfs4
  - cloudfoundry/java-buildpack
  - cloudfoundry/java-buildpack-memory-calculator
  - cloudfoundry/java-buildpack-release
  - cloudfoundry/java-buildpack-system-test
  - cloudfoundry/java-buildpack-dependency-builder
  - cloudfoundry/java-buildpack-container-customizer
  - cloudfoundry/java-test-applications
  - cloudfoundry/java-buildpack-support
  - cloudfoundry/java-buildpack-security-provider
  - cloudfoundry/java-buildpack-metric-writer
  - cloudfoundry/java-buildpack-client-certificate-mapper
  - cloudfoundry/java-buildpack-auto-reconfiguration
  - cloudfoundry/ibm-websphere-liberty-buildpack
  - cloudfoundry/nodejs-buildpack
  - cloudfoundry/nodejs-buildpack-release
  - cloudfoundry/php-buildpack
  - cloudfoundry/php-buildpack-release
  - cloudfoundry/ruby-buildpack
  - cloudfoundry/ruby-buildpack-release
  - cloudfoundry/python-buildpack
  - cloudfoundry/python-buildpack-release
  - cloudfoundry/go-buildpack
  - cloudfoundry/go-buildpack-release
  - cloudfoundry/binary-buildpack
  - cloudfoundry/binary-buildpack-release
  - cloudfoundry/dotnet-core-buildpack
  - cloudfoundry/dotnet-core-buildpack-release
  - cloudfoundry/hwc-buildpack
  - cloudfoundry/hwc-buildpack-release
  - cloudfoundry/nginx-buildpack
  - cloudfoundry/nginx-buildpack-release
  - cloudfoundry/staticfile-buildpack
  - cloudfoundry/staticfile-buildpack-release
  - cloudfoundry/r-buildpack
  - cloudfoundry/r-buildpack-release
  - cloudfoundry/apt-buildpack
  - cloudfoundry/docs-buildpacks
  - cloudfoundry/brats
  - cloudfoundry/binary-builder
  - cloudfoundry/buildpack-packager
  - cloudfoundry/buildpacks-envs
  - cloudfoundry/buildpacks-workstation
  - cloudfoundry/buildpacks-ci
  - cloudfoundry/buildpacks-feature-eng-ci
  - cloudfoundry/buildpacks-github-config
  - cloudfoundry/cflinuxfs3-release
  - cloudfoundry/cflinuxfs4-release
  - cloudfoundry/dagger
  - cloudfoundry/example-sidecar-buildpack
  - cloudfoundry/jvmkill
  - cloudfoundry/libbuildpack
  - cloudfoundry/pip-pop
  - cloudfoundry/public-buildpacks-ci-robots
  - cloudfoundry/stack-auditor
  - cloudfoundry/switchblade
  - cloudfoundry/core-deps-ci
  - cloudfoundry/app-runtime-interfaces-infrastructure

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
  repositories:
  - cloudfoundry/cloud_controller_ng
  - cloudfoundry/capi-release
  - cloudfoundry/capi-dockerfiles
  - cloudfoundry/capi-bara-tests
  - cloudfoundry/capi-k8s-release
  - cloudfoundry/capi-ci
  - cloudfoundry/capi-ci-private
  - cloudfoundry/capi-env-pool
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
  approvers:
  - name: David Stevenson
    github: dsboulder
  - name: Gareth Smith
    github: totherme
  - name: Diego Lemos
    github: dlresende
  - name: Fernando Naranjo
    github: fejnartal
  repositories:
  - cloudfoundry/notifications-release
  - cloudfoundry/notifications
  - cloudfoundry/app-runtime-interfaces-infrastructure

```
