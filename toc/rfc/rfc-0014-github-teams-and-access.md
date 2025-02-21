# Meta
[meta]: #meta
- Name: Standardizing Github Teams and Access
- Start Date: 2022-07-28
- Author(s): @ameowlia, @stephanme
- Status: Accepted
- RFC Pull Request: [community#375](https://github.com/cloudfoundry/community/pull/375)


## Summary

All working groups SHOULD create GitHub teams using the standardized name
format.

Supersedes [rfc-0005-github-teams-and-access](https://github.com/cloudfoundry/community/blob/main/toc/rfc/archived/rfc-0005-github-teams-and-access.md)

## Problem

CFF technical governance has changed to be organized around working groups and
new roles like Tech Lead and Approver. Most working groups also have sub-groups.

We need ways within the community to:
* Provide the team members with proper push access to certain repos,
* Provide a way for others to tag groups of people.

## Proposal

Every working group SHOULD use GitHub teams within the necessary CFF Managed
Github Org to reflect the following groups. The GitHub teams SHOULD be
provisioned automatically from the yaml blocks in the working group charters.

| Name of Team  | Team Membership  | Permissions  |
|---|---|---|
| toc | Technical Oversight Committee | Admin access to everything |
| wg-leads | Tech and Execution Leads for all WGs | Write access to community repo |
| wg-[WORKING-GROUP-NAME] | All approvers and leads for a WG | None: only for organization and tagging |
| wg-[WORKING-GROUP-NAME]-leads | All leads for a WG | Admin access for all WG repos |
| wg-[WORKING-GROUP-NAME]-bots | Bot accounts for a WG | Write access for all WG repos |
| wg-[WORKING-GROUP-NAME]-[AREA-NAME]-approvers | Approvers & tech leads for an area within a WG | Write access for all repos in the area |
| wg-[WORKING-GROUP-NAME]-[AREA-NAME]-reviewers | Contributors who want to become approver for an area within a WG | Read access for all repos in the area, so that PRs can be assigned for review |
| wg-[WORKING-GROUP-NAME]-[AREA-NAME]-bots | Bot accounts for an area within a WG | Write access for all repos in the area |

Where: 
* `WORKING-GROUP-NAME` is the name of the Working Group, converted to kebab
  case,
* `AREA-NAME` is the name of the area, also converted to kebab case, or a
  suitable short name that identifies it clearly and uniquely within the
  Working Group.
