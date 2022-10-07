# Meta
[meta]: #meta
- Name: Default git branch protection rules
- Start Date: 2022-10-07
- Author(s): AP-Hunt, Benjamintf1, rkoster
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/449


## Summary

In Q3 2022, the technical oversight committe accepted and implemented [an RFC for the managemnet of Github teams and user access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0014-github-teams-and-access.md). This unintentionally broke the workflow and branch protection roles of some working groups.

This RFC seeks to address that by defining a baseline of branch protection rules across all repositories under management in the cloufoundry GitHub org.

## Problem

Prior to the approval and implementation of RFC 0014, some working groups had set up branch protection rules on their repositories to enable things like:
* allowing members of cloudfoundry org without approver status in the working group to push only to non-release-line branches
* allowing approvers in the working group to push to both release-line and non-release-line branches
* allowing release bots to push commits to release-line branches

When the TOC approved and implemented [RFC 0013](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0013-remove-nonstandard-github-teams.md), any GitHub teams within the cloudfoundry org that were **not** defined in working group charter were removed. This broke branch protection rules because they were now referring to non-existent teams.

## Proposal

The CFF TOC should implement basic branch protection rules for all repositories in an automated manner, and allow working groups to extend them as they see fit. This can be achieved, technically, with [the `branchprotector` tool from `prow` toolset](https://github.com/kubernetes/test-infra/blob/master/prow/cmd/branchprotector/README.md).

We propose that protection be applied to all branches matching the expressions `main` or `v[0-9]*`.

On protected branches, we propose the following rules:
* working group leads, approvers, and bots will be able to push directly to the branch
* contributors outside of leads, approvers, and bots must raise a pull request before the change can be merged
* pull requests must have at least 2 approvals, at least 1 of which must come from a working group approver or lead.