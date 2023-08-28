# Docs: Working Group Charter

## Mission

To document the Cloud Foundry user experience.

## Goals

- Make a plan for regular reviews and updates
- Update and maintain READMEs for all docs repos
- Update and maintain CF book repo/Table of Contents
- Update and maintain contribution guidelines


## Scope

- Merge and edit all doc changes
- Update with the latest best practices for SEO
- Remove out-dated information
- Advise contributors on best practices

## Non-Goals

- Be responsible for component level documentation (e.g. Cloud Controller v3 docs).

## Roles & Technical Assets

```yaml
name: Documentation
execution_leads:
- name: Anita Flegg
  github: anita-flegg
technical_leads:
- name: Anita Flegg
  github: anita-flegg
config:
  generate_rfc0015_branch_protection_rules: true
  github_project_sync:
    mapping:
      cloudfoundry: 41
areas:
- name: Docs
  approvers:
  - name: Max Hufnagel
    github: animatedmax
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
  - name: Lora Boe
    github: blora1

  repositories:
  - cloudfoundry/docs-book-cloudfoundry
  - cloudfoundry/docs-cf-admin
  - cloudfoundry/docs-loggregator
  - cloudfoundry/docs-running-cf
  - cloudfoundry/docs-bbr
  - cloudfoundry/docs-credhub
  - cloudfoundry/docs-uaa
  - cloudfoundry/docs-buildpacks
  - cloudfoundry/docs-cf-cli
  - cloudfoundry/docs-cloudfoundry-concepts
  - cloudfoundry/docs-dev-guide
  - cloudfoundry/docs-services
  - cloudfoundry/docs-credhub
  - cloudfoundry/docs-dotnet-core-tutorial
  - cloudfoundry/app-runtime-interfaces-infrastructure
```
