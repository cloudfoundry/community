# Meta
[meta]: #meta
- Name: Define Criteria and Process to Remove Inactive Cloud Foundry Github Members
- Start Date: 2023-10-25
- Author(s): @beyhan
- Status: Accepted
- RFC Pull Request: [community#707](https://github.com/cloudfoundry/community/pull/707)

## Summary

Define criteria for the Cloud Foundry Github organization which can be used to identify inactive members. Additionally, define a process how to remove the inactive members.

It is out of scope for this RFC to deal with users having roles in any working group. It is the responsibility of the working group leads to keep the approvers and reviewers up to date.

## Problem

Currently, there are no criteria to identify inactive members in the Cloud Foundry Github organization. Therefore we have many members in the Cloud Foundry organization, who are not actively contributing anymore and not part of any working group. This has many downsides for the foundation like:
* We don't know how many active members we have
* A potential change of the Github plan which costs depends on the number of Github organization members will generate higher costs
* Security risk because some of the inactive members could have access to resources belonging the Cloud Foundry Github organization

## Proposal

In this proposal the word "contributions" to the repositories of the Cloud Foundry Github organization includes following activities:
* Code contributions
* Creation, discussion or review of pull-requests
* Creation or discussion of issues

### Criteria for Inactive Members

The period to analyze should be the last 12 months and following criteria should be used to identify inactive users:
* The user is not listed in any working group as reviewer or approver
* There are no contributions to the Cloud Foundry Github organization repositories

### Remove the membership to the Cloud Foundry Github Organization

If the inactivity criteria are fulfilled for a member they should be removed from the Cloud Foundry Github organization. Any automation, approver or TOC member may submit a PR to remove the member from the Cloud Foundry Github organization. The person whose membership is being removed must be given two weeks to refute the removal. The working group lead to which the member belongs or TOC in case the member doesn't belong to any working group must make the final decision to remove the membership by merging the PR.

#### Implementation

This process should be fully automated until a pull-request for the removal is created. It should do following:
1. Find the Github users listed in [contributors.yml](https://github.com/cloudfoundry/community/blob/main/org/contributors.yml) without any working group role
2. Find the inactive Github users from 1). We will implement this by ourself or use tools like [inactive-users-action](https://github.com/peter-murray/inactive-users-action/tree/main).
3. Create a pull-request to remove the user from the Cloud Foundry Github organization

#### Initial cleanup
As described in the problem section of this RFC there are many inactive members in the Cloud Foundry Github organization. Therefore, for the initial cleanup we should have an exception to create a bulk PR with all inactive members. Having PRs for every user will be very high effort because there are several hundreds of inactive users currently.

