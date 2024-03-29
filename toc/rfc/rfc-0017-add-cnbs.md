# Meta
[meta]: #meta
- Name: Add Cloud Native Buildpacks
- Start Date: 2023-05-01
- Author: @gerg
- Contributing Authors: @ryanmoran, @robdimsdale, @dsabeti, @aramprice, @dsboulder
- Status: Accepted
- RFC Pull Request: [community#591](https://github.com/cloudfoundry/community/pull/591)

## Summary

[Cloud Native Buildpacks (CNBs)](https://buildpacks.io/), also known as v3
buildpacks, are the current generation of buildpacks and offer some
improvements over the v2 buildpacks that CF Deployment currently uses. The
Cloud Foundry Foundation already has an implementation of Cloud Native
Buildpacks via the [Paketo](https://paketo.io/) project, however these CNBs are
not currently integrated with core CF Deployment.

This RFC proposes adding CNB support to Cloud Foundry and including the Paketo
buildpacks in CF Deployment.

## Problem

The v2 buildpacks are effectively in maintenance mode and do not receive
substantial new features. By not integrating with v3 buildpacks, Cloud Foundry
is missing out on new capabilities like app
[SBOM](https://en.wikipedia.org/wiki/Software_supply_chain) generation, new
buildpacks like the Java Native and Web Servers CNBs, as well as any new
features that are added to the still-actively-developed v3 buildpacks.

## Proposal

### Overview

Cloud Foundry integration with CNBs will be executed over multiple phases.

In the first phase (the focus of this RFC), the Paketo buildpacks will be
"shimmed" to work with Cloud Foundry's existing v2 buildpack interface. These
shimmed Paketo buildpacks will be bundled with select
[CNB lifecycle](https://github.com/buildpacks/lifecycle) binaries and
lightweight orchestration binaries. At build time, the Cloud Foundry
[buildpack lifecycle](https://github.com/cloudfoundry/buildpackapplifecycle)
will invoke the orchestration binaries, which will map the v2 build process to
the v3 build process.

Based on learnings from the first phase of CNB integration and other
factors, there will likely be additional phases of work, however these additional
phases are not covered by this RFC.

Notably, this proposal does NOT include building or running OCI images on Cloud
Foundry. This proposal is to use Paketo buildpacks to build and run Cloud
Foundry droplets. This proposal does not preclude future efforts to integrate
Cloud Foundry with OCI images, container registries, etc.

### Goals

1. Align CF Deployment with the main focus of the Buildpacks team
1. Bring new build capabilities to CF Deployment users, including:
    1. [App SBOMs](https://paketo.io/docs/howto/sbom/)
    1. [Web Servers Buildpack](https://github.com/paketo-buildpacks/web-servers)
    1. [Java Native Buildpack](https://github.com/paketo-buildpacks/java-native-image)
    1. Easier buildpack customization/composition
1. Increase cohesion and app portability between CF Deployment and
   [Korifi](https://www.cloudfoundry.org/technology/korifi/), via mutual Paketo
   integration
1. Increase user base for the CNB lifecycle and Paketo buildpacks
1. Open the door for eventual deprecation of the v2 buildpacks, reducing
   maintenance costs (v2 buildpack deprecation is NOT included in this RFC)

### High Level Implementation

Cloud Foundry will produce a series of experimental, shimmed buildpacks that
include:
1. A Paketo CNB
1. Select executables from the CNB lifecycle
1. Orchestrator executables that conform to the v2 buildpack interface

Cloud Foundry users will interact with the shimmed buildpacks the same as they
do for any other buildpack. For example, the following commands will work as
expected:

```
$ cf create-buildpack ruby_cnb ./ruby_cnb_shim.zip
...
$ cf push my-app --buildpack=ruby_cnb
```

At build time, the procedure will be as follows:
1. The Cloud Foundry Buildpack App Lifecycle's Builder will invoke the shim
   orchestrator executables, consistent with the v2 buildpack interface.
1. The shim orchestrator will invoke the bundled CNB lifecycle executables.
1. The CNB lifecycle executables will invoke the Paketo buildpack executables,
   consistent with the v3 buildpack interface.
1. The Paketo buildpack will build a set of "layer" directories.
1. The shim orchestrator will package the layer directories and
   buildpack-generated SBOMs into a Cloud Foundry droplet and return it back to
   the Cloud Foundry Lifecycle.

For a proof of concept of shimmed buildpacks, see @ryanmoran's
[cfnb](https://github.com/ryanmoran/cfnb) project. Developing the shim
externally at first will allow for more rapid iteration, without disrupting the
core Cloud Foundry runtime.


### Shim at Build Time

At build time, the shim orchestrator will expose the following v2 buildpack
executables:

| Executable | Function |
| --- | --- |
| `detect` | Invoke the CNB Lifecycle `detector` executable |
| `supply` | Invoke the CNB Lifecycle `builder` executable |
| `finalize` | Add CNB `launcher` executable and runtime configuration files to build layers |
| `release` | Package the generated layer directories into a Cloud Foundry droplet |

These executables will be invoked by the Cloud Foundry Buildpack App Lifecycle's
builder.

### Shim at Run Time

At run time, the Cloud Foundry Buildpack App Lifecycle's Launcher will invoke the
CNB Lifecycle `launcher` executable that was included in the droplet at build
time. In order to support custom start commands for apps using the CNB
buildpack shims, the CNB launcher invocation will be prepended to the app start
command using the [`entrypoint_prefix` hook](https://github.com/cloudfoundry/buildpackapplifecycle/commit/29feb13caeff646f35585eee865c376c818fc2ea)
in the CF Lifecycle launcher.

### Service Bindings

The largest anticipated breaking change from v2 to v3 buildpacks is the change
in how service bindings are consumed by buildpacks. The v3 buildpacks expect
service bindings to follow the [Kubernetes Service Binding specification](https://github.com/servicebinding/spec),
which places service binding credentials on the filesystem. Cloud Foundry and
v2 buildpacks instead use environment variables for service binding
credentials. The majority of the v2 and v3 buildpacks do not consume service
bindings, so solving this problem will not block execution for most buildpacks.

At time of writing, there are two viable solutions to integrate the Paketo
buildpacks with CF Deployment: emulating Kubernetes Service Bindings in Diego
or updating the Paketo buildpacks to consume Cloud Foundry environment
variables.

#### Emulating Kubernetes Service Bindings

In order to securely place credentials on the filesystem, Diego will need the
ability to mount in-memory filesystems (e.g. `tmpfs`) in app containers. Once
an in-memory filesystem is available, select `VCAP_SERVICES` environment
variables can be translated into their Kubernetes Service Binding equivalents
by the shim orchestrator, for consumption by the Paketo buildpacks.

#### Paketo Buildpacks Consume Environment Variables

There is work in progress for CNBs using the `libcnb` package to read Cloud
Foundry environment variables in addition to Kubernetes Service Bindings
(see [buildpacks/libcnb#227](https://github.com/buildpacks/libcnb/pull/227)).
Outside of the Java buildpacks, the Paketo buildpacks do not currently use
`libcnb`, so the remaining Paketo buildpacks that consume service bindings
will need to be updated to use `libcnb` or add equivalent logic. If the Paketo
buildpacks are updated with this change, then no changes will be needed to the
core Cloud Foundry runtime.

#### Recommendation

Updating the Paketo buildpacks to consume Cloud Foundry environment variables
appears to be the easier option. However, given that there are at least two
viable options for buildpack service binding consumption, this RFC proposes
making the final decision at implementation time.

### Governance and Release

A `cnb-shim-builder` repository will be added to the Application Runtime
Interfaces working group. This repository will contain the tooling necessary
for converting existing Paketo buildpacks into shimmed CNBs.

The shimmed buildpacks will be experimental BOSH releases, belonging to the
Application Runtime Interfaces working group. The proposed list of buildpacks
is as follows (in rough priority order):
1. `java_native_cnb_release`
1. `java_cnb_release`
1. `web_servers_cnb_release`
1. `dotnet_core_cnb_release`
1. `nodejs_cnb_release`
1. `python_cnb_release`
1. `ruby_cnb_release`
1. `procfile_cnb_release`
1. `go_cnb_release`
1. `nginx_cnb_release`
1. `php_cnb_release`
1. `rust_cnb_release`

It is possible that not all buildpacks will be shimmed during the first phase
of this project. Depending on the effort to shim buildpacks and other factors,
it may make sense to move to later phases of CNB integration before all Paketo
buildpacks are shimmed. In such an event, follow-on RFCs will describe
additional phases of work.

The CNBs will initially be opt-in for CF Deployment operators via an
experimental ops file. When installed, the Paketo buildpacks will follow a
different naming convention than the v2 buildpacks (e.g. `ruby_cnb` instead
of `ruby_buildpack`) and will be installed with a lower detect order than the
v2 buildpacks. Once the v3 buildpacks have reached a suitable level of maturity
and stability, they will be added to the default set of buildpacks installed as
part of CF Deployment.

### Possible Future Work

The following areas are not directly covered by this RFC, but suggest some of
the possible follow-on work that could be executed in later phases of Cloud
Foundry CNB integration.

#### Support Unmodified Paketo Buildpacks

Unmodified (non-shimmed) Paketo buildpacks could be natively supported by Cloud
Foundry. For instance, this could be implemented by integrating the buildpack
shim logic into a new or existing Cloud Foundry lifecycle. The details of this
integration should be covered by an additional RFC, once the first phase of CNB
integration is complete.

#### Build Apps into OCI Images

Instead of outputting droplets from the staging process, Cloud Foundry could
instead produce OCI images, consistent with other CNB platforms. This change
would have a number of architectural and operator-impacting implications, and
would need to be discussed in detail via another RFC.

#### Add Paketo Stacks

Initially, the shimmed Paketo buildpacks will be compatible with `cflinuxfs4` to
ease development and adoption. Paketo provides
[multiple stacks](https://paketo.io/docs/concepts/stacks/#what-paketo-stacks-are-available)
that are compatible with the Paketo buildpacks. There is an opportunity to
adopt some or all of the Paketo stacks into CF Deployment. The Paketo
buildpacks have greater cohesion with the Paketo stacks than with `cflinuxfs4`,
and the Paketo "base" and "tiny" stacks could offer security-conscious CF
Deployment users stacks with far fewer native packages than are currently
included with `cflinuxfs4`. This RFC does not cover the adoption of additional
stacks into CF Deployment, but it does open the door to add these stacks in the
future.

