# Meta
[meta]: #meta
- Name: CF CLI v2 Plugins Transition Plan
- Start Date: 2026-04-17
- Author(s): @anujc25, @gerg, @vuil
- Status: Draft
- RFC Pull Request: TBD

## Summary

This RFC defines the strategy for addressing the CAPI v2 End of Life
([RFC-0032](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0032-cfapiv2-eol.md))
for CF CLI plugins, many of which currently directly or indirectly depend on
the v2 API.

Two strategies will be pursued concurrently:
1. The CLI v8 will adopt a compatibility layer (Option A below), ensuring that
   existing, unmodified plugins will continue to function seamlessly even as v2
   endpoints are removed
2. Plugin authors will be provided with a migration tool (Option B) to
   encourage developers to transition their plugins toward direct CAPI v3
   usage, aligning with the long-term vision of a streamlined plugin interface

Crucially, this RFC separates the immediate need to address the v2 EOL from
broader discussions about releasing a v9 CLI or redesigning the plugin interface.

## Problem

RFC-0032 defines the phased end-of-life for CAPI v2, with total removal
targeted for mid/end 2026. While the CF CLI itself no longer uses v2 for core
commands, the plugin interface relies on v2 endpoints for several domain
methods (e.g., `GetApp`, `GetService`). The `plugin_models.*` types returned by
these methods also mirror v2 structures.

If no action is taken, the removal of v2 endpoints will break all plugins
relying on the CLI's domain methods. Additionally, plugins making direct `cf
curl /v2/...` calls are already breaking on environments where v2 has been
disabled.

Two primary solutions have emerged in the community:
- **Option A (CLI-side approach):** Re-implement the internal RPC server that
backs the CLI's plugin interface to call CAPI v3 while preserving the existing
v2-shaped `plugin_models` wire format, effectively shimming the legacy
interface: ([cli#3751](https://github.com/cloudfoundry/cli/pull/3751)).
- **Option B (plugin-side approach):** Plugin developers migrate their plugins
to use CAPI v3 directly, utilizing the CLI solely as an auth and context
provider:
([community#1452](https://github.com/cloudfoundry/community/pull/1452)).

## Proposal

We propose implementing **Option A** as the primary
mechanism to protect the ecosystem from the CAPI v2 EOL, while concurrently
promoting the tools and practices of **Option B** for the long-term health of
the plugin ecosystem.

We explicitly do not want to block the v2 API EOL on the release of a v9 CLI,
nor do we want to block the v2 API EOL on a completely re-designed plugin
interface. Therefore, we are separating what we need to do to address the v2
EOL from any v8/v9 branching discussions.

### Addressing the V2 EOL

We support efforts, such as [PR
#3751](https://github.com/cloudfoundry/cli/pull/3751), to migrate the RPC
server to use v3 APIs.
- This provides an immediate, transparent fix to the v2 EOL issue. It will very
likely prevent field breakages that are already occurring today for some
plugins when used against a CF environment with v2 APIs disabled.

This stability provides the community with a durable, working platform for the
foreseeable future. With the immediate threat of breakage mitigated, there is
no pressing deadline to force an ecosystem-wide migration or introduce breaking
changes to the interface.

### Promoting the Plugin-Side Migration

Despite the safety net provided by Option A, there is a general community
desire to clean up and simplify the plugin interface. The long-term role of the
CLI's plugin interface should be to provide core context (e.g., authenticated
sessions, target retrieval) rather than serving as a proxy for Cloud Controller
domain objects.

This means it is still recommended that plugin authors follow the
migration path laid out in Option B:
- Plugin authors should reduce their dependency on the v2-shaped domain methods
and instead interact directly with CAPI v3.
- We encourage the use of migration tools (like `cf-plugin-migrate`) to audit
and update plugin code.

Doing so will prepare plugins for a transition to a new plugin interface when
it is eventually introduced.

## Impact and Consequences

### For Unmigrated Plugins

Thanks to the CLI-side shim, unmigrated plugins will remain fully functional
when used with an updated CF CLI v8. Plugin authors have no urgent need to
rewrite their code to survive the CAPI v2 removal. They will continue to
receive data mapped into the legacy v2 model structures.

### For Migrated Plugins

Plugins that proactively adopt the plugin-side recommendations will benefit from
direct access to v3-exclusive features and improved performance. Should the
plugin interface be updated or streamlined in the future to formally drop the
deprecated domain methods, these migrated plugins will require little to no
architectural changes, though minor mechanical updates to their registration
plumbing might be necessary.

## Next Steps

- Implement Option A to preserve legacy plugins and sustain support.
- Communicate best practices advising plugin authors to transition v2-based
plugins using Option B for a v3-native experience.
- Continue discussions on the scope and feasibility of a new plugin interface,
separate from the CAPI v2 EOL timeline.
