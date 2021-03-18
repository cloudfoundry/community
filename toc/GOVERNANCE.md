# CFF “Open Governance” Model Proposal (rough strawman)

Initial design inspired by the [Istio](https://github.com/istio/community) and [Knative](https://github.com/knative/community) communities.

# Technical Oversight Committee (TOC)

* Makes technical/architectural/direction decisions
* Resolve disagreements and escalations
* Approves new Working Groups
* Maintains community health
* Membership by election. Individual membership (if someone leaves company, the seat goes with them).
* Requirement for election: approver in a WG
* Requirement for voting: contributor to the project
* Max per-company representation
* Public weekly meeting, public backlog

# Working Groups

* Sponsored by TOC for major areas, e.g. scheduling, logging etc
* Roughly equivalent to projects today
* Some may be focused on one area, some may be cross-cutting
* Should have a charter (mission, goals, scope etc)
* Should maintain a Roadmap
* Anyone can join the WG
* Weekly meetings, slack channel etc
* All work in the open
* Leadership, N (1-3ish)  Leads appointed as below 
* Generally, WG should make decisions by consensus, but the leads are ultimately responsible
* Create subgroups as needed (e.g. could create a team to focus on a specific, time-bound deliverable, potentially that team may work in a tracker/pairing model) - no formal model for these
* If consensus not reached Leads generally make decision, but can escalate to TOC

*Note:* the working group does _not_ privilege pairing or tracker by default. (It may split out a subgroup to work on a task or deliverable in a pairing model which is then adopted on completion by the WG, or becomes its own WG). In general the WGs default to open, so both pairing and non-pairing contributions are the same. Of course, members of the WG may choose to pair, and the WG may choose to have a daily (open) standup, and to practice TDD, but there’s not a magic different backlog for people pairing, and pairing does *not* skip the need for an /approve (tho 1 of the pair may be an approver). Contentious decisions should trigger a conversation on a github issue etc, they should _not_ be resolved by an offline conversation with a PM that doesn’t end up back on the issue.

# Working Group Roles
Modelled after https://github.com/knative/community/blob/master/ROLES.md

* Member: 
  * Actively contributing
  * Has power to lgtm PRs (requirement to merge: 1 lgtm, 1 approve)
* Approver/Maintainer (of a part of the code): roughly
  * Regular contribution to that area
  * Member of project for 3 months
  * Reviewed at least 30 PRs in relevant area
  * Nominated by Lead, not veto-ed by another lead
  * Can approve and merge PRs
  * Has power to approve PRs (requirement to merge: 1 lgtm, 1 approve)
* Lead (of a WG): roughly
  * Regular contribution
  * Member 6 months
  * Significant contributions to/expertise in the area (can be code, PMing, Scribe etc)
  * Sponsored by TOC
  * Can potentially be split in to Execution Lead and Tech Lead.
  * Has power to approve PRs (requirement to merge: 1 lgtm, 1 approve)
  * A WG has 1-3ish leads, generally.

# Decision Making

* Regular meetings in each WG
* Regular open TOC meeting, each week a WG presents to the TOC
  * Slides include “wins, losses”, “plans for next release”, “on track for approver/lead” etc
* Public backlog for TOC, WGs
* Decisions generally happen as low as possible. WGs report progress to TOC, TOC has ability to create new WGs/merge/change WGs, with Steering approval.
* Escalations can happen as needed
