
# Meta
[meta]: #meta
- Name: TOC Administrative Access to CFF Infrastructure
- Start Date: 2026-01-27
- Author(s): @rkoster
- Status: Accepted
- RFC Pull Request: [community#1415](https://github.com/cloudfoundry/community/pull/1415)

## Summary

This RFC proposes granting all Technical Oversight Committee (TOC) members admin-level access to key Cloud Foundry Foundation (CFF) infrastructure systems, including Concourse instances, Docker Hub organizations, Cloudflare, and all IaaS accounts used by the CFF. The goal is to improve responsiveness and reduce operational bottlenecks.

## Problem

TOC members are responsible for the technical oversight of Cloud Foundry but currently lack the permissions required to assist engineers when issues arise within critical CFF-managed accounts. This creates delays—especially across time zones—when troubleshooting CI outages, image publishing failures, DNS/CDN issues, or IaaS‑level infrastructure problems. Access is currently limited to a few individuals, creating single points of failure.

## Proposal

TOC members SHOULD be granted full administrative access to:
- All CFF-managed Concourse CI instances  
- CFF Docker Hub organizations  
- The Cloudflare CFF account  
- All IaaS provider accounts used by the CFF
- CF community Slack workspace  

This access MUST be provisioned through existing secure authentication methods (e.g., SSO, MFA) and MUST remain auditable. When TOC membership changes, access MUST be updated immediately.

Providing TOC members with this level of access WILL enable timely support for engineering teams globally, reduce dependency on a small number of privileged account holders, and strengthen operational resilience.
