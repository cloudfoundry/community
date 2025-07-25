# Meta
[meta]: #meta
- Name: Default git branch protection rules
- Start Date: 2022-10-07
- Author(s): AP-Hunt, Benjamintf1, rkoster
- Status: Accepted
- RFC Pull Request: [community#449](https://github.com/cloudfoundry/community/pull/449)


## Summary

In Q3 2022, the Technical Oversight Committee accepted and implemented [an RFC for the management of GitHub teams and user access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0014-github-teams-and-access.md). This unintentionally broke the workflow and branch protection rules of some working groups.

This RFC seeks to address that by defining a baseline of branch protection rules across all repositories under management in the cloudfoundry GitHub org.

## Problem

Prior to the approval and implementation of RFC 0014, some working groups had set up branch protection rules on their repositories to enable things like:
* allowing members of cloudfoundry org without approver status in the working group to push only to non-release-line branches
* allowing approvers in the working group to push to both release-line and non-release-line branches
* allowing release bots to push commits to release-line branches

When the TOC approved and implemented [RFC 0013](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0013-remove-nonstandard-github-teams.md), any GitHub teams within the cloudfoundry org that were **not** defined in working group charter were removed. This broke branch protection rules because they were now referring to non-existent teams.

## Proposal

The CFF TOC should implement basic branch protection rules for all repositories in an automated manner, and allow working groups to extend them as they see fit. This can be achieved, technically, with [the `branchprotector` tool from `prow` toolset](https://github.com/kubernetes/test-infra/blob/master/prow/cmd/branchprotector/README.md).

We propose that protection be applied to all branches matching either the default branch or the expression `v[0-9]*`.

On protected branches, we propose the following rules:
* only the bots for the Working Group owning the repository and any areas in the Working Group contributing to the repository may push directly to the branch
* human contributors must make contributions through a regular pull request workflow.

With respect to the approval of pull requests, we propose that the number of approvals required will depend on the number of people in the approver role of a working group:
* 0 approvals will be required when a working group has 3 or fewer people in the approver rule
* 1 approval will be required when a working group has 4 or more people in the approver role.

The automation should allow to override the standard branch protection per respository using a configuration file maintained in this community repository. This allows working group leads e.g. to reduce the number of required approvals if several approvers are temporarily not available.

## Amendments

### Protection by Default

To improve the security posture of the foundation, the branch protection rules defined in this RFC are applied by default to all repositories of all Working Groups. The previous opt-in mechanism via a flag in Working Group charters is removed.

Working Groups can request exceptions for specific repositories by creating a pull request against `orgs/branchprotection.yml`. The pull request description MUST contain a justification for the exception.
