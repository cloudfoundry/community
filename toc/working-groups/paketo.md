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
- name: Forest Eckhardt
  github: ForestEckhardt
- name: Daniel Mikusa
  github: dmikusa
- name: Jan von Löwenstein
  github: loewenstein
technical_leads:
- name: Forest Eckhardt
  github: ForestEckhardt
- name: Daniel Mikusa
  github: dmikusa
- name: Jan von Löwenstein
  github: loewenstein
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
  reviewers:
- name: Builders
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Jerico Pena
    github: jericop
  - name: Sophie Wigmore
    github: sophiewigmore
- name: Content
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Victoria Campbell
    github: TisVictress
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Tim Hitchener
    github: thitch97
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
- name: Dependencies
  approvers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Brayan Henao
    github: brayanhenao
  - name: Sophie Wigmore
    github: sophiewigmore
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Joshua Casey
    github: joshuatcasey
- name: Dotnet Core
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Sophie Wigmore
    github: sophiewigmore
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Joshua Casey
    github: joshuatcasey
- name: Go
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Genevieve L'Esperance
    github: genevieve
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Victoria Campbell
    github: TisVictress
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
  - name: Kevin Ortega
    github: kevin-ortega
  - name: Hank Ibell
    github: hibell
- name: NodeJS
  approvers:
  - name: Tim Hitchener
    github: thitch97
  - name: Brayan Henao
    github: brayanhenao
  - name: Victoria Campbell
    github: TisVictress
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
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Frankie G-J
    github: fg-j
  - name: Emily Johnson
    github: emmjohnson
- name: PHP
  approvers:
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  reviewers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Frankie G-J
    github: fg-j
  - name: Victoria Campbell
    github: TisVictress
  - name: Joshua Casey
    github: joshuatcasey
- name: Python
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Brayan Henao
    github: brayanhenao
  - name: Joshua Casey
    github: joshuatcasey
  reviewers:
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Victoria Campbell
    github: TisVictress
  - name: Emily Johnson
    github: emmjohnson
- name: Ruby
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  reviewers:
  - name: Tim Hitchener
    github: thitch97
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Frankie G-J
    github: fg-j
  - name: Genevieve L'Esperance
    github: genevieve
- name: Rust
  approvers:
  reviewers:
- name: Stacks
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: Forest Eckhardt
    github: ForestEckhardt
  reviewers:
- name: Tooling
  approvers:
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  - name: Tim Hitchener
    github: thitch97
  - name: Philipp Stehle
    github: phil9909
- name: Utilities
  approvers:
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
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Frankie G-J
    github: fg-j
  - name: Emily Johnson
    github: emmjohnson
- name: Web Servers
  approvers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Tim Hitchener
    github: thitch97
  - name: Forest Eckhardt
    github: ForestEckhardt
  - name: Victoria Campbell
    github: TisVictress
  reviewers:
  - name: Rob Dimsdale-Zucker
    github: robdimsdale
  - name: Sophie Wigmore
    github: sophiewigmore
  - name: Frankie G-J
    github: fg-j
```