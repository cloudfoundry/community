Most community activity is organized into _working groups_.

Working groups follow the [contributing](../CONTRIBUTING.md) guidelines although
each of these groups may operate a little differently depending on their needs
and workflow.

When the need arises, a new working group can be created. See the
[working group processes](../mechanics/WORKING-GROUP-PROCESSES.md) for working
group proposal and creation procedures.

Additionally, all working groups should hold regular meetings, which should be
added to the
[shared CFF calendar](https://calendar.google.com/calendar/u/0/embed?src=cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78@group.calendar.google.com)
WG leads should have access to be able to create and update events on this
calendar, and should invite cf-dev@lists.cloudfoundry.org to working group
meetings.

### Calendar import

If you're using Google Calendar, the above should work. If you're using some
other system (Apple Calendar or Outlook, for example),
[here is an iCal export of the community calendar](https://calendar.google.com/calendar/ical/cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78@group.calendar.google.com/public/basic.ics).

- [Follow these directions to import into Outlook Web](https://support.office.com/en-us/article/import-or-subscribe-to-a-calendar-in-outlook-on-the-web-503ffaf6-7b86-44fe-8dd6-8099d95f38df)
- [Follow these directions for desktop Outlook](https://support.office.com/en-us/article/See-your-Google-Calendar-in-Outlook-C1DAB514-0AD4-4811-824A-7D02C5E77126)
- [Follow the import directions to import into Apple Calendar](https://support.apple.com/guide/calendar/import-or-export-calendars-icl1023/mac)

# Conventions for Working Group repository management

Most working groups manage a subset of repositories in the `cloudfoundry` GitHub organization, among other technical assets. To provide visibility into which working groups manage which repositories, each working group shall add `cff-wg-<wg-name>` as a topic to each repository it manages in this organization, where `<wg-name>` is the name of the working group converted to [kebab-case](https://en.wikipedia.org/wiki/Kebab_case).


# Working Groups

The current working groups are:

- App Runtime Platform
- CF on K8s
- Foundational Infrastructure
- Paketo


## App Runtime Platform

Mission: To provide operational components for the CF App Runtime, including those for application build, application execution, ingress and app-to-app routing, and aggregation of application logs and metrics.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-app-runtime-platform` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [app-runtime-platform.md](./app-runtime-platform.md)  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channel              | TBD  |

| &nbsp;                                                   | Leads            | Company | Profile                                  |
| -------------------------------------------------------- | ---------------- | ------- | ---------------------------------------- |
| <img width="30px" src="https://github.com/ameowlia.png"> | Amelia Downs     | VMware  | [@ameowlia](https://github.com/ameowlia) |



## CF on K8s

Mission: To bring the ease and simplicity of the Cloud Foundry developer experience to Kubernetes.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-cf-on-k8s` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [cf-on-k8s.md](./cf-on-k8s.md)  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channel              | TBD  |

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/georgethebeatle.png"> | Georgi Sabev       | SAP  | [@georgethebeatle](https://github.com/georgethebeatle) |
| <img width="30px" src="https://github.com/gcapizzi.png"> | Giuseppe Capizzi       | VMware  | [@gcapizzi](https://github.com/gcapizzi) |


## Foundational Infrastructure

Mission: To provide infrastructure automation and core capabilities shared across CF projects, including identity management, credential management, and integrated data services.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-foundational-infrastructure` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [foundational-infrastructure.md](./foundational-infrastructure.md)  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channel              | TBD  |

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/beyhan.png"> | Beyhan Veli       | SAP  | [@beyhan](https://github.com/beyhan) |
| <img width="30px" src="https://github.com/rkoster.png"> | Ruben Koster       | VMware  | [@rkoster](https://github.com/rkoster) |


## Paketo

Mission: To provide cloud-native buildpacks for servers, languages, and frameworks popular with application developers.

This working group has no repositories in the `cloudfoundry` GitHub organization.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [paketo.md](./paketo.md)  |
| Forum                      | [Video chat](https://vmware.zoom.us/j/97458838615?pwd=djB0OTZyTXpNd2dQa0ZQb3V2UFVCQT09) |
| Community Meeting Calendar | Weekly on Tuesdays at 2 pm ET / 11 am PT  |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1V1jtZmjpivMsWdoYOrGlaK4exoIezn2r4Lf3XcPxduQ/view)  |
| Slack Channel              | [&#x23;general](https://paketobuildpacks.slack.com/archives/CU8RVQZ1R) in the [Paketo Slack Workspace](paketobuildpacks.slack.com) |

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/dmikusa-pivotal.png"> | Daniel Mikusa       | VMware  | [@dmikusa-pivotal](https://github.com/dmikusa-pivotal) |
| <img width="30px" src="https://github.com/ekcasey.png"> | Emily Casey       | VMware  | [@ekcasey](https://github.com/ekcasey) |
| <img width="30px" src="https://github.com/ryanmoran.png"> | Ryan Moran       | VMware  | [@ryanmoran](https://github.com/ryanmoran) |


<!--
## Working Group Template

Mission:

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-<wg-name-in-kebab-case>` topic.


| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | TBD  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channel              | TBD  |

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/<GitHub handle>.png"> | <name>       | <company>  | [@<GitHub handle>](https://github.com/<GitHub handle>) |

-->

