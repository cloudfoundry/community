# Meta
[meta]: #meta
- Name: Standardizing Github Teams and Access
- Start Date: 2022-02-28
- Author(s): @ameowlia
- Status: Accepted
- RFC Pull Request: [community#170](https://github.com/cloudfoundry/community/pull/170)


## Summary

All working groups SHOULD create GitHub teams using the standardized name format.

## Problem

CFF technical governance has changed to be organized around working groups and
new roles like Tech Lead and Approver. Most working groups also have sub-groups.

We need ways within the community to:
* Provide the team members with proper push access to certain repos,
* Provide a way for others to tag groups of people.

## Proposal

Every working group SHOULD make GitHub teams within the `cloudfoundry` org to reflect the following groups.

| Name of Team  | Team Membership  | Permissions  |
|---|---|---|
| toc | Technical Oversight Committee | Admin access to everything |
| wg-leads | Tech and Execution Leads for all WGs | Write access to community repo |
| wg-[WORKING-GROUP-NAME] | All approvers and leads for a WG | None: only for organization and tagging |
| wg-[WORKING-GROUP-NAME]-leads | All leads for a WG | Admin access for all WG repos |
| wg-[WORKING-GROUP-NAME]-[AREA-NAME]-approvers | Approvers & tech leads for an area within a WG | Write access for all repos in the area |
| wg-[WORKING-GROUP-NAME]-bots | Bot accounts for a WG | Write access for all WG repos |

Where: 
* `WORKING-GROUP-NAME` is the name of the Working Group, converted to kebab case,
* `AREA-NAME` is the name of the area, also converted to kebab case, or a suitable short name that identifies it clearly and uniquely within the Working Group.
