# Meta
[meta]: #meta
- Name: Roadmap Visibility Expectations
- Start Date: 2022-02-23
- Author(s): @rkoster, @ameowlia, @geofffranks
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/173


## Summary

We wish to provide a common format for working groups to provide visibility into work
currently in progress for repos, PR/Issue review, and roadmaps. This should make it
easier for external parties to view priorities and progress in things they're interested in,
and help build a bigger sense of community.

## Problem

There is a gap in visibility into issues/PRs that are being worked on, as well as new
features under development. Much of this work/discussion/prioritization is done
internally within different companies, and community members have a difficult time
understanding what’s happening, or if they’ve opened a request to a repo that no one
is watching.

## Proposal

### High Level Solution
- Provide GitHub Project per Working Group for tracking PR status + issue status + prioritization
- Encourage Slack integration on issue and PR creation for repos
- Provide GitHub Project per Working Group for large technical proposals/new feature RFCs
- Adopt the PR-only workflow on repos via automation
- Encourage weekly review/triage of issues and PRs for each Working Group

### Solution Details

#### Create a config file to iterate Working Groups, areas, and their repos
- Can be used to automate access control for teams, enforce branch restrictions, etc.
- Would be located at `cloudfoundry/community/toc/working-groups/wg-configs.yml`

#### Provided GitHub Projects
- Make use of terraform integrations and a GitHub action on the `cloudfoundry/community`
  repo to create/manage projects, columns, and an ongoing GitHub action that will
  add the cards to projects.
- This can be configured to create projects on a per-WG basis, or per WG-area
  basis as needed

#### Provided Slack Integration Instructions
- Provide a doc in the `cloudfoundry/community` repo detailing how to set up the
  GitHub slack app integration.

### FAQ

#### Does my Working Group have to use these?
No, terraforming of repos would be opt-in by editing a configuration file in the
community repo.

#### Do we have to use the default project columns?
No, the action making cards for the project only needs a column ID to place
cards initially. If you want to bring-your-own project, that’s fine.

#### What about GitHub Projects’ 25-repo single-org limitation?
We’re using terraform to populate the cards initially, rather than the built in
issue/project integration, which lets us get around this limitation. TF won’t
manage the cards otherwise until the PR is closed. In the long term we will move
to GitHub's new style projects which remove this limitation.

#### Why use a GitHub Project for proposals?
Teams might use a variety of solutions for writing proposals (Google docs, GitHub
repos with markdown docs + PRs, long-lived GitHub Issues, internal project-management
tools). Having each Working Group utilize a GitHub project with cards linking to the underlying
proposals gives the community a consistent experience for finding out what’s going on.

#### Why are there different projects for proposals vs PRs?
Chances are there will be different swimlanes for proposals, rather than PRs,
and the noise of both in a single board may be troublesome.

