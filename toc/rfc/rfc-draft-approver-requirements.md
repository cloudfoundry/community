## Meta
[meta]: #meta
- Name: Approver Requirements
- Start Date: 2022-04-08)
- Author(s): @ameowlia, @ctlong
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Change the requirements for nominating an Approver to allow for a wider range of
contributions to be accepted.

## Problem

The current criteria that must be met in order to be nominated as an approver
are very narrow. Not every working group receives PRs frequently, providing
scant opportunity for folks to review them in order to be considered for
nomination as an approver. Additionally, other valuable functions within working
groups (ie. reviewing Issues, answering Slack questions, etc.) are ignored as
options to be considered for nomination.

## Proposal

We want to consider a wider range of engagement for consideration when
nominating approvers. This RFC proposes to change the [language in the approver
requirements](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md#requirements-2)
to the following:

**Requirements**
* Be a reviewer for at least 3 months
* Have completed at least 20 of the following
  * Submitted a substantial PR
  * Reviewed a substantial PR
  * Submitted a substantial Issue
  * Reviewed a substantial Issue
  * Involved in technical discussion. This includes, but is not limited to,
    being involved in technical decision making in proposals or resolving
    interrupts in slack.
* Nominated by a WG lead (with no objections from other leads).

A substantial PR is anything that changes the logic of the code or introduces a
complex amount of documentation. The following are examples of substantial PRs:
bug fixes, features, large docs changes like creating a new debugging document
or new architecture diagram. The following are examples of non-substantial PRs:
dependabot PRs or small docs changes like fixing typos or reorganizing content.

A substantial Issue is anything that requires knowledge of the codebase. The
following are examples of substantial Issues: feature requests, bug write ups,
debugging help requests. The following are examples of non-substantial Issues:
minor doc change requests.

The WG lead has final say if an issue, PR, or discussion is considered
substantial.

When a reviewer has achieved all of these requirements they can then open a PR
against the community repo adding their name to the list of approvers in a
Working Group. This PR should include links to all of their completed
requirements.

