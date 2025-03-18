# Meta
[meta]: #meta
- Name: Remove Non-Standard GitHub Teams
- Start Date: 2022-04-28
- Author(s): @gerg
- Status: Accepted
- RFC Pull Request: [community#262](https://github.com/cloudfoundry/community/pull/262)


## Summary

Remove GitHub teams (and associated access) that are outside of the CFF
governance model.

## Problem

There are currently many GitHub teams in the `cloudfoundry` GitHub organization
that do not correlate with a CFF-recognized entity (working group, TOC, etc).
These teams grant access to CFF-governed repositories, but are not beholden to
the CFF's roles and other processes for governing access. In addition, the
volume of GitHub teams makes it more difficult to manage team access via the
GitHub UI and intermediary tools like
[`orgs.yml`](https://github.com/cloudfoundry/community/blob/main/orgs/orgs.yml).

Nevertheless, controlling access to Cloud Foundry repositories only by teams defined by CFF technical governance is a substantial change from the previous system of access and team management and in the short term will cause unexpected loss of access to repositories for some contributors and automated development and release processes.

As per [RFC 0007](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0007-repository-ownership.md), CFF staff also require access to many repositories in the Cloud Foundry GitHub organization that are outside the scope of project technical operation, such as those for CFF websites or the Cloud Foundry Certified Developer examinations.
## Proposal

Delete all GitHub teams in the `cloudfoundry` organization that do not conform
to
[rfc-0005-github-teams-and-access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0005-github-teams-and-access.md)
or another CFF-recognized entity, such as CFF staff members.

To allow the CF community to function while the Working Groups adjust their scope and membership, the TOC will permit the formation of exceptional teams on a case-by-case basis. These exceptional teams must be identified as such clearly in their names with phrases such as "temporary" and "delete me", and these teams should be related to unofficial teams that were previously deleted. The TOC and Working Groups will review these exceptional teams regularly for deletion, with the goal of removing all exceptional teams by the end of 2022.

CFF staff may create teams as needed to administer repositories outside the scope of technical project operation. The names for any such teams should clearly indicate their relation to CFF staff responsibilities.
