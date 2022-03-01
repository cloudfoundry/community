# Meta
[meta]: #meta
- Name: Who is able to add and remove members of the Cloudfoundry GitHub org
- Start Date: 2022-01-26
- Author(s): @LeePorte
- Status: Accepted
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/194


## Summary

Working group leads and approvers are the primary roles responsible for granting GitHub users membership in the `cloudfoundry` GitHub org, as they have the most context on which users within the CF community meet the criteria to be regular contributors. 

The TOC is the body responsible for removing an existing member from the `cloudfoundry` GitHub org and coordinating with working groups to ensure that the removal does not have unexpected consequences.

## Problem

Under the previous dojo-based participation model, a central team of VMware admins was primarily responsible for managing the members of the `cloudfoundry` GitHub org. In the current system of CF community roles and responsibilities, however, that delegation to the administrative team of a single member company no longer makes sense.

## Proposal

As defined in the [roles](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md), each Contributor
should be a member of the `cloudfoundry` GitHub org.
The leads and approvers within a Working Group are best positioned to decide whether an individual has met the minimum contribution criteria to become an official contributor.

A Working Group approver or lead should raise a [PR on the community repository](https://github.com/cloudfoundry/community/pulls) to propose adding a new member to the `cloudfoundry` GitHub org.
This PR should add the member directly to the [YAML file describing the organization membership](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml), as automation will synchronize the GitHub org membership with the contents of this file periodically. 
Only Working Group leads and the TOC will actually have permission to merge these PRs under the planned access control on the community repository.

As removing a member from the `cloudfoundry` GitHub org may have unintended consequences across the organization, the TOC is the body required to approve those removals.
Proposals to remove a member should also be submitted via PR, and the submitter should tag the PR with `toc` and should mention `@cloudfoundry/toc` to make the TOC aware of the request.
The TOC will then consult any working groups that may be affected by the removal of this member and use its usual decision process to approve or reject the removal. 

