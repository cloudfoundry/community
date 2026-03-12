# Meta
[meta]: #meta
- Name: Usage Snapshots for App and Service Usage Baselines
- Start Date: 2026-03-12
- Author(s): @joyvuu-dave
- Status: Draft
- RFC Pull Request: [community#1449](https://github.com/cloudfoundry/community/pull/1449)


## Summary

This RFC proposes new V3 API endpoints for capturing point-in-time usage snapshots of all running app processes and service instances. Snapshots provide a non-destructive way for billing consumers to establish a baseline of current platform usage, tied to a checkpoint in the usage event stream. The feature is purely additive to Cloud Controller and does not modify any existing endpoints or behavior.

## Problem

When a new billing consumer wants to start processing usage events, the START/CREATE events for long-running apps and services have often already been pruned (default 31-day retention). The only current way to establish a baseline is `destructively_purge_all_and_reseed`, which truncates the entire event table and synthesizes new events for running resources. This breaks any existing consumer's event stream -- their checkpoint IDs become invalid, and there is no way to scope the reset to a single consumer. See [Issue #4182](https://github.com/cloudfoundry/cloud_controller_ng/issues/4182) for further discussion.

The result is a gap in the V3 API: there is no safe way for a new consumer to onboard without risking data loss for consumers that are already operating.

## Proposal

Cloud Controller should support two new resource types -- app usage snapshots and service usage snapshots -- each exposed under `/v3/app_usage/snapshots` and `/v3/service_usage/snapshots` respectively. Each resource type supports `POST` (async, admin-write), `GET` list, `GET` by GUID, and `GET` chunks (admin-read). Only one snapshot generation MAY be in progress at a time; concurrent requests SHOULD return `409 Conflict`.

A snapshot captures every running process (or service instance) on the platform at the moment of generation, organized into chunks of up to 50 items grouped by space. Each snapshot records a `checkpoint_event_guid` referencing the most recent usage event at the time the snapshot was created. This checkpoint is what bridges the snapshot to the event stream: a consumer reads the snapshot for its baseline, then begins polling usage events with `after_guid` set to the checkpoint, ensuring no gap or overlap between the two data sources.

An app usage snapshot response looks like this:

```json
{
  "guid": "abc-123",
  "created_at": "2026-01-14T10:00:00Z",
  "completed_at": "2026-01-14T10:00:03Z",
  "checkpoint_event_guid": "def-456",
  "checkpoint_event_created_at": "2026-01-14T09:59:58Z",
  "summary": {
    "instance_count": 15234,
    "app_count": 2500,
    "organization_count": 42,
    "space_count": 156,
    "chunk_count": 200
  },
  "links": {
    "self": { "href": "/v3/app_usage/snapshots/abc-123" },
    "checkpoint_event": { "href": "/v3/app_usage_events/def-456" },
    "chunks": { "href": "/v3/app_usage/snapshots/abc-123/chunks" }
  }
}
```

An earlier approach based on consumer registration was [prototyped](https://github.com/joyvuu-dave/cloud_controller_ng/tree/usage_consumer) but coupled consumer lifecycle to the event cleanup job, creating circular dependencies and an unsolvable zombie consumer problem -- dead consumers block pruning indefinitely, and there's no clean fix short of per-consumer heartbeats. Snapshots avoid this entirely by separating the baseline concern from the event stream.

Snapshots work well in conjunction with the already-reviewed keep-running-records change ([PR #4646](https://github.com/cloudfoundry/cloud_controller_ng/pull/4646)), which prevents start events from being pruned while apps and services are still running. Together they eliminate the need for `destructively_purge_all_and_reseed` when onboarding new billing consumers.

Daily cleanup jobs SHOULD remove completed snapshots older than a configurable retention period (default 31 days) and any in-progress snapshots that have been stuck for more than one hour. Snapshot generation is atomic -- if interrupted, it rolls back completely so no partial snapshots can exist.

This proposal is scoped to Cloud Controller and does not modify any existing API surface.

A reference implementation is available in [PR #4858](https://github.com/cloudfoundry/cloud_controller_ng/pull/4858). Community input is welcome -- in particular, whether a `DELETE` endpoint for manual snapshot removal and operator-configurable chunk sizes would be useful.

## Possible Future Work

CF CLI commands for listing and requesting snapshots (e.g. `cf app-usage-snapshot`, `cf service-usage-snapshot`) would improve the operator experience. The initial proposal focuses on the API surface, which billing systems will consume directly.
