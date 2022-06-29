# Meta
[meta]: #meta
- Name: Stemcell Release Schedule
- Start Date: 2022-06-29
- Author(s): @thomasthal
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/...


## Summary
This RFC proposes a well defined release schedule for the CF Stemcell to ensure the availability of OS related security patches in a timely manner.

## Problem
Almost daily, Canonical releases security patches of known vulnerabilities.  As a PaaS offering provider, you want to consume those patches as fast as possible to mitigate vulnerabilities and keep your customers safe. Cloud Foundry has the huge security advantage to be able to rollout zero downtime updates and patch security vulnerabilities at any time. This potential is limited by the fact, that often there is only an "outdated" stemcell available, which does not yet contain latest patches. 

A second concern is that the current stemcell release strategy seems to be an undocumented, informal agreement. This makes it impossible to evaluate if the process to create a new stemcell is executed accordingly. Moreover, it is difficult to provide clear  statements to customers how long the rollout of an OS patch takes or to judge if compliance requirements are met.

## Proposal
- Release a new stemcell every week on Tuesday, that contains all available ubuntu security patches 
- Release a new stemcell for every critical security vulnerability as soon as possible

**Reason**:
From a security perspective patches should be rolled out as fast as possible. On the other hand, each stemcell release triggers many build piplines, which can not be used to validate remaining changes at the same time. This proposal tries to balance these two concerns by utilizing the pipelines only once per week and by garanteeing that independent of the vulnerability after 7 days a stemcell, that includes the patch from Ubuntu, is available. The weekday Tuesday is proposed as it is not directly after weekend, but there are still a few days left to consume the stemcell before the next weekend arrives. 

In rare cases, there are vulnerabilities that are so servere that rolling out a patch as soon as possible is required. This proposal considers all vulnerabilities with CVSS Score 9.0 (or higher) and all vulnerabilities that can lead to a diego container breakout as critical. 

