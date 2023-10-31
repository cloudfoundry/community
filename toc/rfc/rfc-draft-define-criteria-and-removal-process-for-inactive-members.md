# Meta
[meta]: #meta
- Name: Define Criteria and Process to Remove Inactive Cloud Foundry Github Members
- Start Date: 2023-10-25
- Author(s): @beyhan
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Define criteria for the Cloud Foundry Github organization which can be used to identify inactive members. Additionally, define a process how to remove the inactive members.

## Problem

Currently, there are no criteria to identify inactive members in the Cloud Foundry Github organization. Therefore we have many members in the Cloud Foundry organization, who are not actively contributing anymore. This has many downsides for the foundation like:
* We don't know how many active members we have
* A potential change of the Github plan which costs depends on the number of Github organization members will generate higher costs
* Security risk because some of the inactive members could have access to resources belonging the Cloud Foundry Github organization


## Proposal

### Criteria for Inactive Members

The period to analyze should be the last 12 months and following criteria should be use to identify inactive users:
* No contributions to the Cloud Foundry Github organization repositories
* No participations in working group activities

### Remove the membership to the Cloud Foundry Github Organization

If the inactivity criteria are fulfilled for a member they should be removed from the Cloud Foundry Github organization. Any automation, approver or TOC member may submit a PR to remove the member from the Cloud Foundry Github organization. The person whose membership is being removed must be given two weeks to refute the removal. The working group lead to which the member belongs or TOC in case the member doesn't belong to any working group must make the final decision to remove the membership by merging the PR.

#### Initial cleanup
As described in the problem section of this RFC there are many inactive members in the Cloud Foundry Github organization. Therefore, for the initial cleanup we should have an exception to create a bulk PR with all inactive members. Having PRs for every user will be very high effort because there are several hundreds of inactive users currently.