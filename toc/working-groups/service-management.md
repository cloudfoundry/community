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




## Proposed Membership

- Technical Lead(s): Marcela Campo (@pivotal-marcela-campo)
- Execution Lead(s): Marcela Campo (@pivotal-marcela-campo)

## Approvers by Area
### Cloud Service Broker
* [@blgm](https://github.com/blgm)
* [@FelisiaM](https://github.com/FelisiaM)
* [@jimbo459](https://github.com/jimbo459)
* [@pivotal-marcela-campo](https://github.com/pivotal-marcela-campo) 
* [@tinygrasshopper](https://github.com/tinygrasshopper)


### OSBAPI
* [@Samze](https://github.com/Samze)
* [@rsampaio](https://github.com/rsampaio)

### ServiceFabrik
* [@anoopjb](https://github.com/anoopjb)
* [@jintusebastian](https://github.com/jintusebastian)
* [@Pooja-08](https://github.com/Pooja-08) 
* [@swati1102](https://github.com/swati1102)
* [@visargsoneji](https://github.com/visargsoneji)

### Volume Service Adapters
* [@dlresende](https://github.com/dlresende)
* [@fejnartal](https://github.com/fejnartal)
* [@totherme](https://github.com/totherme)


## Technical Assets by Area

Components from the Cloud Service Broker, Open Service Broker API, Service Fabrik, and Volume Services projects.

### Cloud Service Broker

* [cloud-service-broker](https://github.com/cloudfoundry-incubator/cloud-service-broker)
* [csb-brokerpak-azure](https://github.com/cloudfoundry-incubator/csb-brokerpak-azure)
* [csb-brokerpak-aws](https://github.com/cloudfoundry-incubator/csb-brokerpak-aws)
* [csb-brokerpak-gcp](https://github.com/cloudfoundry-incubator/csb-brokerpak-gcp)


### OSBAPI

* [OSBAPI spec](https://github.com/openservicebrokerapi/servicebroker)
* [osb-checker](https://github.com/openservicebrokerapi/osb-checker)

### ServiceFabrik

* [service-fabrik-broker](https://github.com/cloudfoundry-incubator/service-fabrik-broker)
* [service-fabrik-blueprint-app](https://github.com/cloudfoundry-incubator/service-fabrik-blueprint-app)
* [service-fabrik-boshrelease](https://github.com/cloudfoundry-incubator/service-fabrik-boshrelease)
* [service-fabrik-backup-restore](https://github.com/cloudfoundry-incubator/service-fabrik-backup-restore)
* [service-fabrik-blueprint-service](https://github.com/cloudfoundry-incubator/service-fabrik-blueprint-service)
* [service-fabrik-blueprint-boshrelease](https://github.com/cloudfoundry-incubator/service-fabrik-blueprint-boshrelease)
* [service-fabrik-cli-plugin](https://github.com/cloudfoundry-incubator/service-fabrik-cli-plugin)
* [service-fabrik-lvm-volume-driver](https://github.com/cloudfoundry-incubator/service-fabrik-lvm-volume-driver)

### Volume Service Adapters

* [existing-volume-broker](https://github.com/cloudfoundry/existingvolumebroker)
* [goshims](https://github.com/cloudfoundry/goshims)
* [mapfs](https://github.com/cloudfoundry/mapfs)
* [mapfs-release](https://github.com/cloudfoundry/mapfs-release)
* [migrate-mysql-to-credhub](https://github.com/cloudfoundry/migrate_mysql_to_credhub)
* [nfsv3driver](https://github.com/cloudfoundry/nfsv3driver)
* [nfsbroker](https://github.com/cloudfoundry/nfsbroker)
* [nfs-volume-release](https://github.com/cloudfoundry/nfs-volume-release)
* [perci-ci](https://github.com/cloudfoundry/persi-ci)
* [service-broker-store](https://github.com/cloudfoundry/service-broker-store)
* [smbdriver](https://github.com/cloudfoundry/smbdriver)
* [smbbroker](https://github.com/cloudfoundry/smbbroker)
* [smb-volume-release](https://github.com/cloudfoundry/smb-volume-release)
* [volume-mount-options](https://github.com/cloudfoundry/volume-mount-options)
* [volume-driver](https://github.com/cloudfoundry/volumedriver)
