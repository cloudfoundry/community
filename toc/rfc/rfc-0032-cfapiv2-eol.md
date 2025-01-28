# Meta
[meta]: #meta
- Name: CF API v2 End of Life
- Start Date: 2024-08-08
- Author(s): stephanme
- Status: Accepted
- RFC Pull Request: [community#941](https://github.com/cloudfoundry/community/pull/941)


## Summary

CF API v2 is deprecated since at least 2021 but there is no End of Life date communicated (see [ccng #2725](https://github.com/cloudfoundry/cloud_controller_ng/discussions/2725)).

This RFC shall define a plan to disable and finally remove CF API v2 from CAPI and cf-deployment.

## Problem

There are several issues and efforts with keeping the deprecated CF API v2 as part of CAPI and cf-deployment:

- Maintenance effort in CAPI and CF API client libraries
- CF API v2 uses a different Ruby web framework than v3 
- Shipping an API that is not well tested anymore: CATS don’t test CF API v2
- Performance problems especially in large foundations: metrics show that v2 requests take between 3 to 5 times as long as v3 requests on average
- Larger cloud controller database schema refactorings/improvements are not possible or at least difficult because the same DB schema has to serve v2 and v3. This blocks performance improvements in CF API v3.
  - Example: [ccng decision 0007-implementing-v3-roles.md](https://github.com/cloudfoundry/cloud_controller_ng/blob/main/decisions/0007-implementing-v3-roles.md)
  - Areas where schema changes could lead to performance improvements: roles, service plan visibilities
- More fine grained org and space roles, a recurring user request, would benefit from a DB schema migration away from the current one table per role design. Blocked as well by CF API v2.

## Proposal

Since CF API v2 removal is a fundamental breaking change, the removal is divided into 3 phases of about 1 year each with checkpoints in between that require TOC approval.
If the TOC does not approve moving to the next phase, the TOC will decide a number of months to extend the current phase. Subsequent phases and the EoL date will be updated accordingly. The TOC will then re-convene after that period to again evaluate if it is appropriate to move to the next phase.

**Phase 1** (starts after accepting this RFC)
- Announce an End of Life date for CF API v2 (~ mid/end 2026).
- Engineering work so that all cf-deployment components are built/tested/released with v2 turned off
- Turn off CF API v2 by default in cf-deployment (set CAPI property [cc.temporary_enable_v2](https://bosh.io/jobs/cloud_controller_ng?source=github.com/cloudfoundry/capi-release&version=1.185.0#p%3dcc.temporary_enable_v2) to false). Operators may still re-enable v2.

**Checkpoint 1**
- [cf-deployment v47.0.0](https://github.com/cloudfoundry/cf-deployment/releases/tag/v47.0.0) ships with disabled CF API v2. It can be re-enabled by operators using [enable-v2-api.yml](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/enable-v2-api.yml).
- TOC approval documented in PR

**Phase 2** (after Checkpoint 1, ~mid/end 2025)
- Engineering work so that all CFF-controlled clients use v3 by default
- Window for 3rd-party clients to complete migration to v3

**Checkpoint 2**
- TOC approval

**Phase 3** (after Checkpoint 2, ~mid/end 2026)
- Turn CF API v2 permanently off for CAPI/cf-deployment.
- Engineering work to remove CF API v2 from CAPI.

### Impact and Consequences

- CF API client libraries like [cf-java-client](https://github.com/cloudfoundry/cf-java-client), [cf-goclient](https://github.com/cloudfoundry/go-cfclient) and [cf_exporter](https://github.com/cloudfoundry/cf_exporter) should plan for closing gaps in CF API v3 support and for removing their CF API v2 implementation.
- CF CLI v6 and v7 still use CF API v2 and will stop working against foundations with disabled CF API v2. CF CLI v8 doesn’t use CF API v2 anymore (exception: CLI plugins, see next point).
- Most CF CLI plugins rely on CF API v2. A new CF CLI plugin interface should be defined (out of scope of this RFC). However, it is possible to implement a CLI plugin without using CF API v2.
- Cloud Foundry users and operators may use tooling and CI/CD pipelines which still rely on CF API v2 and therefore have migration efforts.

CF API v2 specific rate limiting and the feature flag to disable CF API v2 completely is already implemented in CAPI.
The [CF API v3 Upgrade Guide](https://v3-apidocs.cloudfoundry.org/index.html#upgrade-guide) helps authors of CF api clients to migrate from v2 to v3.
