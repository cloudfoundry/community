# Cloud Foundry Request For Comments

Cloud Foundry community members use this directory as a common, public forum to make, discuss, and record both procedural and technical decisions. These decisions may result in a sequence of actions for the community to take, either as a one-off to address an outstanding issue or as an ongoing process, or in a new or revised set of guidelines or standards for the community to follow.

## Process

1. Create a new branch on this repo and copy `rfc-0000-template.md` to `rfc-0000-my-proposal-title.md` and edit. The number of the RFC should not be selected until you are ready to merge the RFC. The number used should be the next sequential number to follow on from the already merged RFCs. This is to remove numbering gaps that would be caused by rejected RFCs if numbers were chosen earlier.
1. If your RFC is relevant for only a single Working Group, please place it in a subdirectory of `toc/rfc` specifically for that working group.
   1. If that Working Group hosts its RFCs elsewhere, its RFC subdirectory will contain a file called `EXTERNAL.md` that contains a link to that group's RFC repository. In that case, follow that link to create the group-specific RFC in that repository.
1. Include any images etc in a separate directory named `rfc-000` (using the number of your RFC) and link to them.
1. Make a Pull Request (PR) for your branch.
1. Rename your file and directory with the number of the PR and push as a new commits.
1. Tag `@toc` and any relevant working groups in your PR to enable discussion of the RFC. 
1. Cloud Foundry community members discuss your proposal using both inline comments against your RFC document and the general PR comments section.
1. As changes are requested and agreed in comments, make the changes in your RFC and push them as new commits.
1. Stay active in the discussion and encourage and remind other relevant people to participate. If you’re unsure who should be involved in a discussion, ask the Leads for relevant working groups or the TOC. If you start an RFC it is up to you to engage people to guide it through the process.
1. Once the proposers are ready and all discussions have taken place they will propse a "motion for final comment period (FCP)" with the proposed outcome (accepted / rejected). The FCP will last for 7 days.
1. Once the FCP is proposed, approvals shall be given using the Github review system, the PR can be merged early if there is a majority agreement by the project leads.
1. When an RFC is accepted, ensure the Cloud Foundry community is made aware of it via Slack using the previously used channels.
1. An RFC can be rejected. This can happen if a consensus isn’t reached, or people agree rejecting it is the right thing to do. In this case the PR should be closed with a suitable comment. There is no preset time limit for an RFC to be automatically rejected, it must be explicitly acknowledged that a consensus was not reached. The proposal author or the TOC should perform the closing of the rejected RFC.

## Managing Standards and Processes

[Standards](#Standards) and [Processes](#Processes) RFCs shouldn’t be substantially altered after they are accepted, although it’s fine to correct typos and other mistakes via a new PR. In order to change a Standard or Process, the original RFC must be superseded by a new one. The process for this is:

1. Create a new RFC PR as above, noting in the summary which RFC it is superseding.
1. In the same branch, mark the old RFC as superseded and link to the new RFC and move (using `git mv`) it into the archived directory.
1. When the new RFC is accepted and the PR is merged, the old RFC will no longer be active.

## Managing Action Plans

For RFCs where the outcome is an agreed Action Plan, you may want to update the RFC with meaningful status updates in new PRs. Once the plan is either complete or no longer relevant, it should be moved to the archived directory in a new PR.

### Definitions

#### Standards

A standard is a repeatable, harmonised, agreed and documented way of doing something. Standards contain technical specifications or other precise criteria designed to be used consistently as a rule, guideline, or definition.

#### Processes

A process is a procedure, something you do in order to achieve a certain result.
