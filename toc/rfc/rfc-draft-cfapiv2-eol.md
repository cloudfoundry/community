# Meta
[meta]: #meta
- Name: CF API v2 End of Life
- Start Date: 2024-08-08
- Author(s): stephanme
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


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

September 2024 (after accepting this RFC)
- Add a validation to cf-deployment that runs with disabled CF API v2
- Define and announce an End of Life date for CF API v2: end of 2025

Jan 2025
- Disable CF API v2 in cf-deployment by changing the default for CAPI property [cc.temporary_enable_v2](https://bosh.io/jobs/cloud_controller_ng?source=github.com/cloudfoundry/capi-release&version=1.185.0#p%3dcc.temporary_enable_v2) to false. Operators may still re-enable v2.

Jan 2026
- CF API v2 reached EOL
- Remove the option to re-enable CF API v2 in CAPI and cf-deployment
- Remove CF API v2 implementation from CAPI

### Impact and Consequences

- CF API client libraries like [cf-java-client](https://github.com/cloudfoundry/cf-java-client), [cf-goclient](https://github.com/cloudfoundry/go-cfclient) and [cf_exporter](https://github.com/cloudfoundry/cf_exporter) should plan for closing gaps in CF API v3 support and for removing their CF API v2 implementation.
- CF CLI v6 and v7 still use CF API v2 and will stop working against foundations with disabled CF API v2. CF CLI v8 doesn’t use CF API v2 anymore (exception: CLI plugins, see next point).
- Most CF CLI plugins rely on CF API v2. A new CF CLI plugin interface should be defined (out of scope of this RFC). However, it is possible to implement a CLI plugin without using CF API v2.
- Cloud Foundry users and operators may use tooling and CI/CD pipelines which still rely on CF API v2 and therefore have migration efforts.

CF API v2 specific rate limiting and the feature flag to disable CF API v2 completely is already implemented in CAPI.
The [CF API v3 Upgrade Guide](https://v3-apidocs.cloudfoundry.org/index.html#upgrade-guide) helps authors of CF api clients to migrate from v2 to v3.