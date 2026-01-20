# Meta

- Name: Enhance Stack Handling in Cloud Foundry
- Start Date: 2025-06-24
- Author(s): @FloThinksPi
- Status: Accepted
- RFC Pull Request: [community#1220](https://github.com/cloudfoundry/community/pull/1220)

## Summary

With the deprecation of the CFLinuxfs3 stack it became obvious that
removing unsupported stacks from an existing and heavily used CF
Foundation comes with massive problems. Ultimately a stack cannot be
removed without all depending apps being migrated to a new stack,
otherwise downtimes of applications that rely on the removed stack will
occur. This RFC proposes improvements in CF to shift this unavailability
towards lifecycle operations early and not actual app downtime - making it a
more pleasant experience for CF users and operators alike.
To mitigate the downsides of this approach, the [Custom Stack RFC](https://github.com/cloudfoundry/community/pull/1251) proposes to provide custom stacks functionality.

## Table of Contents

- [Meta](#meta)
- [Summary](#summary)
- [Problem](#problem)
- [Motivation](#motivation)
- [Proposal](#proposal)
  - [Improve logical stack management in CF API (cloud_controller_ng)](#improve-logical-stack-management-in-cf-api-cloud_controller_ng)
- [Future Improvements](#future-improvements)
  - [Enable org scoped stack management in CF (cloud_controller_ng)](#enable-org-scoped-stack-management-in-cf-cloud_controller_ng)

## Problem

In the current CF implementation, apps run on so-called Stacks which
provide the base operating system.

Stacks are based on ubuntu and thus bound to ubuntu's [LTS release
cadence and Support](https://ubuntu.com/about/release-cycle). With
Canonical\'s stop of standard security maintenance for ubuntu
18.04(Bionic Beaver) as a consequence also the CFLinuxFS3 stack could
not be maintained anymore and was deprecated. A successor CFLinuxFS4 was
offered based on ubuntu 22.04(Jammy Jellyfish).

Stacks are used for the staging of an application meaning buildpacks run
on the stack to produce the droplet. This in return means that:

- The buildpack is stack specific meaning it can/will break on an
  incompatible stack change like a major version bump

- The droplet the buildpack produces is also stack specific meaning it
  CAN just be instantiated to become an app instance when combining the droplet
  with the same stack it was built with at execution time

![Current Stack Usage](rfc-0045-enhance-stack-handling/current_stack_usage.png)
Pictured in above diagram is how the stack is brought into a CF
Foundation and used in a CF Foundation. The following problems occur
when trying to remove/deprecate a stack towards users of a CF
Foundation.

Due to [RFC-39](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0039-noble-based-cflinuxfs5.md), these struggles with the stack become a more pressing issue for CF Foundation operators and users since many still use CFLinuxFS3 and the migration to CFLinuxFS4 is not yet complete for many users. The current stack handling in CF does not allow for a smooth transition and leads to potential downtimes for applications when a stack is removed from the CF Foundation.

### Usage

The management entry of the stack in the stacks table of the CF API
cannot be removed as long as apps exist which use it as the stack delete
has a check in place that looks up usage and prevents the deletion of a
stack that is still in use.
still visible and still usable to all users of a CF Foundation even if
being insecure, deprecated and SHOULD not be adopted anymore.
It is a cumbersome process for the users to migrate their workload to a
new stack. Оne has to acknowledge that and give users of Cloud Foundry
time to adapt their workload accordingly without a hard deadline when
their apps will stop working.

### Delivery

By regulations one MAY be forced to stop shipping insecure parts of
CloudFoundry for formal/regulatory reasons. That means removing it/not
deploying it with CF-Deployment at all. In this case, the stack is not
put onto the local filesystem of the Diego cell and every app instance
(Long Running Process(LRP)/Task) start will fail because the runtime did not find the
preloaded stack in its local filesystem. One thus is not able to stop
shipping/delivering the outdated, insecure stack anymore without causing
downtimes to all apps still using it.

## Motivation

1. Enable operators to remove/disable a stack to prevent/limit new
    adoption

2. Better communicate and make a stack deprecation visible to
    users of a CF Foundation

## Proposal

### Improve logical stack management in CF API (cloud_controller_ng)

In the CF API currently only a global stack table exists, that either
makes the stack usable(present) or not(missing). Using a stack means
that a call to diego bbs includes that stack as e.g. rootfs
`precached:<stackname>`. No check is in place if the diego cells have
that stack available, so this table is just used to check what a user
requests as stack when doing cf capi calls or pushing a cf manifest.
Also against available system buildpacks if the stack+buildpack
combination is supported. It's not used to check what's actually
available on diego though.

In this proposal we extend the global stack management and table by
introducing a `state` field for each stack. This field will control the
stack's lifecycle and behavior within the Cloud Foundry platform. An administrator
will be able to set the state of a stack via the API, triggering different
behaviors.

The possible states for a stack will be:

- `ACTIVE`: The stack is fully usable. This is the default state for a new stack.
- `DEPRECATED`: The stack is still usable, but a prominent warning will be logged during staging and starting of applications. This is to inform users about the upcoming removal of the stack.
- `RESTRICTED`: The stack cannot be used for new applications. Existing applications using this stack can still be updated, restarted, and scaled. This state is intended to prevent new adoption of the stack.
- `DISABLED`: The stack cannot be used for staging or restaging any application. Existing applications will continue to run, but they cannot be updated. Restarting and scaling of existing apps using the disabled stack is still possible.

This requires extending the `stacks` table in the database with a `state` column. The API endpoints for managing and listing stacks will also need to be updated to expose and allow modification of this new field. Client libraries and the `cf` CLI should be updated to display the stack's state.

The `state` of the stack will directly influence the behavior of the CF API:

- When an application is staged or restaged, the API will check the state of the used stack.
- If the state is `DEPRECATED`, a warning message will be added to the logs.
- If the state is `RESTRICTED`, staging a *new* application will fail with an error.
- If the state is `DISABLED`, staging or restaging *any* application will fail with an error.

To improve communication with developers, the existing `description` field of a stack will be leveraged. The content of the `description` field should be included in any warning or error message related to the stack's state. This allows operators to provide context, migration guides, or links to further documentation.

For example, a deprecation warning could look like this:

```
WARNING: The stack 'cflinuxfs3' is DEPRECATED and will be removed in the future.
Description: This stack is based on Ubuntu 18.04, which is no longer supported. Please migrate your applications to 'cflinuxfs4'. For more information, see: <link-to-docs>.
```

And an error message for a disabled stack:

```
ERROR: Staging failed. The stack 'cflinuxfs3' is DISABLED and can no longer be used for staging.
Description: This stack is based on Ubuntu 18.04, which is no longer supported. Please migrate your applications to 'cflinuxfs4'. For more information, see: <link-to-docs>.
```

This approach provides a clear and explicit way for operators to manage the lifecycle of stacks and communicate changes to users effectively.

#### Positive

- It allows cf admins to phase out a stack via multiple small steps and
  gives both customer and admins a paved road forward to move from one
  stack to another.

- Better awareness of the deprecation and removal of a stack by
  printing a deprecation notices and timelines in the app logs

- It deliberately shifts the unavailability of a stack towards
  lifecycle operations and not actual app downtime - making it a more
  pleasant experience for CF users and operators alike.
  More pleasant for a CF User because an operator that removes a stack does not cause immediate downtime for their apps.
  More pleasant for a CF Operator because they can follow a staged process to remove a stack without causing immediate downtime for all apps using it.

- Likely a manageable change as just in the app creation/staging
  workflows a check is required and the stack table and endpoints CAN be
  extended in a compatible way since all fields are only additions.

#### Negative

- It introduces additional complexity to the stack management process

- Blocks workflows of CF users who want to use a stack that is
  deprecated, restricted or disabled. This may lead to support tickets and
  complaints from CF users. It only affects lifecycle operations and not creates actual app downtime, but it may still be perceived as a negative operation by some users.
  To mitigate this and allow users to regain control over lifecycle operations the [Custom Stack RFC](https://github.com/cloudfoundry/community/pull/1251) proposes
  to provide custom stacks functionality. This allows CF Foundation operators to respond
  to user requests that need the deprecated stack for a longer time.
  Users CAN be enabled by the [Custom Stack RFC](https://github.com/cloudfoundry/community/pull/1251) to unblock themselves by taking over ownership
  of the stack in the case they cannot/don't want to follow the lifecycle of Stacks
  provided by the CF Community.

## Future Improvements

In this section we describe future work that is not part of this RFC but CAN extend the current proposals in the future with a new RFC. Its just here for completeness and to give an idea of what future improvements are possible.

### Enable org scoped stack management in CF (cloud_controller_ng)

In the CF API currently, only a global stack management exists as
described above.
In addition to that we'd like to create the ability for CF Admins to
decide per organization to set or remove the statuses "deprecate",
"restricted", "disabled" on an organization individual basis.

Introducing two new endpoints:

`GET /v3/organizations/[GUID]/stacks`

`UPDATE /v3/organizations/[GUID]/stacks`

This allows CF admins to react on CF user request/complains/tickets on
an individual level rather than re-enabling a deprecated, restricted or
disabled stack for a whole CF Foundation and all users.\
It supplies the tool required by CF admins to support individual users
properly without making commitments to all CF users regarding
support/enablement of a certain stack.

It also creates the opportunity to offer certain system stacks to just a
subset of CF Users as a side motivation. With this mechanism extended
support for a certain stack CAN be provides to individual users.

#### Positive

- Enables admins to react on CF user complains/issues/incidents when
  locking or disabling a certain stack globally

- Enable CF foundation admins to offer certain stacks for certain CF
  users exclusively and not globally for all.

#### Negative

- Likely higher implementation effort since every check against the
  stacks table would need to join a "stacks-visibility-table" in various
  places.

- Needs additional endpoint on org level to list/manage the
  "stacks-visibility-table" to control which stacks are available to
  certain orgs
