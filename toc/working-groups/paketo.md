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
- name: Anthony Dahanne
  github: anthonydahanne
- name: Daniel Mikusa
  github: dmikusa
- name: Jerico Pena
  github: jericop
technical_leads:
- name: Anthony Dahanne
  github: anthonydahanne
- name: Daniel Mikusa
  github: dmikusa
- name: Jerico Pena
  github: jericop
bots:
- name: paketo-bot
  github: paketo-bot
- name: paketo-bot-reviewer
  github: paketo-bot-reviewer
areas:
- name: App Monitoring
  approvers:
  - name: Anthony Dahanne
    github: anthonydahanne
  - name: Daniel Mikusa
    github: dmikusa
  reviewers:
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Builders
  approvers:
  - name: Jerico Pena
    github: jericop
  - name: Costas Papastathis
    github: pacostas
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Content
  approvers:
  - name: Anthony Dahanne
    github: anthonydahanne
  - name: Jan von Löwenstein
    github: loewenstein
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  repositories: []
- name: Dependencies
  approvers:
  - name: Jerico Pena
    github: jericop
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Dotnet Core
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  - name: Brynley McDonald
    github: ZephireNZ
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Go
  approvers:
  - name: Jerico Pena
    github: jericop
  - name: Samuel Gaist
    github: sgaist
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Java
  approvers:
  - name: Anthony Dahanne
    github: anthonydahanne
  - name: Daniel Mikusa
    github: dmikusa
  - name: Jerico Pena
    github: jericop
  reviewers:
  - name: Ralf Pannemans
    github: c0d1ngm0nk3y
  - name: Johannes Dillmann
    github: modulo11
  repositories: []
- name: NodeJS
  approvers:
  - name: Costas Papastathis
    github: pacostas
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Ralf Pannemans
    github: c0d1ngm0nk3y
  repositories: []
- name: PHP
  approvers:
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Michael Both
    github: ionphractal
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Python
  approvers:
  - name: Jerico Pena
    github: jericop
  - name: Samuel Gaist
    github: sgaist
  - name: Stanislav Khlud
    github: TheSuperiorStanislav
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Joshua Casey
    github: joshuatcasey
  repositories: []
- name: Ruby
  approvers:
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Michael Both
    github: ionphractal
  repositories: []
- name: Rust
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  reviewers: []
  repositories: []
- name: Stacks
  approvers:
  - name: Jerico Pena
    github: jericop
  - name: Costas Papastathis
    github: pacostas
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Tooling
  approvers:
  - name: Jerico Pena
    github: jericop
  - name: Johannes Dillmann
    github: modulo11
  - name: Nicolas Bender
    github: nicolasbender
  - name: Costas Papastathis
    github: pacostas
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  - name: Daniel Mikusa
    github: dmikusa
  repositories: []
- name: Utilities
  approvers:
  - name: Anthony Dahanne
    github: anthonydahanne
  - name: Daniel Mikusa
    github: dmikusa
  - name: Jerico Pena
    github: jericop
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
- name: Web Servers
  approvers:
  - name: Daniel Mikusa
    github: dmikusa
  reviewers:
  - name: Arjun Sreedharan
    github: arjun024
  repositories: []
```
