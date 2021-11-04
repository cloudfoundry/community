# Reviewer Workflows for Issues and PRs

**Date of Forum to be Discussed:** Wednesday Nov 3, 2021 9 Pacific / 12 Eastern / 17 Britain / 18 Germany
See the community calendar for more details.

**Author:** Amelia Downs - @ameowlia

## Problem
Our working group has 70+ repos. In order to run a healthy open source community we need to make sure that we triage issues and merge PRs in a timely fashion.

**As a PR author I want:**
* To have my PR reviewed and merged in a timely manner.

**As an issue author I want:**
* To have guidance on how to fix my bug in a timely manner.

**As an Approver I want:**
* To know which PRs and issues I have to review.
* I want to know what is expected of me as a reviewer.

**As a Tech Lead I want:**
* To know how many open issues and PRs there are.
* To be able to assign reviews for open issues and PRs.

## Solution
#### PR + Issue Tracking Github Projects for Each Sub-Group
Each sub-group of our working group has a github project.
These projects will contain a card for each issue and PR for the subgroup.
The tech lead is responsible for assigning reviewers.
The reviewers are responsible for triaging the card until either they make it to the “Done” or “Needs Fix” swimlanes.
The reviewer is not responsible for fixing the bug for a given issue.

**Links to Github Projects**
* [App Platform - Diego](https://github.com/orgs/cloudfoundry/projects/20)
* [App Platform - Garden Containers](https://github.com/orgs/cloudfoundry/projects/23)
* [App Platform - Logging and Metrics](https://github.com/orgs/cloudfoundry/projects/19)
* [App Platform - Networking](https://github.com/orgs/cloudfoundry/projects/24)

### Issue Workflow
Below is the outline of a typical issue workflow. [See drawing](https://docs.google.com/drawings/d/1_W-Xk8pCUCv1la-rEuJAA8rE_ivMKrmxrmWyR7b0Tk4/edit?usp=sharing).
<img src="https://i.ibb.co/BN2qS60/Screen-Shot-2021-10-28-at-5-37-39-PM.png">

### PR Workflow
Below is the outline of a typical PR workflow. [See drawing](https://docs.google.com/drawings/d/1BlIXESgk_Ycp9jRQdnY_v_qrgn2fGwCSJ-eiAssryfg/edit?usp=sharing).
<img src="https://i.ibb.co/7vCsqBX/Screen-Shot-2021-10-28-at-5-38-59-PM.png">


## FAQ

❓ **How can I see what is assigned to me?**
1. To view all open issues assigned to you in the cf org
  *   Go to this link when you are logged in: [https://github.com/issues/assigned?q=is%3Aopen+archived%3Afalse+org%3Acloudfoundry](https://github.com/issues/assigned?q=is%3Aopen+archived%3Afalse+org%3Acloudfoundry).
2. To view all open issues assigned to you for a particuluar project
  * Go to the github project.
  * Click on your icon on a card that is already assigned to you.
  * OR 
  * Add the following query param to the URL: `?card_filter_query=assignee:YOUR-GITHUB-USERNAME`.

❓ **How much time will this take per week?**

I don’t know! We are trying this for the first time and we will learn together.

❓ **As an approver, how long do I have to review something?**

I am not currently setting any SLIs or SLOs. I ask that you please do your best
to triage your assigned PRs and issues at least once a week.

❓ **What if I don’t think I am qualified to review something?**

I ask that you try your hardest to review something.
However, if you can't, that is okay.
Either reach out in our working group slack channel (#wg-app-runtime-platform) and ask for
someone else to review it or reach out to your tech lead and ask them to assign someone else.

❓ **What if I want to review something that is assigned to someone else?**

Great! If they haven’t started on it, feel free to unassign them and assign yourself as a reviewer.

❓ **What about issues that are actually proposals?**

Proposals are issues that are created and tracked in order to facilitate
conversation amongst the community before a large chunk of work is started.
These will be tracked in a different project ([App Platform Proposals](https://github.com/orgs/cloudfoundry/projects/22)).
The workflow for this project is not flushed out yet.
