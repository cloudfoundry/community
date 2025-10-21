# Paketo: Working Group Charter

## Mission

Provides Paketo buildpacks for servers, languages, and frameworks popular with application developers.

## Goals

- Provides end users with stable, reliable and performant buildpacks with which to build their application.
- Provides end users with buildpacks that are compatible with multiple platforms (such as Cloud Foundry, Docker, and Kubernetes).
- Provides documentation to enable platforms to adopt Paketo buildpacks and maintain compatibility with Paketo buildpacks.

## Scope

- Provide the community with regular releases of Paketo buildpacks.
- Provide timely releases to address CVEs.
- Maintain public roadmaps for the development of Paketo.
- Provide the community with technical and end user documentation.
- Collaborate with App Runtime Interfaces WG to enable Paketo buildpacks to have first-class support in Cloud Foundry.

## Non-Goals

- Maintaining V2 (classic) buildpacks

## Working Group Governance Structure

[Working group governance structure](https://github.com/paketo-buildpacks/community/blob/main/GOVERNANCE.md)

## Membership

[Working group membership](https://github.com/paketo-buildpacks/community/blob/main/TEAMS.md)

## Roles & Technical Assets

Technical assets for the Paketo working group are contained in the following Github Organizations:

- [github.com/paketo-buildpacks](https://github.com/paketo-buildpacks)
- [github.com/paketo-community](https://github.com/paketo-community)

```yaml
name: Paketo
execution_leads:
- name: Jerico Pena
  github: jericop
- name: Daniel Mikusa
  github: dmikusa
- name: Jan von Löwenstein
  github: loewenstein-sap
technical_leads:
- name: Jerico Pena
  github: jericop
- name: Daniel Mikusa
  github: dmikusa
- name: Jan von Löwenstein
  github: loewenstein-sap
bots:
- name: paketo-bot
  github: paketo-bot
- name: paketo-bot-reviewer
  github: paketo-bot-reviewer
areas:
- name: App Monitoring
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: Joshua Casey
    github: joshuatcasey
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  - name: Anthony Dahanne
    github: anthonydahanne
  reviewers: []
  repositories: []
- name: Builders
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Michael Dawson
    github: mhdawson
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Jerico Pena
    github: jericop
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories: []
- name: Content
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Anthony Dahanne
    github: anthonydahanne
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories: []
- name: Dependencies
  approvers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Dotnet Core
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Go
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Genevieve L'Esperance
    github: genevieve
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories: []
- name: Java
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: Anthony Dahanne
    github: anthonydahanne
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  reviewers:
  - name: Ralf Pannemans
    github: c0d1ngm0nk3y
  - name: Johannes Dillmann
    github: modulo11
  repositories: []
- name: NodeJS
  approvers:
  - name: Michael Dawson
    github: mhdawson
  - name: Costas Papastathis
    github: pacostas
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Ames
    github: accrazed
  - name: Ralf Pannemans
    github: c0d1ngm0nk3y
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Emily Johnson
    github: emmjohnson
  repositories: []
- name: PHP
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  reviewers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Python
  approvers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Joshua Casey
    github: joshuatcasey
  reviewers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Emily Johnson
    github: emmjohnson
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Ruby
  approvers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Genevieve L'Esperance
    github: genevieve
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Rust
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: Forest Eckhardt
    github: ForestEckhardt
  reviewers: []
  repositories: []
- name: Stacks
  approvers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Michael Dawson
    github: mhdawson
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Jerico Pena
    github: jericop
  repositories: []
- name: Tooling
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  repositories: []
- name: Utilities
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: David O'Sullivan
    github: pivotal-david-osullivan
  reviewers:
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Anthony Dahanne
    github: anthonydahanne
  repositories: []
- name: Web Servers
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Forest Eckhardt
    github: ForestEckhardt
  reviewers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  repositories: []
```
