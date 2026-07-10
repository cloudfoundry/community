# Meta
[meta]: #meta
- Name: Archive the CF on K8S working group
- Start Date: 2026-07-10
- Author(s): @georgethebeatle @danail-branekov
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1560
- Related RFCs:
- Affected Component(s): Korifi



## Summary

Archive the `CF on K8S` working group

## Problem

In the past couple of months we have been observing diminishing community interest in the [Korifi](https://github.com/cloudfoundry/korifi) project:
- No communication on the slack channel
- No attendees on community meetings
- No new issues, PRs or feature requests being raised
- We are not aware of any productive deployments or plans of such ones in future

Korifi maintainers (currently three SAP employees) no longer have the capacity to continue maintaining the project. Therefore, unless someone else is willing to take over, the `CF on K8S` working group does not make sense any more.

## Proposal

On accepting the RFC (after public discussion and final comment period):

- Introduce an archival notice and archive Korifi github repositories:
  - https://github.com/cloudfoundry/korifi
  - https://github.com/cloudfoundry/korifi-ci
  - https://github.com/cloudfoundry/intro-to-korifi
  - https://github.com/cloudfoundry/korifi-website
  - https://github.com/cloudfoundry/korifi-sample-app
- Delete the [CF-on-K8s-WG GCP project](https://console.cloud.google.com/welcome?project=cf-on-k8s-wg)
- Delete the `CFF-korifi` AWS account (accountID: `007801690126`)
- Delete the [`CF-on-K8S` working group](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/cf-on-k8s.md)

## Alternatives

The [`kind-deployment`](https://github.com/cloudfoundry/kind-deployment) project provides a simple and fast way to run Cloud Foundry on a local kind cluster. While it currently focuses on quick and cheap local CF API setup, covering one of the Korifi use cases, its long-term vision, as outlined in the [cf-on-kind RFC](https://github.com/cloudfoundry/community/blob/35ddcbb326f4cc7e41f8dba2cef027928b334f81/toc/rfc/rfc-0049-cf-on-kind.md?plain=1#L38-L44), is to support real Kubernetes clusters.
