# Meta
[meta]: #meta
- Name: Move to a PR Only Workflow
- Start Date: 2022-02-28
- Author(s): @ameowlia
- Status: Accepted
- RFC Pull Request: [community#171](https://github.com/cloudfoundry/community/pull/171)


## Summary

By default, all repos SHOULD require PRs for changes.

## Problem

It is near impossible for community members to know what is being worked on and
why changes are being made. This makes it difficult for anyone to join our
community or for anyone to try to do code archeology.

## Proposal

All repos SHOULD:
* have branch protection to prevent any direct committing to the default branch(es).
* require changes must be submitted as a PR.
* require one approver review and approve the code via github reviews.

**Happy path workflow**
1. A community member makes a PR.
1. An approver uses github reviews and approves the change.
1. The approver merges the PR.

**Github Setup**

To enable this, each repo will require the following branch protections for their default branch(es):
* "Require a pull request before merging": checked
* "Require approvals": checked
* "Required number of approvals before merging": 1

<img src="https://i.ibb.co/qnNvkT7/Screen-Shot-2021-11-09-at-7-47-29-AM.png">

## FAQ

**What if the pipeline is red?**
Just because a PR has been approved does not mean it will be merged right away.
Approvers SHOULD aim to merge PRs as quickly as is safe to do so, but reserve the
right to not merge PRs right away.

**What if the PR breaks the pipeline?**
Whoever diagnoses the broken pipeline SHOULD alert the PR author and, if they
have permission, they SHOULD revert the PR. If they don’t have permission to
revert they SHOULD ask the original reviewer to revert or submit a PR to revert
so another approver can merge.

**Can a PR author review their own PR?**
No. Github does not let you review your own PRs. So even if you are a Working
Group approver you will need another approver to review your PR. We can change
this if it is a burden.

**What about bots?**
Some teams have bots (like dependabot) that currently make a PR, wait for checks
to pass, and then merge their own PR. With this review proposal that will no
longer be possible. To continue with a fully automated workflow a repo MAY use
a **two bot** workflow. Have one bot for making PRs (dependabot) and one for
merging them (mergebot). This is similar to the Istio and Kubernetes processes.
