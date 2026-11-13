# Meta
[meta]: #meta
- Name: Define Criteria and Process to Deprecate Inactive Accepted RFCs
- Start Date: 2026-11-13
- Author(s): @beyhan
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs:
- Affected Component(s): Cloud Foundry Community RFC Process



## Summary

Define criteria for identifying accepted RFCs that are no longer being actively worked on, and establish a process to deprecate and archive them. This keeps the set of active accepted RFCs an accurate reflection of the community's current intentions and ongoing work.

## Problem

Accepted RFCs that define action plans may remain in the accepted state indefinitely even when no one is actively working on them. This creates several problems:

- It is unclear to community members whether an accepted RFC represents ongoing work or a silently abandoned intention.
- The list of accepted RFCs does not accurately reflect what the community is actually doing.
- Contributors who might want to pick up abandoned work have no signal that the RFC needs a new owner.

This RFC does not address RFCs that define **Standards** or **Processes**, as those remain active by definition until explicitly superseded by a new RFC.

## Proposal

### Scope

This process applies only to accepted RFCs whose outcome is an **Action Plan** — that is, RFCs that describe a concrete set of actions the community agreed to carry out. It does not apply to RFCs that define a Standard or a Process, which MUST continue to follow the existing supersede path described in the RFC README.

### Criteria for Inactivity

An accepted action-plan RFC is considered inactive if all of the following are true for the past **12 months**:

- No pull request updating the RFC has been merged or is open.
- No linked issue or tracking item shows active progress.
- No community member has publicly claimed ownership of the work (e.g., via Slack, a GitHub comment, or a PR).

### Deprecation Process

1. Any community member, Working Group lead, or TOC member MAY open a pull request (PR) that:
   - Changes the RFC's `Status` field to `Deprecated`.
   - Moves the RFC file (and any associated image directory) into the `toc/rfc/archived/` directory using `git mv`.
   - Includes a brief comment in the PR explaining the inactivity criteria that were met.

2. The PR description MUST mention `@cloudfoundry/toc` and the leads of any relevant Working Groups to raise awareness.

3. A **notice period of 2 weeks** applies from the time the PR is opened. During this period:
   - The original RFC authors and any interested community members MAY step up to claim active ownership of the work by commenting on the PR.
   - If someone credibly commits to resuming work on the RFC (e.g., by opening a follow-up PR or issue within the notice period), the deprecation PR MUST be closed.

4. After the notice period, if no one has claimed ownership, a TOC member or the PR author MAY merge the deprecation PR.

### Revival of a Deprecated RFC

A deprecated RFC MAY be revived at any time by creating a new RFC that:

- References the deprecated RFC.
- Picks up or updates the original action plan.

The new RFC follows the standard RFC process from the beginning.

### Summary of Status Values

| Status | Meaning |
|---|---|
| Accepted | The RFC's action plan is agreed upon and considered active. |
| Deprecated | The RFC's action plan was accepted but is no longer being actively pursued. Archived for historical reference. |
