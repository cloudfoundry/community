# Common Stale Bot

## Problem

* Over the years, a lot of repo’s have accumulated a large number of unresolved issues and open PRs. For the working group to be efficient it would be good to know which issues still need attention and which ones can be closed.

## High Level Solution

* Provide a Foundation owned bot account which mark issues and PR’s as being stale after 14 days of inactivity.
* The same bot should close stale issues after being stale without further activity for 7 days.
* Using this bot should be opt-in for all working groups on a per area basis.

## Solution Details

* Use github actions build in [stale action](https://github.com/actions/stale), driven by the central [configuration file](link pending).

## FAQ

**My PR is still being worked on but keeps getting marked as stale by the git bot.**
Convert your PR into a draft so the bot can ignore it.
