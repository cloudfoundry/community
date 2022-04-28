# Meta
[meta]: #meta
- Name: Remove Non-Standard Github Teams
- Start Date: 2022-04-28
- Author(s): @gerg
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: [https://github.com/cloudfoundry/community/pull/262](https://github.com/cloudfoundry/community/pull/262)


## Summary

Remove Github teams (and associated access) that are outside of the CFF
governance model.

## Problem

There are currently many Github teams in the `cloudfoundry` Github organization
that do not correlate with a CFF-recognized entity (working group, TOC, etc).
These teams grant access to CFF-governed repositories, but are not beholden to
the CFF's roles and other processes for governing access. In addition, the
volume of Github teams makes it more difficult to manage team access via the
Github UI and intermediary tools like
[`cloudfoundry.yml`](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml).

## Proposal

Delete all Github teams in the `cloudfoundry` organization that do not conform
to
[rfc-0005-github-teams-and-access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0005-github-teams-and-access.md)
or another CFF-recognized entity (for example: the
[`toc`](https://github.com/orgs/cloudfoundry/teams/toc) team).
