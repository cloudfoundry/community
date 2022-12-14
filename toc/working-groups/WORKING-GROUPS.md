Most community activity is organized into _working groups_.

Working groups follow the [contributing](../../CONTRIBUTING.md) guidelines although
each of these groups may operate a little differently depending on their needs
and workflow.

When the need arises, a new working group can be created or an existing one can be dissolved. There is no process
around this at the moment and would fall back to a general decision by the TOC to accept or remove a proposed charter document for a WG.
In the case of a WG getting dissolved, the TOC and the remaining WGs would have to decide which repos owned by the WG would go to other WGs and which would be archived or transferred to TOC or to administrative control.

Additionally, all working groups should hold regular meetings, which should be
added to the
[shared CFF calendar](https://calendar.google.com/calendar/u/0/embed?src=cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78@group.calendar.google.com)
WG leads should have access to be able to create and update events on this
calendar, and should invite cf-dev@lists.cloudfoundry.org to working group
meetings. The meetings will be recorded and the recordings will be available in the [Cloud Foundry YouTube channel](https://www.youtube.com/@CloudFoundryFoundation). Please check the different [playlists](https://www.youtube.com/@CloudFoundryFoundation/playlists) available per WG in the YouTube channel.

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

- App Runtime Deployments
- App Runtime Interfaces
- App Runtime Platform
- CF on K8s
- Foundational Infrastructure
- Paketo
- Service Management
- Vulnerability Management


## App Runtime Deployments

Mission: Provide reference deployments of the CF App Runtime to CF community end users, CF community contributors, and CF commercial vendors.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-app-runtime-deployments` topic.

| Artifact                   | Link |
| -------------------------- | -- |
| Charter                    | [app-runtime-deployments.md](./app-runtime-deployments.md) |
| Forum                      | [Video chat](https://zoom.us/j/97528090021?pwd=TWU4c0NEMlRvUVAxMjRwMGtpSUhTQT09) |
| Community Meeting Calendar | [Monthly on the second Thursday at 4:30pm – 5:30pm UTC](https://calendar.google.com/event?action=TEMPLATE&tmeid=MHBqNGxmM24xbmE4NmE3MjBmbzUzN2xxbHFfMjAyMjA1MTJUMTYzMDAwWiBjbG91ZGZvdW5kcnkub3JnX29lZGIwaWxvdGc1dWRzcGRsdjMyYTV2Yzc4QGc&tmsrc=cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78%40group.calendar.google.com&scp=ALL) / [Monthly on the fourth Thursday at 4:30pm - 5:30pm UTC](https://calendar.google.com/event?action=TEMPLATE&tmeid=N2loZWdqb3VnOWhjcjVybWs5bGg2bzEydHNfMjAyMjA1MjZUMTUzMDAwWiBjbG91ZGZvdW5kcnkub3JnX29lZGIwaWxvdGc1dWRzcGRsdjMyYTV2Yzc4QGc&tmsrc=cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78%40group.calendar.google.com&scp=ALL) |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1lBOSKMWYb1y2d0YcUmIHe0JX7lc5qcLFO6sa-gp9N_g) |
| Slack Channel              | [&#x23;wg-app-runtime-deployments](https://cloudfoundry.slack.com/archives/C033ALST37V) |

| &nbsp;                                                   | Leads            | Company | Profile                                  |
| -------------------------------------------------------- | ---------------- | ------- | ---------------------------------------- |
| <img width="30px" src="https://github.com/jochenehret.png"> | Jochen Ehret | SAP | [@jochenehret](https://github.com/jochenehret) |


## App Runtime Interfaces

Mission: To provide APIs for the CF App Runtime and community clients for end users.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-app-runtime-interfaces` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [app-runtime-interfaces.md](./app-runtime-interfaces.md)  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channel              | [&#x23;wg-app-runtime-interfaces](https://cloudfoundry.slack.com/archives/C02LR0XCV3M)  |

| &nbsp;                                                   | Leads            | Company | Profile                                  |
| -------------------------------------------------------- | ---------------- | ------- | ---------------------------------------- |
| <img width="30px" src="https://github.com/Gerg.png"> | Greg Cobb     | VMware  | [@Gerg](https://github.com/Gerg) |


## App Runtime Platform

Mission: To provide operational components for the CF App Runtime, including those for application build, application execution, ingress and app-to-app routing, and aggregation of application logs and metrics.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-app-runtime-platform` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [app-runtime-platform.md](./app-runtime-platform.md)  |
| Forum                      | [Video chat](https://zoom.us/j/96811724570?pwd=akxYdzlPQVJZMU9ySDVKSThNTUI4dz09) |
| Community Meeting Calendar | [Monthly on the first Wednesday at noon ET / 9 am PT](https://calendar.google.com/event?action=TEMPLATE&tmeid=bnBmZTMzMzYyNGlxY3U5ODR2ZHFtZ2kyZDRfMjAyMTExMDNUMTYwMDAwWiBjbG91ZGZvdW5kcnkub3JnX29lZGIwaWxvdGc1dWRzcGRsdjMyYTV2Yzc4QGc&tmsrc=cloudfoundry.org_oedb0ilotg5udspdlv32a5vc78%40group.calendar.google.com&scp=ALL)  |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1aGT5P_1kFiDMqgvRgmryXMvjGRXKpmtexAhAGK0t3yc/edit)  |
| Slack Channel              | [&#x23;wg-app-runtime-platform](https://cloudfoundry.slack.com/archives/C02HNDJB31R)  |

| &nbsp;                                                   | Leads            | Company | Profile                                  |
| -------------------------------------------------------- | ---------------- | ------- | ---------------------------------------- |
| <img width="30px" src="https://github.com/ameowlia.png"> | Amelia Downs     | VMware  | [@ameowlia](https://github.com/ameowlia) |



## CF on K8s

Mission: To bring the ease and simplicity of the Cloud Foundry developer experience to Kubernetes.

The GitHub repos this WG manages in the `cloudfoundry` GitHub organization are to be labeled with the `cff-wg-cf-on-k8s` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [cf-on-k8s.md](./cf-on-k8s.md)  |
| Forum                      | [Video chat](https://zoom.us/j/98762513821?pwd=dUk1WGZwcXJqR0UxRXQ4NnljcCtydz09)  |
| Community Meeting Calendar | Every other Wednesday at 11:30 am ET / 8:30 am PT  |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1ULNBEjlrNAgn3ko9y8ZJfwI7mw5-oofYdjl-dhkEoDA/edit)  |
| Slack Channel              | [&#x23;korifi-dev](https://cloudfoundry.slack.com/archives/C0297673ASK) |

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
| Forum                      | [Video chat](https://zoom.us/j/92400700135?pwd=MTZONUlRdGQxTmMveDVlMVYvRTFIZz09)  |
| Community Meeting Calendar | Weekly on Thursdays at 10:30 am ET / 7:30 am PT  |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1pLKTANki82JsCqPr4DE8vu4je_omA20eH96CUuRW_8Q)  |
| Slack Channels              | [&#x23;bosh](https://cloudfoundry.slack.com/archives/C02HPPYQ2) &middot; [&#x23;credhub](https://cloudfoundry.slack.com/archives/C3EN0BFC0) &middot; [&#x23;uaa](https://cloudfoundry.slack.com/archives/C03FXANBV) &middot; [&#x23;mysql-galera](https://cloudfoundry.slack.com/archives/C7NDVQ55Z) &middot; [&#x23;postgres-release](https://cloudfoundry.slack.com/archives/C3CR3GC1F) |

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
| <img width="30px" src="https://github.com/dmikusa.png"> | Daniel Mikusa       | VMware  | [@dmikusa](https://github.com/dmikusa) |
| <img width="30px" src="https://github.com/ekcasey.png"> | Emily Casey       | VMware  | [@ekcasey](https://github.com/ekcasey) |
| <img width="30px" src="https://github.com/ryanmoran.png"> | Ryan Moran       | VMware  | [@ryanmoran](https://github.com/ryanmoran) |


## Service Management

Mission: Provides interfaces for service lifecycle within application platforms and adapters to common external service providers.

The GitHub repos this WG manages in the `cloudfoundry` and `cloudfoundry-incubator` GitHub organization are to be labeled with the `cff-wg-service-manangement` topic.

| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [service-management.md](./service-management.md)  |
| Forum                      | [Video chat](https://zoom.us/j/96135973215?pwd=NzQrRk1tbXlTQnZEVmRNZlluSm50QT09)  |
| Community Meeting Calendar | Monthly on the first Tuesday at 10:30 UK / 11:30 CET/ 16 IST / Monthly on the second Tuesday at 11:30 ET/ 16:30 UK |
| Meeting Notes              | [Google Doc](https://docs.google.com/document/d/1pVepAY0IxA9zz6imyMNnZeCM_mUkxzk1Dd1PDClmkWE/view)  |
| Slack Channels             | [&#x23;wg-service-management](https://cloudfoundry.slack.com/archives/C02TXDMPSUS)|

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/pivotal-marcela-campo.png"> | Marcela Campo       | VMWare  | [@pivotal-marcela-campo](https://github.com/pivotal-marcela-campo) |


## Vulnerability Management

Mission: Provides discreet management of security vulnerabilities issues relevant for active CF projects.


| Artifact                   | Link |
| -------------------------- | ---- |
| Charter                    | [vulnerability-management.md](./vulnerability-management.md)  |
| Forum                      | TBD  |
| Community Meeting Calendar | TBD  |
| Meeting Notes              | TBD  |
| Slack Channels             | [&#x23;security](https://cloudfoundry.slack.com/archives/C0DEQSW9W)|

| &nbsp;                                                   | Leads            | Company | Profile                                 |
| -------------------------------------------------------- | ---------------- | ------- | --------------------------------------- |
| <img width="30px" src="https://github.com/paulcwarren.png"> | Paul Warren       | VMWare  | [@paulcwarren](https://github.com/paulcwarren) |

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

