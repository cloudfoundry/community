The Cloud Foundry Technical Oversight Committee (TOC) is responsible for cross-cutting
product and design decisions.

- [Charter](#charter)
- [Composition](#composition)
- [Committee Mechanics](#committee-mechanics)
- [Committee Decision-Making](#committee-decision-making)
- [Committee Meeting](#committee-meeting)
- [Committee Members](#committee-members)
- [TOC Election Process](#election-process)

## Charter

- Technical Project Oversight, Direction & Delivery

  - Set the overall technical direction and roadmap of the project.

  - Resolve technical issues, technical disagreements and escalations within the
    project.

  - Set the priorities of individual releases to ensure coherency and proper
    sequencing.

  - Approve the creation and dissolution of working groups and approve
    leadership changes of working groups.

  - Create proposals based on TOC discussions and bring them to the relevant
    working groups for discussion.

  - Approve the creation/deletion of GitHub repositories, along with other
    high-level administrative issues around GitHub and our other tools.

- Happy Healthy Community

  - Establish and maintain the overall technical governance guidelines for the
    project.

  - Decide which sub-projects are part of the Cloud Foundry project, including
    accepting new sub-projects and pruning existing sub-projects to maintain
    community focus

  - Ensure the team adheres to our
    [code of conduct](./CONTRIBUTING.md#code-of-conduct) and respects our
    [values](./VALUES.md).

  - Foster an environment for a healthy and happy community of developers and
    contributors.

## Composition

The TOC will have five seats, with a maximum of 2 seats being held by employees
from the same vendor.

There will be an annual election to determine the composition of the TOC for the
following year. Three seats will be up for election in one year and two will be
up for election the following year.

## Committee Mechanics

The TOC’s work includes:

- Regular committee meetings to discuss hot topics, resulting in a set of
  published
  [meeting notes](https://docs.google.com/document/d/1hR5ijJQjz65QkLrgEhWjv3Q86tWVxYj_9xdhQ6Y5D8Q/edit#).

- Create, review, approve and publish technical project governance documents.

- Create proposals for consideration by individual working groups to help steer
  their work towards a common project-wide objective.

- Review/address/comment on project issues.

- Act as a high-level sounding board for technical questions or designs bubbled
  up by the working groups.

## Committee Decision-Making

The TOC should strive to reach consensus on decisions when possible. Any
decision requires a quorum of the TOC, defined as the presence of a simple
majority (greater than 50%) of the current TOC members.

If a TOC member sustains an objection to a proposed decision, any member of
the TOC may call the decision to a vote. Each member of the TOC is entitled to
one vote in any voting matter. A simple majority (greater than 50%) of all
members of the TOC must vote to approve the decision for it to be accepted.

The TOC shall record calls to vote and decisions voted upon, including the
individual votes of the TOC members, in the regularly published TOC meeting
notes.

## Committee Meeting

The TOC will determine a schedule for regular meetings. It may also hold ad-hoc
meetings at the request of two or more members of the TOC.

Community members are encouraged to suggest topics for discussion ahead of the
TOC meetings, and are invited to observe these meetings and engage with the TOC
during the community feedback period at the end of each meeting.

| Artifact                   | Link                                                                                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Google Group               | [cf-toc@lists.cloudfoundry.org](https://lists.cloudfoundry.org//g/cf-toc)                                                                                |
| Community Meeting VC       | See the top of the [Meeting notes]()                                                                                                                     |
| Community Meeting Calendar | Xdays at XX:XXa-XXp <br>[Calendar]()                                                                                                                     |
| Meeting Notes              | [Notes]()                                                                                                                                                |
| Document Folder            | [Folder]()                                                                                                                                               |

## Chair

The TOC will select a chair from amongst the TOC members.

The TOC Chair is responsible for:
* Chairing meetings of the TOC
* Coordinating meeting agendas, based on feedback from the community and other TOC members
* Representing the technical community on the CFF board

## Committee Members

The members of the TOC are shown below. Membership in the TOC is determined by
the Cloud Foundry community via an election.

| &nbsp;                                                         | Member         | Company | Profile                                              |
| -------------------------------------------------------------- | -------------- | ------- | ---------------------------------------------------- |
| GH picture        | name     | employer  | profile               |

## Election Process

### Candidate Eligibility

Current TOC members and
[Approvers](https://github.com/cloudfoundry/community/blob/master/ROLES.md#approver)
with at least 3 months tenure are eligible to stand for election. Candidates may
self-nominate or be nominated by another eligible member.

### Voter Eligibility

Contributions are defined as opening PRs, reviewing
and commenting on PRs, opening and commenting on issues, writing design docs,
commenting on design docs, helping people on slack, participating in working
groups, helping people on  and etc. Anyone who has at least 50 contributions in the last 12 months is eligible to
vote in the TOC election. 

[This dashboard][1]
shows only GitHub based contributions and does not capture all the contributions
we value. **We expect this metric not to capture everyone who should be eligible
to vote.** If a community member has had significant contributions over the past
year but is not captured in the lfanalytics.io dashboard, they will be able
to submit an exception form to the steering committee who will then review and
determine whether this member should be marked as an exception.

All eligible voters will be captured at
`cloudfoundry/community/elections/$YEAR/voters.md` and the voters’ guide
will be captured at `cloudfoundry/community/elections/$YEAR/README.md`
similar to the kubernetes election process.

We are committed to an inclusive process and the TOC will have the right to
adjust future eligibility requirements based on community feedback.

### Election Method and Tools

Elections will be held using a time-limited
[Condorcet](https://en.wikipedia.org/wiki/Condorcet_method) ranking on
[CIVS](http://civs.cs.cornell.edu/) using the
[Schulze](https://en.wikipedia.org/wiki/Schulze_method) method. The top
vote-getters will be elected to the open seats. This is the same process used by
the Kubernetes project.

### Election Administration

On behalf of the Cloud Foundry Foundation's Board of Directors, foundation staff will 
administer the election based on the process outlined above.

---

The initial content of this page is from the work of the [KNative community](https://github.com/knative/community)
under the terms of the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).

[1]: https://lfanalytics.io/projects/cloud-foundry%2Fcloud-foundry/active-contributor?time=%7B%22from%22:%22now-1y%22,%22type%22:%22datemath%22,%22to%22:%22now%22%7D
