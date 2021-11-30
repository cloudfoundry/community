# Move to a PR Only Workflow

## Problem
It is near impossible for community members to know what is being worked on and
why changes are being made. This makes it difficult for anyone to join our
community or for anyone to try to do code archeology.

## High Level Solution
* Use branch protection to prevent any direct committing to the default branch of all repos.
* All changes must be submitted as a PR.
* All PRs must have one approver review and approve the code via github reviews.

**Happy path workflow**
1. A community member makes a PR.
1. An approver uses github reviews and approves the change.
1. The approver merges the PR.

## Solution Details

**Github Setup**
Each repo will require the following branch protections for their default branch:
* "Require a pull request before merging": checked
* "Require approvals": checked
* "Required number of approvals before merging": 1

<img src="https://i.ibb.co/qnNvkT7/Screen-Shot-2021-11-09-at-7-47-29-AM.png">

## FAQ

**What if the pipeline is red?**
Just because a PR has been approved does not mean it will be merged right away.
Approvers will aim to merge PRs as quickly as is safe to do so, but reserve the
right to not merge PRs right away.

**What if the PR breaks the pipeline?**
Whoever diagnoses the broken pipeline should alert the PR author and, if they
have permission, they should revert the PR. If they don’t have permission to
revert they should ask the original reviewer to revert or submit a PR to revert
so another approver can merge.

**Can a PR author review their own PR?**
No. Github does not let you review your own PRs. So even if you are a Working
Group approver you will need another approver to review your PR. We can change
this if it is a burden.

**What about bots?**
Some teams have bots (like dependabot) that currently make a PR, wait for checks to pass, and then merge their own PR. With this review proposal that will no longer be possible. To continue with a fully automated workflow we suggest using a **two bot** workflow. Have one bot for making PRs (dependabot) and one for merging them (mergebot). This is similar to the Istio and Kubernetes processes. 


