# Meta
[meta]: #meta
- Name: Who is able to add and remove members of CFF Github Orgs
- Start Date: 2022-01-26
- Author(s): @LeePorte
- Status: Accepted
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/194


## Summary

Working group leads and approvers are the primary roles responsible for
granting GitHub users membership to the CFF Github Orgs, as they have
the most context on which users within the community meet the criteria to be
regular contributors. 

The TOC is the body responsible for removing an existing member from the CFF
Github Orgs and coordinating with working groups to ensure that the removal
does not have unexpected consequences.

## Problem

Under the previous dojo-based participation model, a central team of VMware
admins was primarily responsible for managing the members of the CFF Github
Orgs . In the current system of CF community roles and responsibilities,
however, that delegation to the administrative team of a single member company
no longer makes sense.

## Proposal

As defined in the
[roles](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md), each
Contributor should be a member of the appropriate CFF Github Org(s). The leads
and approvers within a Working Group are best positioned to decide whether an
individual has met the minimum contribution criteria to become an official
contributor.

A Working Group approver or lead should raise a [PR on the community
repository](https://github.com/cloudfoundry/community/pulls) to propose adding
a new member to a CFF Github Org. This PR should add the member directly to the
file in the [organizational structure
directory](https://github.com/cloudfoundry/community/tree/main/org) that
contains the list of contributors. Automation will periodically synchronize the
GitHub org membership with the files in this directory. Only Working Group
leads and the TOC will actually have permission to merge these PRs under the
planned access control on the community repository.

As removing a member from a CFF GitHub Org may have unintended consequences
across the organization, the TOC is the body required to approve those
removals. Proposals to remove a member should also be submitted via PR, and the
submitter should tag the PR with `toc` and should mention `@cloudfoundry/toc`
to make the TOC aware of the request. The TOC will then consult any working
groups that may be affected by the removal of this member and use its usual
decision process to approve or reject the removal. 

