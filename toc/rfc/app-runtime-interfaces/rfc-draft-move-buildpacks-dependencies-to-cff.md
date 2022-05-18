# Meta
[meta]: #meta
- Name: Move Buildpack Dependencies Repository to CFF
- Start Date: 2022-05-18
- Author(s): @gerg
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request:
  [https://github.com/cloudfoundry/community/pull/279](https://github.com/cloudfoundry/community/pull/279)


## Summary

Move ownership of the buildpack dependency repositories from VMware to the Cloud
Found Foundation (CFF).

## Problem

As part of staging, Cloud Foundry buildpacks download their dependencies from a
VMware-managed central dependency repository. For example, here is an excerpt
from staging an app using the ruby buildpack:
```
   -----> Ruby Buildpack version 1.8.53
   -----> Supplying Ruby
   -----> Installing bundler 2.3.11
   Download [https://buildpacks.cloudfoundry.org/dependencies/bundler/bundler_2.3.11_linux_noarch_any-stack_cab63d95.tgz]
   -----> Installing ruby 2.7.5
   Download [https://buildpacks.cloudfoundry.org/dependencies/ruby/ruby_2.7.5_linux_x64_cflinuxfs3_2c25fe7d.tgz]
   -----> Update rubygems from 3.1.6 to 3.3.11
   -----> Installing rubygems 3.3.11
   Download [https://buildpacks.cloudfoundry.org/dependencies/rubygems/rubygems_3.3.11_linux_noarch_any-stack_a9fa9578.tgz]
   -----> Installing dependencies using bundler 2.3.11
   Running: bundle install --jobs=4 --retry=4 --local
```

The `*.cloudfoundry.org` DNS Zone is managed by the CFF, so VMware is not able to
renew the TLS certificate for this dependency
repository. This issue came to a head on March 27 2022, when the
`buildpacks.cloudfoundry.org` TLS certificate expired, resulting in widespread
staging failures. Luckily, VMware had access to a `*.cloudfoundry.org` TLS
certificate, which does not expire until February 23 2023. Going forward, VMware
will need to coordinate certificate renewals with the CFF until this problem is
resolved, risking future outages.

In addition to `buildpacks.cloudfoundry.org`, the Java buildpack is also
dependent on a dependency repository, `java-buildpack.cloudfoundry.org`, with a
certificate expiring in May 2023. Both of these repositories are currently
implemented using AWS CloudFront distributions, backed by AWS S3 buckets. These
AWS resources are controlled by teams within VMware, and are not easily
accessible to Application Runtime Interfaces working group members, including
those who work for VMware.

Historically, we have not migrated the buildpack dependency repository because:
1. It it difficult to transfer large S3 buckets between AWS accounts
1. The storage and network traffic for the dependency repository is expensive,
   and VMware has agreed to pay for it


## Proposal

Move the buildpack dependency repository CloudFront distributions
(`buildpacks.cloudfoundry.org` and`java-buildpack.cloudfoundry.org`) to a
CFF-managed AWS account, but keep the existing S3 blobstore in a VMware-managed
AWS account for the time being.

**Pros:**
1. Reduces dependency on single vendor (VMware) for Cloud Foundry operation
1. Moves control of the buildpack dependency repositories into a CFF working group
1. Doesn't require significant redesign of existing systems
1. Less expensive for the CFF than migrating both CloudFront distributions and S3 buckets
1. Doesn't require migrating S3 buckets between AWS accounts

**Cons:**
1. Does not fully remove dependency on single vendor (VMware) for Cloud Foundry
   operation, since the S3 buckets will still be under VMware control
1. Does not address underlying centralization issue with buildpacks
1. May be too expensive for the CFF to maintain under current funding, depending
   on network traffic cost
1. Using CloudFront and S3 across two AWS accounts may result in some unforeseen
   issues
1. This migration will require some engineering and coordination effort between
   the CFF and teams within VMware to ensure a low/no downtime transfer.

