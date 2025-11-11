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
- Update with the latest best practices for SEO and inclusive language
- Maintain internal consistency of doc style, including Notes and tables, for example
- Remove out-dated information (ongoing)
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
bots: []
areas:
- name: Docs
  approvers:
  - name: Anita Flegg
    github: anita-flegg
  - name: Richard Johnson
    github: RichardJJG
  - name: Stuart Clements
    github: stuclem
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
  - cloudfoundry/docs-deploying-cf
  - cloudfoundry/docs-dotnet-core-tutorial
- name: Cloud Foundry Tutorials
  approvers:
  - name: Steve Greenberg
    github: spgreenberg
  - name: Anita Flegg
    github: anita-flegg
  reviewers:
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Maurice Brinkmann
    github: mauricebrinkmann
  - name: Andreas Koppenhöfer
    github: akop
  - name: Jovan Kostovski
    github: chombium
  - name: Arsalan Khan
    github: asalan316
  repositories:
  - cloudfoundry-tutorials/cf4devs
  - cloudfoundry-tutorials/korifi-ci
  - cloudfoundry-tutorials/korifi-sample-app
  - cloudfoundry-tutorials/tutorials
  - cloudfoundry-tutorials/what-is-cf
  - cloudfoundry-tutorials/sample-app
  - cloudfoundry-tutorials/edx
  - cloudfoundry-tutorials/unhappy-appy
  - cloudfoundry-tutorials/fake-mysql-broker
```
