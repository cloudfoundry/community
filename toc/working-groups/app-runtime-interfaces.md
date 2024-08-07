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
- name: Stephan Merker
  github: stephanme
technical_leads:
- name: Greg Cobb
  github: gerg
bots:
- name: Cloud Foundry Buildpacks Team Robot
  github: cf-buildpacks-eng
- name: ARI WG Git Bot
  github: ari-wg-gitbot
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
  - name: Josua Geiger
    github: geigerj0
  - name: Susanne Salzmann
    github: salzmannsusan
  - name: Alan Moran
    github: bonzofenix
  bots:
  - name: App Autoscaler CI Bot
    github: app-autoscaler-ci-bot
  repositories:
  - cloudfoundry/app-autoscaler-release
  - cloudfoundry/app-autoscaler-cli-plugin
  - cloudfoundry/app-autoscaler-env-bbl-state
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Buildpacks Docs
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/docs-buildpacks
  - cloudfoundry/example-sidecar-buildpack

- name: Buildpacks Go
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/go-buildpack
  - cloudfoundry/go-buildpack-release

- name: Buildpacks Java
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  - name: Kevin Ortega (IBM)
    github: kevin-ortega
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
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/dotnet-core-buildpack
  - cloudfoundry/dotnet-core-buildpack-release

- name: Buildpacks .NET Framework
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/hwc-buildpack
  - cloudfoundry/hwc-buildpack-release

- name: Buildpacks Node.js
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/nodejs-buildpack
  - cloudfoundry/nodejs-buildpack-release

- name: Buildpacks PHP
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/php-buildpack
  - cloudfoundry/php-buildpack-release

- name: Buildpacks Python
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/python-buildpack
  - cloudfoundry/python-buildpack-release

- name: Buildpacks R
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/r-buildpack
  - cloudfoundry/r-buildpack-release

- name: Buildpacks Ruby
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/ruby-buildpack
  - cloudfoundry/ruby-buildpack-release

- name: Buildpacks Stacks
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/cflinuxfs4
  - cloudfoundry/cflinuxfs4-compat-release
  - cloudfoundry/cflinuxfs4-release
  - cloudfoundry/stack-auditor

- name: Buildpacks Tooling
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/binary-builder
  - cloudfoundry/brats
  - cloudfoundry/buildpack-packager
  - cloudfoundry/buildpacks-ci
  - cloudfoundry/buildpacks-envs
  - cloudfoundry/buildpacks-github-config
  - cloudfoundry/buildpacks-workstation
  - cloudfoundry/dagger
  - cloudfoundry/libbuildpack
  - cloudfoundry/public-buildpacks-ci-robots
  - cloudfoundry/switchblade

- name: Buildpacks Utilities
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
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
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories:
  - cloudfoundry/nginx-buildpack
  - cloudfoundry/nginx-buildpack-release
  - cloudfoundry/staticfile-buildpack
  - cloudfoundry/staticfile-buildpack-release

- name: CAPI
  approvers:
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
  - name: Tim Downey
    github: tcdowney
  - name: Katharina Przybill
    github: kathap
  - name: Ben Fuller
    github: Benjamintf1
  - name: Sam Gunaratne
    github: samze
  reviewers:
  - name: Al Berez
    github: a-b
  - name: Alex Rocha
    github: xandroc
  - name: David Alvarado
    github: dalvarado
  - name: Evan Farrar
    github: evanfarrar
  - name: Daniel Felipe Ochoa
    github: danielfor
  - name: Shwetha Gururaj
    github: gururajsh
  - name: Jochen Ehret
    github: jochenehret
  - name: Ryker Reed
    github: reedr3
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Cristhian Peña
    github: ccjaimes
  bots:
  - name: capi-bot
    github: capi-bot
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
  - cloudfoundry/cf-performance-tests-release
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
  - name: Ryker Reed
    github: reedr3
  - name: Michael Oleske
    github: moleske
  - name: Cristhian
    github: ccjaimes
  - name: George Blue
    github: blgm
  - name: Shwetha Gururaj
    github: gururajsh
  - name: David Alvarado
    github: dalvarado
  - name: João Pereira
    github: joaopapereira
  - name: Sam Gunaratne
    github: samze
  reviewers:
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Pete Levine
    github: PeteLevineA
  - name: Tim Downey
    github: tcdowney
  - name: Michael Chinigo
    github: chinigo
  - name: Greg Weresch
    github: weresch
  bots:
  - name: CF CLI Eng
    github: cf-cli-eng
  repositories:
  - cloudfoundry/cli
  - cloudfoundry/cli-i18n
  - cloudfoundry/cli-ci
  - cloudfoundry/cli-plugin-repo
  - cloudfoundry/CLAW
  - cloudfoundry/cli-docs-scripts
  - cloudfoundry/cli-workstation
  - cloudfoundry/cli-private
  - cloudfoundry/cli-pools
  - cloudfoundry/jsonry
  - cloudfoundry/stack-auditor
  - cloudfoundry/ykk
  - cloudfoundry/app-runtime-interfaces-infrastructure
  - cloudfoundry/bosh-package-cf-cli-release

- name: Java Tools
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  - name: Anthony Dahanne
    github: anthonydahanne  
  reviewers:
  - name: Radoslav Tomov
    github: radoslav-tomov
  repositories:
  - cloudfoundry/cf-java-client
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Go Tools
  approvers:
  - name: Shawn Neal
    github: sneal
  - name: Caleb Washburn
    github: calebwashburn
  repositories:
  - cloudfoundry/go-cfclient

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
  - name: Ikasarov
    github: ikasarov
  - name: Velizar Kalapov
    github: vkalapov
  - name: Vasil Bogdanov
    github: VRBogdanov
  - name: Yavor Uzunov
    github: Yavor16
  reviewers:
  - name: Monika Noeva
    github: MNoeva
  - name: Stefan Yonkov
    github: s-yonkov-yonkov
  bots:
  - name: MultiApps Bot
    github: cf-mta-deploy-bot
    
  repositories:
  - cloudfoundry/multiapps-controller
  - cloudfoundry/multiapps-cli-plugin
  - cloudfoundry/multiapps
  - cloudfoundry/app-runtime-interfaces-infrastructure

- name: Notifications
  approvers:
  - name: David Stevenson
    github: dsboulder
  - name: Al Berez
    github: a-b
  - name: Ben Fuller
    github: Benjamintf1
  - name: Evan Farrar
    github: evanfarrar
  repositories:
  - cloudfoundry/notifications-release
  - cloudfoundry/notifications
  - cloudfoundry/app-runtime-interfaces-infrastructure

config:
  generate_rfc0015_branch_protection_rules: true
```
