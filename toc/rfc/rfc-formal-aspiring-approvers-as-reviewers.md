# Meta
[meta]: #meta
- Name: Formally track aspiring approvers as reviewers
- Start Date: 2022-07-05
- Author(s): @rkoster, @stephanme
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/333


## Summary

Extend the working group yaml definitions to optionally include a `reviewers` key per area with a list of contributors who like to become approvers.
The github org automation should use this information to create a github team for the area with `-reviewers` suffix and __read__ permissions.

This will later allow automatic assignment of PRs to be reviewed, which will help these contributors more easily satisfy the requirements to become approvers. An additional use case might be granting read access to non-public CI pipelines.

## Problem

Due to the way to cloudfoundy github organization is setup, contributors gain no additional access rights within the organization. 
This prevents PRs to be assigned to them to be reviewed. 

In addition, the current process for getting people approver status relies a lot on the discipline of contributors to rack up the [needed contribution points](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0006-approver-requirements.md).
Ideally we create an opt-in low resistance path, to help contributors get to approver status quicker.
A lack of enough approvers hinders our ability as a community to review and approve PRs in a timely manner.
Improving the number of approvers should be the top priority of working group leads.

## Proposal

Allow tracking aspiring approvers as `reviewers` per working group area. Create a `*-reviewers` team per area that includes a `reviewers` key with read access to the area's repos.

This extends [RFC-005 Standardizing Github Teams and Access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0005-github-teams-and-access.md):

| Name of Team  | Team Membership  | Permissions  |
|---|---|---|
| wg-[WORKING-GROUP-NAME]-[AREA-NAME]-reviewers | Contributors who want to become approver for an area within a WG | Read access for all repos in the area, so that PRs can be assigned for review |

`reviewers` are not included in the overall working group team `wg-[WORKING-GROUP-NAME]`.

Where: 
* `WORKING-GROUP-NAME` is the name of the Working Group, converted to kebab case,
* `AREA-NAME` is the name of the area, also converted to kebab case, or a suitable short name that identifies it clearly and uniquely within the Working Group.
