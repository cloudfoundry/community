# Meta
[meta]: #meta
- Name: Define Criteria for Inactive Github Members
- Start Date: 2023-10-25
- Author(s): @beyhan
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Define criteria for the Cloud Foundry Github organization which can be used to identify inactive members.

## Problem

Currently, there are no criteria to identify inactive members in the Cloud Foundry Github organization. Therefore we have many members in the Cloud Foundry organization, who are not actively contributing anymore. This has many downsides for the foundation like:
* We don't know how many active members we have
* A potential change of the Github plan which costs depends on the number of Github organization members will generate higher costs
* Security risk because some of the inactive members could have access to resources belonging the Cloud Foundry Github organization


## Proposal

Following criteria should be use to identify inactive users:
* No contributions to the Cloud Foundry Github organization repositories for a period of 12 months
* No participations in any working group activities

If the criteria for inactivity are fulfilled for a member they should be removed from the Cloud Foundry Github organization. Any automation, approver or TOC member may submit a PR to remove the member from the Cloud Foundry Github organization. The person whose membership is being removed must be given two weeks to refute the revocation. The working group lead to which the member belongs or TOC in case the member doesn't belong to any working group must make the final decision to revoke the role by merging the PR.
