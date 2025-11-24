# Service Management: Working Group Charter

## Mission

Provides interfaces for service lifecycle within application platforms and adapters to common external service providers.

## Goals

- Define the service extension API for Cloud Foundry brokered services.
- Provide a flexible adapter layer to common hyperscaler service providers.

## Scope
- Lead OSB API.
- Develop and maintain Cloud Service Brokers for AWS, Azure, and GCP.
- Develop and maintain ServiceFabrik, a generic BOSH-based and Docker-container-based service instance manager.

## Non-Goals

## Roles & Technical Assets
Components from the Cloud Service Broker, Open Service Broker API and Service Fabrik.

```yaml
name: Service Management
execution_leads:
- name: Marcela Campo
  github: pivotal-marcela-campo
technical_leads:
- name: Marcela Campo
  github: pivotal-marcela-campo
bots:
- name: cf-gitbot
  github: cf-gitbot
areas:
- name: Cloud Service Broker
  approvers:
  - name: George Blue
    github: blgm
  - name: Felisia Martini
    github: FelisiaM
  - name: Marcela Campo
    github: pivotal-marcela-campo
  - name: Georgi Dim. Dimitrov
    github: georgidimdimitrov
  - name: Bogomil Kuzmanov
    github: bogomil-kuzmanov
  bots:
  - name: Services Enablement bot
    github: servicesenablement
  repositories:
  - cloudfoundry/cloud-service-broker
  - cloudfoundry/csb-brokerpak-azure
  - cloudfoundry/csb-brokerpak-aws
  - cloudfoundry/csb-brokerpak-gcp
  - cloudfoundry/jdbctestapp
  - cloudfoundry/upgrade-all-services-cli-plugin
  - cloudfoundry/terraform-provider-csbpg
  - cloudfoundry/terraform-provider-csbmysql
  - cloudfoundry/terraform-provider-csbsqlserver
  - cloudfoundry/brokerapi
config:
  github_project_sync:
    mapping:
      cloudfoundry: 27
```
