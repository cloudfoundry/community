# Meta
[meta]: #meta
- Name: Deprecated Metrics Agent
- Start Date: 2023-09-12
- Author(s): @mkocher @rroberts2222
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

Metrics Agent was added as a way to egress metrics by serving a prometheus
endpoint of metrics sent to the forwarder agent. We don't know of any users,
and the functionality can now be accomplished using the prometheus exporter of
OpenTelemetry Collector.

## Problem

We are maintaining code that no one is using and has a viable alternative.

## Proposal

- Today - Mark [metrics-discovery-release](https://github.com/cloudfoundry/metrics-discovery-release) repo as deprecated
- In One Month - Remove metrics agent from cf-deployment
- Accept a PR to move metrics-agent to an ops file in CF-deployment, if a community member needs Metrics Agent and would like a ops file.
- In Three Months - Stop cutting new releases of metrics agent


