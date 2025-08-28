# Meta
[meta]: #meta
- Name: Require AI Tooling Disclosures for Contributions
- Start Date: August 28, 2025
- Author(s): @gerg
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Update all appropriate Cloud Foundry Technical Community's contribution
guidelines to require reasonable disclosure of AI Tooling used for contributions.

## Problem

Inspired by [ghostty-org/ghostty#8289](https://github.com/ghostty-org/ghostty/pull/8289)

Modern AI coding assistants:
1. Allow generation of source code (and documentation, etc) faster than can be
   realistically reviewed by CFF Approvers and Reviewers
1. Do not currently generate code of sufficient quality to be merged without
   human review, especially when used by inexperienced practitioners (colloquially: "slop")

This puts an undue burden on CFF Approvers and Reviewers, especially if they
do not realize they are reviewing low-effort, AI-generated assets.

## Proposal

Update all appropriate Cloud Foundry Technical Community documents to require
reasonable disclosure of AI Tooling used for contributions. The exact means of
this disclosure will be left to Working Groups to implement. Examples of
reasonable disclosure could be: text in the PR description, text in commit
messages, and/or including the AI Tool as a co-author on commit messages.
