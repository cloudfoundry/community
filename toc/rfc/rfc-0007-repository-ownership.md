# Meta
[meta]: #meta
- Name: Working Group Repository Ownership
- Start Date: 2022-04-19
- Author(s): [@emalm](https://github.com/emalm)
- Status: Accepted
- RFC Pull Request: [community#251](https://github.com/cloudfoundry/community/pull/251)


## Summary

Adding a repository to the ownership scope of a Working Group, removing a repository from its scope, or transferring a repository between Working Groups within the `cloudfoundry` GitHub organization requires approval separately from each affected Working Group and from the Technical Oversight Committee (TOC).


## Problem

As the CF community completes its rollout of the new TOC and Working Group governance structure, the large number of unaddressed PRs about repository ownership across Working Groups has illustrated that the community needs a clearer and more consistent process to handle such ownership changes. In particular, there are currently a significant number of repositories in the [`cloudfoundry`](https://github.com/cloudfoundry) and [`cloudfoundry-incubator`](https://github.com/cloudfoundry-incubator) GitHub organizations that are not yet officially assigned to a Working Group, and the community must decide which ones will be managed by which Working Groups and which ones will be archived.

Even after the CF community resolves the ownership of the existing repositories in these two GitHub organizations, it still needs a clear process to create new repositories under a Working Group, to move repositories between Working Groups, and to remove a repository from a Working Group.


## Proposal

### Ownership model

We can represent the ownership structure of the repositories in the `cloudfoundry` GitHub organization as a partition of the set of repositories. Each Working Group has a subset of repositories that it owns, and there are separate subsets under ownership of the TOC and of the CF Foundation staff, respectively. Finally, there are two separate subsets of unmanaged repositories: ones that are archived and ones that are active. Since this collection of subsets is a partition, the subsets MUST be mutually exclusive and comprehensively exhaustive: each repository in the organization is in exactly one of these subsets.

The subset of repositories that each Working Group owns MUST be identical to the set of repositories listed in its charter description. This set of repositories MAY further be partitioned into technical areas within the Working Group, at the discretion of the Working Group.

The subsets of repositories that the TOC and the CF Foundation staff own SHOULD be as small as possible and should be scoped to those that enable the effective operation of the CF community. These repostiories SHOULD NOT be concerned with development of tools and systems that are broadly valuable to the end-user community, as the Working Groups collectively SHOULD own those kinds of repositories instead. These two sets of repositories MUST be listed in the charter document for the TOC in this repository.

The subset of unmanaged active repositories SHOULD be empty under steady-state operation. The community MUST collectively act to resolve the status of an unmanaged active repository within a reasonable period of time, either by archiving it or by placing it under the ownership of a  Working Group, of the TOC, or of the CFF staff, as is appropriate.

The ownership structure of the repositories in the `cloudfoundry-incubator` GitHub organization can be described the same way as a partition of the set of repositories amongst the Working Groups. Since incubation is no longer a relevant concept in CF Foundation governance, the community SHOULD act to move all of the active repositories in this organization to the main `cloudfoundry` GitHub organization in a reasonable period of time, while coordinating with the Working Groups to minimize negative effects on development and release practices. The community MUST NOT create new repositories in the `cloudfoundry-incubator` GitHub organization and MUST NOT move any existing repositories into it.


### Ownership changes

A change to repository ownership is a change to the partition of the set of repositories in the `cloudfoundry` organization. For a single repository, the possible changes are the addition of a new repository to the one of the subsets in the partition, the transfer of an existing repository from one subset to another, or the removal of a repository from a subset.

Addition of a repository to the partition corresponds either to creating a new repository or transferring an existing repository from another GitHub organization.

Removal of a repository corresponds either to transferring it to another GitHub organization or to deleting the repository entirely, neither of which should be undertaken lightly. The CF community SHOULD ensure that either of these cases receives thorough consideration and scrutiny before proceeding.

Proposed changes to repository ownership SHOULD be submitted for consideration as a pull request on the [Cloud Foundry community repository](https://github.com/cloudfoundry/community) that modifies the charter documents of the appropriate Working Groups. As per [RFC 0003](rfc-0003-pr-only-workflow.md), a pull request is preferable in order to provide visibility in the CF community, to encourage asynchronous discussion across time zones, and to reduce fragmentation of discussion.


### Ownership change approvals

The TOC MUST approve any change to repository ownership, just as it originally approved the initial set of repositories for each Working Group. Approval consists of a quorum decision by the TOC.

Additionally, if a change affects the subset of repositories that a Working Group owns, that Working Group MUST approve the change as well. Approval consists of a quorum decision by the leads of the Working Group.

The TOC MUST also approve of any proposal to create a new repository within the `cloudfoundry` GitHub organization or to rename an existing repository. 

We illustrate several different cases of repository ownership changes and the approvals required for them to proceed:

#### Case 1: A Working Group wants to create a new repository under their ownership.

Approval requirements
* The Working Group MUST approve the addition of the proposed repository to the set of repositories that it owns.
* The TOC MUST approve the creation of the proposed repository.
* The TOC MUST approve the addition of the proposed repository to the Working Group's subset.

Steps
1. Someone opens two PRs. The first PR adds the repo to the [cloudfoundry.yml](../../org/cloudfoundry.yml). The second PR adds the repo to the desired Working Group's yaml. These PRs should link to each other.
2. The Working Group and TOC both approve both PRs.
3. The TOC merges the first PR.
4. Wait for automation to run to create the repo.
5. The TOC merges the second PR.

#### Case 2: The TOC wants Working Group A to take ownership of an unclaimed active repository.

Approval requirements
* The TOC MUST approve the change in the ownership scope of Working Group A.
* Working Group A MUST approve the change to the set of repositories they own.

Steps
1. Someone opens a PRs that adds a repo to the desired Working Group's yaml.
2. The Working Group and TOC both approve the PR.
3. The TOC merges the PR.


#### Case 3: Working Group A wants to claim ownership of a repository currently owned by Working Group B.

Approval requirements
* Both Working Group A and Working Group B MUST approve the change to the sets of repositories they own.
* The TOC MUST also approve the transfer of the repository from Working Group B to Working Group A.

Steps
1. Someone opens a PR that moves a repo from Working Group A's yaml to Working Group B's yaml.
2. Working Group A, Working Group B, and TOC approve the PR.
3. The TOC merges the PR.

#### Case 4: A Working Group wants to archive a repository that it currently owns.

Approval requirements
* The Working Group MUST approve the removal of the repository from the set of repositories that it owns.
* The TOC MUST approve the removal of the repository from the Working Group and the archival.

Steps
1. Someone opens a PR that: marks the repo as archived in the [cloudfoundry.yml](../../org/cloudfoundry.yml) and that removes the repo from the Working Group's yaml.
2. The Working Group and TOC both approve the PR.
3. The TOC merges the PR.

#### Case 5: A Working Group wants to delete a repository that it currently owns.
⚠️ Deleting a repository will usually be rejected by the TOC. Please consider archiving instead.

Approval requirements
* The Working Group MUST approve the removal of the repository from the set of repositories that it owns.
* The TOC MUST approve the removal of the repository from the Working Group and the deletion.

Steps
1. Someone opens a PR that removes the [cloudfoundry.yml](../../org/cloudfoundry.yml) and removes the repo from the Working Group's yaml.
2. The Working Group and TOC both approve the PR.
3. The TOC merges the PR.
4. A github admin deletes the repo.

#### Case 6: A Working Group wants to cease maintaining a repository that it currently owns.

Approval requirements
* The Working Group MUST approve the removal of the repository from the set of repositories that it owns.
* The TOC MUST approve the removal of the repository from the Working Group.
* In addition, the TOC MUST decide whether to archive the repository or to arrange for another Working Group to own it instead (possibly a newly formed one, if appropriate and if supported by community contributors).
* Note: In this case, it is unlikely that either the TOC or the CFF staff should own this repository, as it was already owned by some Working Group in the CF community.


Steps
1. Someone opens a PR that removes the repo from the Working Group's yaml.
2. The TOC reviews and decides what action to take with the repo. Other PRs might be required for this step.
3. The Working Group and TOC both approve the PR.
5. The TOC merges the PR.

#### Case 7: A Working Group wants to rename a repository that it currently owns.

Approval requirements
* The Working Group A and the TOC MUST both approve of the new name for the repository.

Steps
1. Someone opens two PRs:
   * PR 1: Add the new repo to the [cloudfoundry.yml](../../org/cloudfoundry.yml).
   * PR 2: Rename the repo in the Working Group's yaml. Remove the old repo from the [cloudfoundry.yml](../../org/cloudfoundry.yml).
The second PR adds the repo to the desired Working Group's yaml. These PRs should link to each other.
3. The Working Group and TOC both approve both PRs.
4. The TOC merges the first PR.
5. Wait for automation to run to create the repo.
6. A github admin copies the old repo contents to the new repo.
7. The TOC merges the second PR.
8. A github admin deletes the old repo.
