# Meta
[meta]: #meta
- Name: Shared Concourse Instance
- Start Date: 2025-07-07
- Author(s): @drich10
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1238

## Summary

Provide a shared Concourse instance for CI/CD workloads within the CFF.

## Problem

Currently, _most_ teams using Concourse are deploying and managing their own instance. This creates overhead in both engineering time and cloud costs.

## Proposal

The Concourse WG MUST host a shared Concourse for working groups to leverage for CI/CD. This MUST reduce both engineering and cloud expenses. Consolidating Concourse spend into a singular account MAY make it easier to manage the spend and usage. Additionally centralizing management of CI maintenance, MAY remove load on members/leads of working groups managing their own instance(s). Working groups MAY use this instance if they choose to.

### Access
Concourse can use Github teams to manage access control within pipelines and credential systems. As such, working group areas and membership MUST determine roles within the system:
* New role in the Concourse WG to administrate.
* WG execution leads that are onboarded are given adminstration permissions.
* WGs must identify area(s) to give access to.

### Credential Management
Credential access and management MUST be segmented so that WGs cannot access one another's secrets.
  * Vault MAY be the secret manager to allow consistent management and separation of secrets between teams on the shared instance.
  * We believe most teams currently use Credhub which does not easily allow us to implement the separation that MUST exist between teams.

### Cost Reduction
* Removes the overhead from additional Web and DB instances that come from running multiple instances of Concourse.
* Enables sharing of lesser used worker types such like Windows Workers. Reducing the number of these workers that MUST exist.

### Expectations and Agreements
* Concourse WG leads will be primarily responsible for system availability during the business hours for each individual.
* Concourse WG leads will be responsible for system upgrades.
* WGs onboarded to the shared instance MUST be given sufficient access to operate the system. This includes, but is not limited to:
  * IaaS access
  * Runbooks and tooling for Concourse deployment
* Support Issues MUST be shared between the Concourse working group maintainers and the concourse supporters

### Timeline
#### Phase 1
* Concourse team creates the new, shared, instance and migrates itself (4-6 weeks from acceptance of this proposal)

#### Phase 2
* Onboard 1 working group to the new instance and refine deployment and operational strategies from initial learnings (4-6 weeks).
* Shut down the concourse owned by the working group.

#### Phase 3
* Open onboarding to the rest of the working groups and migrate their pipelines. Shut down the concourse owned by the working group(s).
* Success criteria:
  * 2 or more teams leveraging this instance.
  * Each team onboarding MUST either reduce or maintain the current level of infrastructure costs.
