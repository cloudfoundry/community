The Cloud Foundry Technical Oversight Committee (TOC) is responsible for cross-cutting
product and design decisions.

- [Charter](#charter)
- [Activities](#activities)
- [Meetings](#meetings)
- [Members](#members)
- [Elections](#elections)

## Charter

The CFF's Technical Oversight Committee (TOC) is responsible for the oversight, 
direction, and delivery of technical aspects of the Cloud Foundry projects and 
working groups.

The TOC is established by the CFF's Governing Board, who is responsible (amongst
other things) for establishing the responsibilities of the TOC, how it is formed 
and the policies it operates under. The Governing Board's definition of the TOC can 
be found in the [CFF's charter](../governing-board/charter.md).

## Activities

Activities of the TOC include:

- Defining, documenting, publishing, and maintaining the overall technical
  direction of the Cloud Foundry Foundation's open-source projects.

- Holding regular public meetings of the TOC to discuss topics currently under
  consideration in the community, with meeting notes to be recorded and
  published for community review and commentary. In order to prevent
  vandalism, the TOC may require that making comments on the notes requires
  authentication.

- Creating, reviewing, approving, and publishing technical project governance
  documents.

- Creating proposals to direct working groups towards project-wide objectives.

- Reviewing, addressing, and commenting on project issues.

- Providing advice on technical questions or designs arising in the working
  groups.

## Meetings

The TOC will determine a schedule for regular meetings. It may also hold ad-hoc
meetings at the request of two or more members of the TOC.

Community members are encouraged to suggest topics for discussion ahead of the
TOC meetings, and are invited to observe these meetings and engage with the TOC
during the community feedback period at the end of each meeting.

| Artifact                   | Link                                                                                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Meeting Schedule | Tuesdays from 10:30 to 11:30 am ET <br>[CF Community Calendar](https://www.cloudfoundry.org/community-calendar/)                                                                                                                     |
| Meeting Video Chat       | See the coordinates section of the [meeting notes](https://docs.google.com/document/d/1qGrDBWBrO8_FrPXmosKD9fa67NPtT4p5NhHKN8ideY0/edit#heading=h.dlm4q8auhcx4)                                                                                                                     |
| Meeting Notes              | [CFF TOC meeting notes](https://docs.google.com/document/d/1qGrDBWBrO8_FrPXmosKD9fa67NPtT4p5NhHKN8ideY0/edit)                                                                                                                                                |

## Members

The members of the TOC are shown below. Membership in the TOC is determined by
the Cloud Foundry community via an election.

| &nbsp;                                                       | Member                 | Company     | Profile                                          | Term Start | Term End |
| ------------------------------------------------------------ | -----------------------| ----------- | ------------------------------------------------ | ---------- | --------
| <img width="30px" src="https://github.com/beyhan.png">       | Beyhan Veli (TOC Chair)| SAP         | [@beyhan](https://github.com/beyhan)             | 2022-06-22 | 2024     |
| <img width="30px" src="https://github.com/Cweibel.png">      | Chris Weibel           | Cloud.gov   | [@cweibel](https://github.com/cweibel)           | 2027-07-01 | 2027     |
| <img width="30px" src="https://github.com/gerg.png">         | Greg Cobb              | VMware      | [@gerg](https://github.com/Gerg)                 | 2025-07-01 | 2027     |
| <img width="30px" src="https://github.com/rkoster.png">      | Ruben Koster           | VMware      | [@rkoster](https://github.com/rkoster)           | 2022-06-22 | 2024     |
| <img width="30px" src="https://github.com/stephanme.png">    | Stephan Merker         | SAP         | [@stephanme](https://github.com/stephanme)       | 2023-06-21 | 2025     |


## Elections

The TOC is elected by the CFF's technical community, from amongst nominees who
have demonstrated technical leadership through sustained contributions to the CFF's
projects and technical working groups. The rules under which the TOC elections are run
can be found in the [CFF's charter](../governing-board/charter.md).

On behalf of the Cloud Foundry Foundation's Governing Board, foundation staff administers 
the elections based on the process defined in the project charter.

### Community Eligibility to Vote in TOC Elections

While the policy describing voter eligibility can be found in the CFF Charter, the topic
of voter eligibility is important enough to provide commentary on here.

The CFF is committed to an inclusive process for electing the TOC. Any member of the
technical community who has contributed to the project in the last year should 
have the ability to participate in the TOC election process. Contributions include, 
but are not limited to, opening PRs, reviewing and commenting on PRs, opening and 
commenting on issues, writing design docs, commenting on design docs, helping people 
(for example, on Slack), participating in mailing list discussions and participating in 
working groups. 

For the purpose of simplifying the election administration, an initial set of voters 
will be identified through automated reporting. Anyone who has at least 25 measurable
contributions in the last 12 months will be automatically added to the eligible voter 
list.

If a community member has contributed over the past year but is not captured in automated
reporting, they will be able to submit an eligibility form to the current TOC who will 
then determine whether this member will be eligible. In a case where the 
TOC declines an eligibility request, the requestor may appeal that decision
to the Governing Board.

For the election in year `YEAR`, all eligible voters will be listed at
`elections/YEAR/voters.md` in this repository, and the voters' guide will be
available at `elections/YEAR/README.md`.

The TOC may propose changes to future eligibility requirements, subject to Governing Board
approval, based on community feedback.

---

The initial content of this page is from the work of the [Knative community](https://github.com/knative/community)
under the terms of the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).

```yaml
name: Technical Oversight Committee
execution_leads:
- name: Beyhan Veli
  github: beyhan
- name: Chris Weibel
  github: cweibel
- name: Greg Cobb
  github: Gerg
- name: Ruben Koster
  github: rkoster
- name: Stephan Merker
  github: stephanme
technical_leads:
- name: Chris Clark
  github: christopherclark
- name: Ram Iyengar
  github: ramiyengar
- name: The Linux Foundation
  github: thelinuxfoundation
bots: []
areas:
- name: CloudFoundry Community
  approvers: []
  repositories:
  - cloudfoundry/community
config:
  github_project_sync:
    mapping:
      cloudfoundry: 31
```
