# Meta
[meta]: #meta
- Name: CF and BOSH should default to more efficient and smaller performance VM sizes
- Start Date: 2022-05-30
- Author(s): @dsboulder
- Status: Draft
- RFC Pull Request: [#290](https://github.com/cloudfoundry/community/pull/290)


## Summary

The vast majority of CF and BOSH deployments are deployed automatically in CF
testing pipelines (or in proprietary vendor pipelines), so we should optimize
the default VM sizes for these workloads. We will choose VM sizes that are
either cheaper because they are newer generation, they provide a smaller/finer
tuned amount of hardware, or they have burstable cores for appropriate
workloads.

**Note: This is a breaking change, especially for [Reserved
Instance](https://aws.amazon.com/ec2/pricing/reserved-instances/) holders.
Anyone using the default VM sizes for a high-performance or production CF should
consider customizing their VM sizes. In addition, the Diego cells have been
reduced from 26-64GB of memory to a consistent 16GB by default, so please
consider how many you need or resize them up.**.

We believe it is acceptable to make this type of change because we expect
production deployments of CF to customize their VM types anyway, and we cannot
prevent progress just to help RI buyers.

## Problem

We'd like to save the CFF, and anyone who deploys default CF configuration,
significant money in operating BOSH and CF deployment. The current deployment
costs for CF-d are so expensive (for example on AWS) that our limited foundation
CI budget will be consumed too quickly. In addition, our VM type usages are in
need of a refresh to match the newest IaaS offerings for both performance and
cost.

## Proposal

### Important decisions:
* VMs are allowed to be burstable, in minimal use cases.
* Diego cells should be smaller and consistent at 16GB of RAM, rather then the
  old 30-50GB ranges.
* Modern (as of 2021) instance types should be used.

### VM Size definitions
We'd like to further clarify the meaning of the default VM sizes for CF-D,
BOSH-D, and Jumpbox-D as follows:

| Deployment Used | VM Size Name | Definition |
| --- | --- | --- |
| bosh | bosh | A VM that MUST have at least 4 GB of memory and 1 CPU. The CPU MAY be burstable, since the director is often idle. Since UAA and/or Credhub are common add-ons that add significant memory, an ops-file with 8GB RAM and more CPU MAY be provided. |
| jumpbox | jumpbox | A minimal VM with at least 1GB of memory and 1 CPU; It SHOULD be burstable. |
| cf | minimal | A minimal VM that SHOULD have 2GB+ of memory and 1+ CPU; It SHOULD be burstable. |
| cf | small | A default VM size for larger processes that SHOULD have 4GB of memory with 1 or 2 CPUs. It MAY be burstable if the VM can sustain baseline usage of at least 75% usage on a vCPU. |
| cf | small-highmem | A default app running VM size that SHOULD have 16GB+ of memory and 2 CPUs. It MAY be burstable since app workloads can be burstable. These SHOULD have a higher memory-to-CPU ratio to optimize cost and fit more applications per Diego Cell. |
| bosh | compilation | A high-compute, short-running VM pool that SHOULD have 2+ CPUs with at least 4GB of RAM and SHOULD NOT be burstable. This pool runs typically for 5-20 minutes, so it SHOULD be 5 nodes for per-minute or per-second billing or 3 nodes for hourly billing. |

### Amazon Web Services VM Mapping
Switch all storage from `gp2` to `gp3` for a **20% cost savings** on disks. The
T3 series defaults to unlimited burst, allowing you to borrow burst credits from
later in the day and eventually pay for extra burst if there's a deficit.

| VM Size Name | Old Size | New Size | Cost Savings | Notes |
| --- | --- | --- | --- | --- |
| bosh | `m5.large` | `t3.medium` | **57% cheaper** ($0.096 vs $0.0416) | Baseline CPU allocation is 40% of 1 core. Unlimited mode allows credit borrowing. |
| jumpbox | `t2.micro` | `t3.micro` | **10% cheaper** ($0.0116 vs $0.0104) | T2 instances are now very old and sometimes fail to allocate. |
| minimal | `m4.large` | `t3.small` | **79% cheaper** ($0.1000 vs $0.0208) | Baseline CPU allocation is 40% of 1 core. |
| small | `m4.large` | `t3.medium` | **58% cheaper** ($0.1000 vs $0.0416)  | Downsize from 8GB => 4GB. Unlimited mode allows lots of extra burst. |
| small-highmem | `r4.xlarge` | `r5a.large` | **58% cheaper** ($0.2660 vs $0.1130) | Use 16GB instead of 32GB VM size to meet spec. |
| compilation | *5x* `c4.large` | *5x* `c5a.large` | **23% cheaper** ($0.5000 vs $0.385) | Keep 5 instances (billed per-second). |

A default BBL + CF-D installation would now cost $791/mo instead of $2668/mo, for
a savings of 70%!

### Azure VM Mapping
_Note: VM sizes on Azure should now all allow Premium Storage (the `s`
suffixes)._

| VM Size Name | Old Size | New Size | Cost Savings | Notes |
| --- | --- | --- | --- | --- |
| bosh | `Standard_D1_v2` | `Standard_B2s` | **28% cheaper** ($0.0570 vs $0.0416) | Adds bursting, and stops using very old Dv2 series. |
| jumpbox | `Standard_D1_v2` | `Standard_B1s` | **82% cheaper** ($0.0570 vs $0.0104) |  |
| minimal | `Standard_F1s` | `Standard_B1ms` | **58% cheaper** ($0.0497 vs $0.0207) | Adds bursting, and stops using very old Fv1 series. |
| small | `Standard_F2s_v2` | `Standard_F2s_v2` | **same**  | Fv2 is modern and meets the spec already. The B2 baseline is too low (only 40%). |
| small-highmem | `Standard_GS2` | `Standard_E2s_v3` | **87% cheaper** ($0.9810 vs $0.1260) | Switch from the very old mega G-series with 56GB of memory to modern E-series with only 16GB of memory. |
| compilation | *5x* `Standard_DS1_v2` | *5x* `Standard_F2s_v2` | **32% more expensive** ($0.285 vs $0.422) | VMs should have 2 CPUs to bring them into spec, but they are expected to run for shorter times (billed per-minute). |

A default BBL + CF-D installation would now cost $1005/mo instead of $3355/mo, for
a savings of 70%!

### Google Compute Cloud VM Mapping
Switch all storage from `pd-ssd` to `pd-balanced` for a **41% cost savings** on
disks.

| VM Size Name | Old Size | New Size | Cost Savings | Notes |
| --- | --- | --- | --- | --- |
| bosh | `n1-standard-1` | `e2-medium` | **29% cheaper** ($0.04749975 vs $0.033503) | Burstable E-series equivalent. Baseline CPU allocation allows constant 100% of 1 core. |
| jumpbox | `n1-standard-1` | `e2-micro` | **82% cheaper** ($0.04749975 vs $0.008376) | |
| minimal | `n1-standard-1` | `e2-small` | **65% cheaper** ($0.04749975 vs $0.016751) | Baseline CPU allocation is 50% of 1 core. |
| small | `n1-standard-2` | `e2-medium` | **65% cheaper** ($0.0949995 vs $0.033503)  | Downsize from 8GB => 4GB. Baseline CPU allocation high enough. |
| small-highmem | `n1-highmem-4` | `e2-highmem-2` | **62% cheaper** ($0.236606 vs $0.09039) | Switch from 26GB RAM to 16GB RAM. |
| compilation | *5x* `n1-highcpu-8` | *5x* `e2-highcpu-4` | **65% cheaper** ($1.416972 vs $0.49468) | 4 CPUs is plenty. Keep 5 instances (billed per-second). |

A default BBL + CF-D installation would now cost $635/mo instead of $1742/mo, for
a savings of 64%!

### Optimizing Concourse Deployments

Default Concourse instances deployed by BOSH use only the `default` VM type for
both ATC and workers. This VM type is likely in use for a variety of activities,
and is loosely defined as 1-2 non-bustable CPUs with 4-8GB of RAM. These VM
types are probably a poor match for Concourse workers, especially the 4GB
variants, and we expect that most Concourse deployments optimize this
configuration to find the best worker types. No significant cost savings exist
for this VM type since most IaaS no longer offer a 4GB VM without also including
a burstable CPU.
