# Service Management: Working Group Charter

## Mission

Provides interfaces for service lifecycle within application platforms and adapters to common external service providers.

## Goals

- Define the service extension API for Cloud Foundry brokered services.
- Provide a flexible adapter layer to common hyperscaler service providers.
- Maintain a set of reference volume service brokers and drivers for CF applications to mount stateful data.

## Scope
- Lead OSBAPI.
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
areas:
- name: Cloud Service Broker
  approvers:
  - name: George Blue
    github: blgm
  - name: Felisia Martini
    github: FelisiaM
  - name: James Norman
    github: jimbo459
  - name: Marcela Campo
    github: pivotal-marcela-campo
  - name: Jatin Naik
    github: tinygrasshopper
  repositories:
  - cloudfoundry-incubator/cloud-service-broker
  - cloudfoundry-incubator/csb-brokerpak-azure
  - cloudfoundry-incubator/csb-brokerpak-aws
  - cloudfoundry-incubator/csb-brokerpak-gcp
- name: OSBAPI
  approvers:
  - name: Sam Gunaratne
    github: Samze
  - name: Rodrigo Sampaio Vaz
    github: rsampaio
  repositories:
  - openservicebrokerapi/servicebroker
  - openservicebrokerapi/osb-checker
- name: ServiceFabrik
  approvers:
  - name: Anoop Joseph Babu
    github: anoopjb
  - name: Jintu Sebastian
    github: jintusebastian
  - name: Pooja
    github: Pooja-08
  - name: Swati
    github: swati1102
  - name: Visarg Soneji
    github: visargsoneji
  repositories:
  - cloudfoundry-incubator/service-fabrik-broker
  - cloudfoundry-incubator/service-fabrik-blueprint-app
  - cloudfoundry-incubator/service-fabrik-boshrelease
  - cloudfoundry-incubator/service-fabrik-backup-restore
  - cloudfoundry-incubator/service-fabrik-blueprint-service
  - cloudfoundry-incubator/service-fabrik-blueprint-boshrelease
  - cloudfoundry-incubator/service-fabrik-cli-plugin
  - cloudfoundry-incubator/service-fabrik-lvm-volume-driver
- name: Volume Service Adapters
  approvers:
  - name: Diego Lemos
    github: dlresende
  - name: fnaranjo
    github: fejnartal
  - name: Gareth Smith
    github: totherme
  repositories:
  - cloudfoundry/existingvolumebroker
  - cloudfoundry/goshims
  - cloudfoundry/mapfs
  - cloudfoundry/mapfs-release
  - cloudfoundry/migrate_mysql_to_credhub
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
```
