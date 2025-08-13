# Meta
[meta]: #meta
- Name: Cloud Controller Blobstore Type: storage-cli
- Start Date: 2025-07-18
- Author(s): @johha, @stephanme
- Status: Accepted
- RFC Pull Request: [community#1253](https://github.com/cloudfoundry/community/pull/1253)


## Summary

Add a new blobstore type `storage-cli` to the Cloud controller that is based on the Bosh storage CLIs. Long-term, the `storage-cli` blobstore type shall replace the blobstore type `fog`.
The RFC also proposes to create a new "Storage CLI" area in the Foundational Infrastructure WG to allow cooperation of Bosh and CAPI teams and to consolidate the Bosh storage CLIs in one repository for easier code reuse.

## Problem

Cloud Controller uses the fog gem family to interface with the blobstores of different IaaS providers like Azure, AWS, GCP, and Alibaba Cloud.
These Ruby gems are largely unmaintained, introducing risks such as:
* Dependency on deprecated SDKs (e.g. Azure SDK for Ruby has reached EOL)
* Blocking Ruby version upgrades
* Potential for unpatched CVEs

## Proposal

Bosh faced similar issues, as it is also written in Ruby and interacts with blobstores. To address this, Bosh introduced standalone CLI tools which shell out from Ruby to handle all blobstore operations:
- https://github.com/cloudfoundry/bosh-azure-storage-cli
- https://github.com/cloudfoundry/bosh-s3cli
- https://github.com/cloudfoundry/bosh-gcscli
- https://github.com/cloudfoundry/bosh-ali-storage-cli
- https://github.com/cloudfoundry/bosh-davcli

These storage CLIs are implemented in Go and use the respective provider golang SDKs that are well supported for the foreseeable future.

Cloud Controller shall implement a new blobstore type `storage-cli` that uses the mentioned storage CLIs for blobstore operations. Missing functionality needed by the Cloud Controller shall be added to the storage CLIs in a compatible way:
- missing commands such as `copy`, `list`, `properties`, `ensure-bucket-exists`
- missing configuration parameters such as GCP Uniform Bucket Access and timeout parameters

It shall be possible to switch from blobstore type `fog` to type `storage-cli` in a productive Cloud Foundry installation. Once blobstore type `storage-cli` supports all four mentioned IaaS providers, the blobstore type `fog` can be removed from Cloud Controller.

### Storage CLI 

A new area "Storage CLI" shall be added to the Foundational Infrastructure WG in order to allow cooperation of Bosh and CAPI teams:

- create a new "Storage CLI" area
- add existing approvers of areas "VM deployment lifecycle (BOSH)" (FI) and "CAPI" (ARI) as initial approvers to this new area
- move the existing 4 bosh storage CLI repos from area "VM deployment lifecycle (BOSH)" into the new area 
- create a new repository `storage-cli` in this area with the goal to consolidate all existing bosh storage CLIs here
- setup CI, consolidate CLIs into the new `storage-cli` repo, implement missing commands and configuration parameters for each IaaS

### Bosh

- eventually switch from (old) bosh storage CLIs to consolidated `storage-cli` 
- finally archive the old bosh storage CLI repos

### Cloud Controller

- add a new blobstore type `storage-cli` that shells out to `storage-cli` for blobstore operations
- validate functionality with CATS
- benchmark blobstore operation performance and compare with blobstore type `fog`, enhance performance tests where necessary
- eventually deprecate and remove the blobstore type `fog` once all IaaS providers are covered

### cf-deployment

- add experimental ops files per IaaS provider for using the `storage-cli` blobstore type
- eventually promote those ops files and replace the existing fog-based blobstore ops files

## Additional Information

- [cloud_controller_ng #4443](https://github.com/cloudfoundry/cloud_controller_ng/pull/4443) - ADR: Use Bosh Storage CLIs for Blobstore Operations
