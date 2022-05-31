# Meta
[meta]: #meta
- Name: CF and BOSH should default to more efficient and smaller performance VM sizes
- Start Date: 2022-05-30
- Author(s): @dsboulder
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

The vast majority of CF and BOSH deployments are doing automatically in CF testing pipelines (or in proprietary vendor pipelines), 
so we should optimize the default VM sizes for these workloads. We will choose VM sizes that are either cheaper because they newer generation, 
they provide a smaller/finer tuned amount of hardware, or they have burstable cores. This is a breaking change, especially for Reserved Instance holder 
who may not want VM size changes at all, but it is acceptable because we expect production deployments of CF to customize their VM types anyway.

## Problem

We'd like to save the CFF, and anyone who deploys default CF configuration, significant money in operating BOSH and CF deployment. 
The current deployment costs for CF-d are so expensive (for example on AWS) that our limited foundation CI budget will be consumed too quickly. 
In addition our VM type usages are in need of a  refresh to match the newest IaaS offerings for both performance and cost.

## Proposal

### VM Size definitions
We'd like to further clarify the meaning of the default VM sizes for CF-D, BOSH-D, and Jumpbox-D as follows:

| Deployment Used | VM Size Name | Definition |
| --- | --- | --- |
| bosh | bosh | A VM that MUST have at least 4 GB of memory and 1 CPU. The CPU MAY be burstable, since the director is often idle. Since UAA and/or credhub are common OpsFiles that add significant memory, the VM MAY default to 8GB of memory when cost effective |
| jumpbox | jumpbox | A minimal VM with at least 1GB of memory and 1 CPU, SHOULD be burstable |
| cf | minimal | A minimal VM that SHOULD have 1GB-2GB of memory and 1 CPU, SHOULD be burstable |
| cf | small | A default VM size for larger processes with 4GB-8GB of memory and 1-2 CPU, SHOULD NOT be burstable |
| cf | small-highmem | A default app running VM size that SHOULD have 16GB+ of memory and 2 CPUs, MAY be burstable since app workloads can be burstable |

### Azure VM Mapping
Note: VM sizes on Azure should now all allow Premium Storage (the `s` suffixes).

| VM Size Name | Old Size | New Size | Cost Savings | Notes |
| --- | --- | --- | --- |
| bosh | `Standard_D1_v2` | `Standard_B2s` | **28% cheaper** ($0.0570 vs $0.0416) | Adds bursting, stop using very old Dv2 series |
| jumpbox | `Standard_D1_v2` | `Standard_B1s` | **82% cheaper** ($0.0570 vs $0.0104) |  |
| minimal | `Standard_F1s` | `Standard_B1ms` | **58% cheaper** ($0.0497 vs $0.0207) | Adds bursting, stop using very old Fv1 series |
| small | `Standard_F2s_v2` | `Standard_F2s_v2` | **same**  | Fv2 is modern and meets the spec already |
| small-highmem | `Standard_GS2` | `Standard_E4s_v3` | **87% cheaper** ($0.9810 vs $0.1260) | Adds bursting, stop using very old Fv1 series |
