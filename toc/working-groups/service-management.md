# Service Management: Working Group Charter

## Mission

Provides interfaces for service lifecycle within application platforms and adapters to common external service providers.

## Goals

- Define the service extension API for cloud foundry brokered services
- Provide a flexible adapater layer to common hyperscaler service providers
- Mantain a set of reference volume service brokers and drivers for CF applications to mount stateful data

## Scope
- Lead OSBAPI
- Develop and maintain Cloud Service Brokers for AWS, Azure, and GCP
- Maintain volume service adapters for NFS and SMB.
- Develop and maintain ServiceFabrik, a generic BOSH-based and Docker-container-based service instance manager

## Non-Goals




## Proposed Membership

- Technical Lead(s): Marcela Campo
- Execution Lead(s): Marcela Campo

## Approvers by Area
### OSBAPI
* @Samse
* @rsampaio

### Cloud Service Broker
* @blgm
* @FelisiaM
* @pivotal-marcela-campo 


### Volume Service Adapters

### ServiceFabrik


## Technical Assets by Area

Components from the Cloud Service Broker, Open Service Broker API, Service Fabrik, and Volume Services projects.

### OSBAPI
* [OSBAPI spec](https://github.com/openservicebrokerapi/servicebroker)
* [osb-checker](https://github.com/openservicebrokerapi/osb-checker)

### Cloud Service Broker

* [cloud-service-broker](https://github.com/cloudfoundry-incubator/cloud-service-broker)
* [csb-brokerpak-azure](https://github.com/cloudfoundry-incubator/csb-brokerpak-azure)
* [csb-brokerpak-aws](https://github.com/cloudfoundry-incubator/csb-brokerpak-aws)
* [csb-brokerpak-gcp](https://github.com/cloudfoundry-incubator/csb-brokerpak-gcp)

### Volume Service Adapters

* [nfsv3driver](https://github.com/cloudfoundry/nfsv3driver)
* [nfsbroker](https://github.com/cloudfoundry/nfsbroker)
* [nfs-volume-release](https://github.com/cloudfoundry/nfs-volume-release)
* [smbdriver](https://github.com/cloudfoundry/smbdriver)
* [smbbroker](https://github.com/cloudfoundry/smbbroker)
* [smb-volume-release](https://github.com/cloudfoundry/smb-volume-release)

### ServiceFabrik

* [service-fabrik-broker](https://github.com/cloudfoundry-incubator/service-fabrik-broker)
* [service-fabrik-blueprint-app](https://github.com/cloudfoundry-incubator/service-fabrik-blueprint-app)