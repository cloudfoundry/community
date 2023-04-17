# Service Management: Working Group Charter

## Mission

Provides interfaces for service lifecycle within application platforms and adapters to common external service providers.

## Goals

- Define the service extension API for Cloud Foundry brokered services.
- Provide a flexible adapter layer to common hyperscaler service providers.
- Maintain a set of reference volume service brokers and drivers for CF applications to mount stateful data.

## Scope
- Lead OSB API.
- Develop and maintain Cloud Service Brokers for AWS, Azure, and GCP.
- Maintain volume service adapters for NFS and SMB.
- Develop and maintain ServiceFabrik, a generic BOSH-based and Docker-container-based service instance manager.

## Non-Goals

## Roles & Technical Assets
Components from the Cloud Service Broker, Open Service Broker API, Service Fabrik, and Volume Services projects.

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
  - name: Andrea Zucchini
    github: zucchinidev
  - name: Konstantin Semenov
    github: jhvhs    
  - name: Fernando Naranjo
    github: fnaranjo-vmw        
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
- name: OSB API
  approvers:
  - name: Rodrigo Sampaio Vaz
    github: rsampaio
  repositories:
  - openservicebrokerapi/servicebroker
  - openservicebrokerapi/osb-checker
- name: Service Fabrik
  approvers:
  - name: Abhik Gupta
    github: abh1kg
  - name: Anoop Joseph Babu
    github: anoopjb
  - name: Jintu Sebastian
    github: jintusebastian
  - name: Pooja
    github: Pooja-08
  - name: Swati
    github: swati1102
  - name: Vinayendraswamy Brahmandabheri
    github: vinaybheri    
  - name: Visarg Soneji
    github: visargsoneji
  repositories:
  - cloudfoundry/service-fabrik-broker
  - cloudfoundry/service-fabrik-blueprint-app
  - cloudfoundry/service-fabrik-boshrelease
  - cloudfoundry/service-fabrik-backup-restore
  - cloudfoundry/service-fabrik-blueprint-service
  - cloudfoundry/service-fabrik-blueprint-boshrelease
  - cloudfoundry/service-fabrik-cli-plugin
  - cloudfoundry/service-fabrik-lvm-volume-driver
- name: Volume Services
  approvers:
  - name: Diego Lemos
    github: dlresende
  - name: Fernando Naranjo
    github: fejnartal
  - name: Gareth Smith
    github: totherme
  - name: George Blue
    github: blgm
  - name: Iain Findlay
    github: ifindlay-cci
  - name: Konstantin Kiess
    github: nouseforaname
  - name: Gary Liu
    github: syslxg
  bots:
  - name: Cryogenics CI Bot
    github: Cryogenics-CI
  repositories:
  - cloudfoundry/existingvolumebroker
  - cloudfoundry/goshims
  - cloudfoundry/mapfs
  - cloudfoundry/mapfs-release
  - cloudfoundry/nfsv3driver
  - cloudfoundry/nfsbroker
  - cloudfoundry/nfs-volume-release
  - cloudfoundry/persi-ci
  - cloudfoundry/service-broker-store
  - cloudfoundry/smbdriver
  - cloudfoundry/smbbroker
  - cloudfoundry/smb-volume-release
  - cloudfoundry/volume-mount-options
  - cloudfoundry/volumedriver
config:
  github_project_sync:
    mapping:
      cloudfoundry: 27
      openservicebrokerapi: 1
      cloudfoundry-incubator: 3
```
