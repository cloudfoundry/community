# Reviewer Workflows for Issues and PRs

**Date of Forum to be Discussed:** Thursday 10 March, 2022 11 am UTC / 4:30 pm IST
See the community calendar for more details.

**Author:** Marcela Campo - @pivotal-marcela-campo

## Problem
Our working group has many different projects maintained by disjointed groups of people.
In order to run a healthy open source community we need to make sure that we triage issues and merge PRs in a timely fashion.

**As a PR author I want:**
* To have my PR reviewed and merged in a timely manner.

**As an issue author I want:**
* To have guidance on the issue I am having in a timely manner.
* To have information on whether my bug will be fixed and roughly when can I expect that to happen.

**As an Approver I want:**
* To know which PRs and issues I have to review.
* To know what is expected of me as a reviewer.

**As a Tech Lead I want:**
* To know how many open issues and PRs there are.
* To ensure the issues and PRs are either being worked on, prioritised, open for contributions, or closed.

## Solution
#### PR + Issue Tracking Github Projects for Each GitHub Organisation
Our working group has projects in multiple GitHub organisation. Each organisation has a GitHub "Service Management Working Group" project.
These projects will contain a card for each issue and PR for the org, organised by area in different tabs
The tech lead is responsible for assigning reviewers.
The reviewers are responsible for following up on the card until either they make it to the “Done”, "Prioritised" or "Waiting for changes" swimlanes.
The reviewer is not responsible for fixing the bug for a given issue.

**Links to Github Projects**
* [cloudfroundy (Cloud Service Broker | Volume Services)](https://github.com/orgs/cloudfoundry/projects/27)
* [cloudfoundry-incubator (ServiceFabrik)](https://github.com/orgs/cloudfoundry-incubator/projects/3)
* [openservicebrokerapi](https://github.com/orgs/openservicebrokerapi/projects/1)

**PR Workflow**
```
Inbox -> Pending review -> Review in progress [-> Waiting for changes] -> Pending merge -> Done
                                                                       \-> Done (Rejected)
```
**Issue Workflow**
```
Inbox -> Discussion -> Prioritised -> Done
                    \-> Open for contributions
                    \-> Done
```
## FAQ

❓ **How can I see what is assigned to me?**
1. To view all open issues assigned to you in an org
  *   Go to this link when you are logged in: [https://github.com/issues/assigned?q=is%3Aopen+archived%3Afalse+org%3AORG-NAME](https://github.com/issues/assigned?q=is%3Aopen+archived%3Afalse+org%3AORG-NAME).


❓ **How much time will this take per week?**

I don’t know! We are trying this for the first time and we will learn together.

❓ **As an approver, how long do I have to review something?**

I am not currently setting any SLIs or SLOs. I ask that you please do your best
to triage your assigned PRs and issues at least once a week.

❓ **What if I don’t think I am qualified to review something?**

I ask that you try your hardest to review something.
However, if you can't, that is okay. There are some options:
1. Decide within your team who is qualified to review an reassign the task.
1. Reach out in our working group slack channel (#wg-service-management) and ask for
someone else to review it.
1. Reach out to your tech lead and ask them to assign someone else.

❓ **What if I want to review something that is assigned to someone else?**

Great! If they haven’t started on it, feel free to unassign them and assign yourself as a reviewer.

❓ **What about issues that are actually proposals?**

Proposals are issues that are created and tracked in order to facilitate
conversation amongst the community before a large chunk of work is started.
These will be tracked in a different project TBD.
The workflow for this project is not flushed out yet.
