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

### Cloud Service Broker

### Volume Service Adapters

### ServiceFabrik


## Technical Assets by Area

Components from the Cloud Service Broker, Open Service Broker API, Service Fabrik, and Volume Services projects.

### OSBAPI
* [OSBAPI spec](https://github.com/openservicebrokerapi/servicebroker)

### Cloud Service Broker

* [cloud-service-broker](https://github.com/cloudfoundry-incubator/cloud-service-broker)
* [csb-azure-brokerpak](https://github.com/cloudfoundry-incubator/csb-brokerpak-azure)
* [csb-aws-brokerpak](https://github.com/cloudfoundry-incubator/csb-brokerpak-aws)
* [csb-gcp-brokerpak](https://github.com/cloudfoundry-incubator/csb-brokerpak-gcp)

### Volume Service Adapters

* [nfsv3driver](https://github.com/cloudfoundry/nfsv3driver)
* [nfsbroker](https://github.com/cloudfoundry/nfsbroker)
* [nfsboshrelease](https://github.com/cloudfoundry/nfs-volume-release)
* [smbdriver](https://github.com/cloudfoundry/smbdriver)
* [smbbroker](https://github.com/cloudfoundry/smbbroker)
* [smbboshrelease](https://github.com/cloudfoundry/smb-volume-release)

### ServiceFabrik

* [serviceFabrikBroker](https://github.com/cloudfoundry-incubator/service-fabrik-broker)
* [service-fabrik-blueprint-app](https://github.com/cloudfoundry-incubator/service-fabrik-blueprint-app)