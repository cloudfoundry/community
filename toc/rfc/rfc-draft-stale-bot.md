# Meta
[meta]: #meta
- Name: Bot for closing stale issues in repos within the CF Foundation managed repo's
- Start Date: 2022-03-15
- Author(s): @rkoster
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: 


## Summary

Setup common stale bot for working groups to use for closing out issues / pull request which have gone stale.

## Problem

Over the years, a lot of repo’s have accumulated a large number of unresolved issues and open PRs. For the working group to be efficient it would be good to know which issues still need attention and which ones can be closed.

## Proposal

Provide a Foundation owned bot account which mark issues and PR’s as being stale after 14 days of inactivity. The same bot should close stale issues after being stale without further activity for 7 days. Using this bot should be opt-in for all working groups on a per area basis.

Use github actions build in [stale action](https://github.com/actions/stale), driven a central per wrokgroup configuration file.

