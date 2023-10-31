# Meta
[meta]: #meta
- Name: Promoting and Revoking Working Group Leads
- Start Date: 2023-10-11
- Author(s): @ameowlia
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/704

## Summary

Define the process for promoting or removing Tech Leads and Execution Leads for
Working Groups.

## Problem

Currently there is no defined process for how to promote or remove Tech Leads
or Execution Leads for Working Groups. This process should be defined.

## Proposal
In this proposal the word "Lead" encompasses both the "Tech Lead" and
"Execution Lead" roles. As currently stated in the
[ROLES.md](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md)
document, both Lead roles are sponsored by the TOC. 

### Promotion to Lead
* If a person meets the criteria to be a Lead as defined in
  [ROLES.md](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md),
  they MAY submit a PR adding themselves to the contributors.yml as a Lead.

* The TOC will start a one week final comment period on the PR to collect
  approvals from the required parties.

* The TOC MUST approve the PR before it can be merged.

* At least one current Lead for the affected Working Group SHOULD approve the PR
  before it can be merged.

* Any current approvers for the affected Working Group MAY 'vote' by commenting
  "+1" or "-1" on the PR. 75% or more of the votes from current Working Group
  approvers MUST vote "+1" for the promotion in order for the PR to be merged.

### Revoking Lead Role
* A Lead MAY revoke their own role by submiting and merging their own PR to
  remove themselves from the `contributors.yml` file for their Working Group.
  
* Any Approver in the Working Group or a TOC member MAY submit a PR revoke the
  Lead role from the current holder. The person whose role is being revoked
  MUST be given two weeks to refute the revocation. The TOC MUST make the final
  decision to revoke the Lead role.

  
