# Cloud Foundry Request For Comments

Cloud Foundry community members use this directory as a common, public forum to make, discuss, and record both procedural and technical decisions. These decisions may result in a sequence of actions for the community to take, either as a one-off to address an outstanding issue or as an ongoing process, or in a new or revised set of guidelines or standards for the community to follow.

## Process

### Draft Creation

1. Create a new branch on this repository or on a fork of it.
1. Copy `rfc-template.md` to `rfc-draft-<my-proposal-title>.md`, where `<my-proposal-title>` is a short identifier for the RFC, and edit the draft RFC document.
1. If your RFC is relevant for only a single Working Group and that Working Group hosts its RFCs elsewhere, please create a file called `EXTERNAL.md` that contains a link to that group's RFC repository and place it in a subdirectory of `toc/rfc` specifically for that working group. In that case, follow that link to create the group-specific RFC in that repository.
1. If your RFC includes images, include them in a separate directory named `rfc-draft-<my-proposal-title>` and link to them from the RFC document.

### Public Discussion Period

1. Make a Pull Request (PR) for your branch.
1. Update the metadata section in your RFC draft with a link to its PR.
1. Mention `@cloudfoundry/toc` and any relevant working groups in your PR to raise awareness of the proposed RFC.
1. Cloud Foundry community members discuss your proposal using both inline comments on your RFC document and the general PR comments section.
1. As changes are requested and agreed upon in comments, make corresponding changes in your RFC draft and push them as new commits.
1. Stay active in the discussion and encourage and remind other relevant people to participate. If you’re unsure who should be involved in a discussion, ask the Leads for relevant working groups or the TOC. If you start an RFC it is up to you to engage people to guide it through the process.

### Final Comment Period

1. Once enough of the discussions conclude, propose a motion for a Final Comment Period (FCP), including the desired outcome ("accepted" or "rejected").
1. For the FCP to start, a majority of the decision makers (the TOC or the leads for relevant working group) must approve the FCP motion. The FCP will last for 7 days.
1. Once the FCP starts, approvals shall be given using the GitHub review system. The PR can be merged or closed early if there is consensus among the decision makers.
1. If substantial new issues are raised during the FCP, the RFC shall go back into the public discussion phase.
1. If the RFC is accepted, ensure the Cloud Foundry community is made aware of it via Slack using the previously used channels.
1. If the RFC is rejected, the author or a TOC member should close the PR for the RFC with a suitable comment.

### Number Assignment

Each accepted RFC is assigned a unique sequence number, replacing the `draft` segment in the names of its document and its optional image directory. This sequence of RFC numbers is shared between the community-wide RFCs and the working-group-specific RFCs contained in this repository. The user merging an RFC after a decision to accept is responsible for assigning the correct sequence number to that RFC.

The [`assign-rfc-number.sh`](assign-rfc-number.sh) script will assign the next RFC number in sequence. Immediately after the RFC PR is merged:

1. Check out the `main` branch at the RFC PR merge commit.
1. Change into the `toc/rfc` directory.
1. Run `./assign-rfc-number.sh <rfc-merge-commit-sha>` where `<rfc-merge-commit-sha>` is the "commit-ish" (commit SHA or commit expression) that resolves to the merge commit of the RFC.
1. If you had set `NOPUSH=true` when running the script, push the numbering commit to `main`.

Script options, to be set via environment variable (such as `DEBUG=true ./assign-rfc-number.sh`):
* `MAIN_BRANCH`: Sets the main branch of the repository. (Default: `main`)
* `OWNER`: Sets the owner of the repository. (Default: `cloudfoundry`)
* `REPO`: Sets the name of the repository. (Default: `community`)
* `DEBUG`: Set to a nonzero value to enable script debugging via the `-x` flag in Bash. (Default: unset)
* `NOPUSH`: Set to a nonzero value not to push the renumbering commit automatically. (Default: unset)

## Managing Standards and Processes

An RFC defining a [Standard](#Standards) or a [Process](#Processes) should not be substantially altered after it is accepted, although it is fine to correct typos and other mistakes via a new PR. In order to change a Standard or Process, a new RFC must supersede the original RFC. The process for this is:

1. Create a new RFC PR as above, noting in the summary which RFC it is superseding.
1. In the same branch, change the status of the original RFC to "Superseded", link to the new RFC, and use `git mv` to move it into the `archived` directory.
1. When the new RFC is accepted and the PR is merged, the original RFC will no longer be active.

## Managing Action Plans

For an RFC where the outcome is an agreed Action Plan, you may want to update the RFC with meaningful status updates in new PRs. Once the plan is either complete or no longer relevant, it should be moved to the archived directory in a new PR.

### Definitions

#### Standards

A standard is a repeatable, harmonised, agreed and documented way of doing something. Standards contain technical specifications or other precise criteria designed to be used consistently as a rule, guideline, or definition.

#### Processes

A process is a procedure, something you do in order to achieve a certain result.
