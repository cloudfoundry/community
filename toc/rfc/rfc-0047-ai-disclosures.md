# Meta
[meta]: #meta
- Name: Require AI Tooling Disclosures for Contributions
- Start Date: August 28, 2025
- Author(s): @gerg
- Status: Accepted
- RFC Pull Request: [community#1297](https://github.com/cloudfoundry/community/pull/1297)


## Summary

Update all appropriate Cloud Foundry Technical Community's contribution
guidelines to require reasonable disclosure of AI Tooling used for contributions.

## Problem

Inspired by [ghostty-org/ghostty#8289](https://github.com/ghostty-org/ghostty/pull/8289)

Modern AI tools:
1. Allow generation of source code (and documentation, etc) faster than can be
   realistically reviewed by CFF Approvers and Reviewers
1. Do not currently generate code of sufficient quality to be merged without
   human review, especially when used by inexperienced or malicious practitioners

This puts an undue burden on CFF Approvers and Reviewers, especially if they
do not realize they are reviewing low-effort, AI-generated contributions.

Though human-generated contributions can also be low-quality, the cost of
manually generating reasonable-looking contributions is substantially higher
than is now possible with AI. This creates a denial-of-service vector, where
the effort to generate low-quality contributions is substantially lower than
the effort to process (review) them.

## Proposal

The goal of this RFC is to implement a light-weight policy to shield Approvers
and Reviewers, while not impeding the responsible use of AI tools.

Update all appropriate Cloud Foundry Technical Community documents to require
reasonable disclosure of AI Tooling used for contributions. The exact means of
this disclosure will be left to Working Groups to implement. Examples of
reasonable disclosure could be: text in the PR description, text in commit
messages, and/or including the AI Tool as a co-author on commit messages.

Working groups may implement exceptions to this policy, for example to allow
Approvers and Reviewers to use AI tooling without disclosure.
