# Meta
[meta]: #meta
- Name: AWS European Sovereign Cloud Account for BOSH Stemcell Publishing
- Start Date: 2026-02-25
- Author(s): @I766702
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

This RFC proposes creating a new AWS account within AWS European Sovereign Cloud to publish BOSH stemcells to isolated European Sovereign Cloud regions, enabling Cloud Foundry deployments for government and highly regulated customers with data sovereignty requirements.


## Problem

AWS European Sovereign Cloud is physically and logically isolated from standard AWS regions. Standard AWS accounts cannot access or publish resources to European Sovereign Cloud regions, and resources cannot be replicated between them.

Without BOSH stemcells available in AWS European Sovereign Cloud regions, Cloud Foundry cannot be deployed in these environments, preventing adoption by government agencies and regulated industries with strict data residency and compliance requirements.


## Proposal

Create a new AWS account within the AWS European Sovereign Cloud partition to enable BOSH stemcell publishing to European Sovereign Cloud regions.

### Pipeline

The existing [stemcell build and publishing pipeline](https://github.com/cloudfoundry/bosh-stemcells-ci/blob/master/pipelines/publisher/pipeline.yml) must be extended to support AWS European Sovereign Cloud regions.
