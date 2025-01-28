# Meta
[meta]: #meta
- Name: Managing Multiple Github Orgs
- Start Date: 2025-01-21
- Author(s): @ameowlia, @rkoster
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1050

## Summary

CFF community documentation and automation MUST be updated to be able to handle multiple
Github Orgs.

## Problem

Currently the documentation in the CFF community repo is written as if there is
only one Github Organization: cloudfoundry. However, there are currently two
Github Organizations that the CFF TOC oversees: cloudfoundry and paketo. In the
near future, we plan to add a third Github Organization: concourse.

We MUST update our documentation to reflect how we want to handle multiple Github organizations.

## Proposal

### New Definitions

* *CFF Github Orgs* - This includes ALL Github Organizations that the CFF TOC
  oversees. This currently includes: cloudfoundry and paketo. When we merge
  [the RFC to add
  concourse](https://github.com/cloudfoundry/community/pull/1047), then
  concourse will also be included in this list.

* *CFF Managed Github Orgs* - This includes all Github organizations that are
  managed via the CFF TOC automation. This currently only includes
  cloudfoundry.

### Rename `org` dir to `orgs`
Currently the directory
[org](https://github.com/cloudfoundry/community/tree/main/org) contains yaml
definitions for the repos and contributors to the cloudfoundry Github org. It
also contains the CFF TOC org management automation scripts. 

This SHOULD be the place where yaml definitions for all CFF Managed Github orgs
are stored. To reflect this, the name of the directory SHOULD be renamed to `orgs`.

### Rename `cloudfoundry.yml` to `orgs.yml`

Currently
[cloudfoundry.yml](https://github.com/cloudfoundry/community/blob/main/org/cloudfoundry.yml)
contains yaml defining all of the repos in the cloudfoundry Github org. It
already has a top level [`orgs`
key](https://github.com/cloudfoundry/community/blob/8c7298337a8515d7dfae058b3bd1f88ad0eeaf95/org/cloudfoundry.yml#L2).

All of the repos for all of CFF Managed Github Orgs SHOULD be in one place, and
the file `cloudfoundry.yml` SHOULD be the place for that. To reflect that this
file will contain information about multiple CFF Managed Github Orgs it SHOULD
be renamed `orgs.yml`.

### Update other docs to match
All other files that contain references to the cloudfoundry Github org as if it
is the only Github org MUST be updated.

This includes, but is not limited to the following files:
* https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0002-github-members.md
* https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0007-repository-ownership.md
* https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0014-github-teams-and-access.md
* https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md

### Update automation
The Github automation maintained by the TOC MUST be updated to work for multiple orgs.
