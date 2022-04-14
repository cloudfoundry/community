# Meta
[meta]: #meta
- Name: Role Change Process
- Start Date: 2022-04-13
- Author(s): @gerg
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Define the process for granting or revoking roles.

## Problem

There are currently
[descriptions](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md)
for the criteria necessary to become a Contributor or Approver. It is not
currently defined how people apply for or are granted these roles. This makes it
difficult for community members to know how to apply for a role promotion and
difficult for Working Group leadership to manage Contributor and Approver
candidates.

In addition, there is no defined process for removing people from Contributor or
Approver roles if they are no longer interested in participating at that level.

## Proposal

### Promotion to Contributor

- When a person meets the criteria to be a Contributor as defined in
[ROLES.md](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md),
they may submit a PR adding themselves to the organization in
[cloudfoundry.yml](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml).

- Two existing Contributors or Approvers must attest that they meet the criteria
  by reviewing the PR.

- An existing Contributor or Approver may submit the promotion request on behalf of someone else, but they
  may not serve as a reviewer.

- Any Working Group Lead may merge the PR after it has been reviewed.

- TOC members may bypass the review process and merge the PR at their
  discretion.

### Promotion to Approver

- When a person meets the criteria to be an Approver for a Working Group as defined in
[ROLES.md](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md),
they may submit a PR adding themselves to the appropriate Working Group in
[cloudfoundry.yml](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml).

- Two existing Approvers for that Working Group must attest that they meet the criteria
  by reviewing the PR.

- For Working Groups with fewer than 4 approvers, a single Approver review is
  sufficient.

- An existing Approver may submit the promotion request on behalf of someone else, but they
  may not serve as a reviewer.

- A Working Group Lead for that Working Group may merge the PR after it has been
  reviewed.

- TOC members may bypass the review process and merge the PR at their
  discretion.

### Revoking Contributor Role

- People with the Contributor role may submit a PR to revoke their role by
  removing the appropriate entry from
  [cloudfoundry.yml](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml).

- An existing Contributor or Approver may submit the revocation request on
  behalf of someone else, but the person whose role is being revoked must be
  given a week to refute the revocation.

- Any Working Group Lead may merge the PR, without review.

- TOC members may merge the PR at their discretion.

### Revoking Approver Role

- People with an Approver role may submit a PR to revoke their role by removing
  the appropriate entry from
  [cloudfoundry.yml](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml).

- An existing Approver may submit the revocation request on behalf of someone
  else, but the person whose role is being revoked must be given a week to
  refute the revocation.

- A Working Group Lead for that Working Group may merge the PR, without review.

- TOC members may merge the PR at their discretion.
