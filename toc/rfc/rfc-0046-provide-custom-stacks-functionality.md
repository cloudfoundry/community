# Meta

- Name: Provide optional Custom Stacks Functionality in Cloud Foundry
- Start Date: 2025-06-24
- Author(s): @FloThinksPi
- Status: Accepted
- RFC Pull Request: [community#1251](https://github.com/cloudfoundry/community/pull/1251)

## Summary

With the deprecation of the CFLinuxfs3 stack it became obvious that
removing unsupported stacks from an existing and heavily used CF
Foundation comes with massive problems. Ultimately a stack cannot be
removed without all depending apps being migrated to a new stack,
otherwise downtimes of applications that rely on the removed stack will
occur. This RFC proposes improvements in CF to shift this unavailability
towards lifecycle operations and not actual app downtime - making it a
more pleasant experience for CF users and operators alike.
This RFC proposes a way for CF Users that cannot follow a stack removal process as described in [RFC-0045](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0045-enhance-stack-handling.md) to take over the responsibility for their stack and run it as a custom stack, while not needing to mimick the CF staging behaviour and building an own docker application to be able to run with a depricated/locked/disabled/removed stack.
It also opens up possibilities for CF Users to not rely on the CF Foundations stacks but rather use their own stacks to gain independence and release the dependency on the CF Community\'s stack release cadence deliberately on the users choice.

## Table of Contents

- [Meta](#meta)
- [Summary](#summary)
- [Problem](#problem)
  - [Usage](#usage)
  - [Delivery](#delivery)
  - [Adoption Timelines](#adoption-timelines)
- [Motivation](#motivation)
- [Proposal](#proposal)
  - [Bring your own Stack](#bring-your-own-stack)
    - [CF API Changes](#cf-api-changes)
    - [Diego BBS API](#diego-bbs-api)
    - [Providing a stack as remote container image](#providing-a-stack-as-remote-container-image)
    - [CF Tasks](#cf-tasks)
    - [CF Sidecars](#cf-sidecars)
    - [Compatibility Documentation](#compatibility-documentation)
    - [Wrap Up](#wrap-up)
    - [Positive](#positive)
    - [Negative](#negative)

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

![Current Stack Usage](rfc-0046-provide-custom-stacks-functionality/current_stack_usage.png)
Pictured in above diagram is how the stack is brought into a CF
Foundation and used in a CF Foundation. The following problems occur
when trying to remove/deprecate a stack towards users of a CF
Foundation.

Due to [RFC-0039](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0039-noble-based-cflinuxfs5.md), these struggles with the stack become a more pressing issue for CF Foundation operators and users since many still use CFLinuxFS3 and the migration to CFLinuxFS4 is not yet complete for many users. The current stack handling in CF does not allow for a smooth transition and leads to potential downtimes for applications when a stack is removed from the CF Foundation.

### Usage

The management entry of the stack in the stacks table of the CF API
cannot be removed as long as apps exist which use it as the apps table
has a foreign key relationship to the stacks table. The stack thus is
still visible and still usable to all users of a CF Foundation even if
being insecure, deprecated and SHOULD not be adopted anymore.\
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

### Adoption Timelines

Currently a stack is only shipped ever 4 years skipping one LTS version
of ubuntu entirely. This creates a situation where the old stack e.g.
CFLinuxFS3 is flagged as unsecure at roughly the same time the new stack
CFLinuxFS4 is available. This forces users to adopt it in a very small
timeframe if they still want to receive security updates for their
existing workload. In the last migration from CFLinuxFS3 to CFLinuxFS4
it turned out also the buildpacks need time to adopt -- then the
customers to the new buildpacks for which the time there was far too
short.

## Motivation

1. Enable a productized shipment of CF to come without a deprecated
    stack that still is used by apps on the Foundations

2. Without the stack shipped or remove/disable by operators, keep all
    apps running without downtime.

3. Give users and buildpacks more time to adopt, ideally in the range
    of multiple years.

## Proposal

### Bring your own Stack

Currenlty diego bbs only accepts as rootfs:

`precached:cflinuxfs4` as a stack on the local filesystem

`docker://{URL:PORT}/[Image Namespace]:[Reference]` A container
image from a remote. Without URL defaulting to docker hub. Current
method of passing a container image to CF see [the CF
Docs](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html).

Since container images and stacks are technically identical, we MAY offer to support container images as stacks.
This would allow CF Users to use their own stacks, similar to how they can use their own buildpacks today.

##### CF API Changes

First of all the CF API SHOULD add a new feature flag similar to the `diego_docker` feature flag that allows to enable the use of lifecycle docker container images. This flag SHOULD be called `diego_custom_stacks` and be disabled by default in the CF API.

In the CF API we extend the endpoints of apps and cf
manifest to allow a stack not only to be a precached one with a fixed
name e.g. `cflinuxfs4` but also be a valid container image reference e.g. `docker://docker.io/cloudfoundry/cflinuxfs4:1.268.0`. See
<https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#stack>

The CF API CAN check if it's a system
provided one or a remote one by checking if the stack is an exact match
in the stacks table(it already does this to check validity of the
manifest/request) and if it's not an exact match try to evaluate it as
remote container image reference. If it does not match the container url schema produce a error message.

The apps lifecycle object would not only be enabled to have a hardcoded stack name like:

```json
{
  "lifecycle": {
    "type": "buildpack",
    "data": {
      "buildpacks": ["java_buildpack"],
      "stack": "cflinuxfs4"
    }
  },
}
```

but rather also allow a stack to be a container image reference:

```json
{
  "lifecycle": {
    "type": "buildpack",
    "data": {
      "buildpacks": ["java_buildpack"],
      "stack": "docker://docker.io/cloudfoundry/cflinuxfs4:1.268.0"
    },
    "credentials": {
      "example.org": {
        "username": "user",
        "password": "****"
      },
    }
  }
}
```

Similar to the [CNB Lifecycle](https://v3-apidocs.cloudfoundry.org/version/3.196.0/index.html#cloud-native-buildpacks-lifecycle-experimental) adding a credentials sections SHOULD be possible in case the stack resides on a private registry and authentication is required to pull the container image. For `Cloud Native Buildpacks` this is already supported as buildpacks are container images. However opposed to the CNB lifecycle, the credential section SHOULD only implement the `username` and `password` fields as the `token` field is not supported by the Diego BBS API. Diego BBS currently needs always a user [when supplying a password](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#imagepassword-optional) to pull a container image in its `rootfs` field.

For pulling the stack the first credentials SHALL be passed to the Diego BBS API that matches the URL/Hostname of the stack image URI. The CF API SHOULD then fill the fields [ImageUsername](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#imageusername-optional) and [ImagePassword](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#imagepassword-optional) when creating `Tasks` or `LRPs` in the Diego BBS API.

Also for CNBs this currently CAN already be used since the credentials are present in the lifecycles data section.

```json
{
  "type": "cnb",
  "data": {
        "buildpacks": [
            "docker://example.org/java-buildpack:latest"
            "docker://second-example.org/logging-buildpack:latest"
        ],
        "stack": "docker://docker.io/cloudfoundry/cflinuxfs4:1.268.0",
        "credentials": {
            "example.org": {
                "username": "user",
                "password": "****"
            },
            "second-example.org": {
                "token": "****"
            },
        }
  }
}
```

In case a `token` is provided in a credential, the CF API SHOULD ignore credentials which supply a `token` as Diego BBS does not support this field and thus the CF API would not be able to pass it to Diego BBS. Only credentials with a `username` and `password` SHOULD be considdered for the stack. Credentials with the `token` field SHOULD be only used for buildpacks.

Furthermore, in case the stack is a remote container image reference also at least
one system buildpack without a pinned stack MUST exist or a custom
buildpack MUST be provided see
<https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#buildpacks>.

Otherwise the request will be denied by the CF API with the message that there is no buildpack
with that name that fits the stack. This is already the current
behaviour since when you try to force a app to stage with a buildpack
that is assigned a specific stack e.g. `CFLinuxFS4` to be staged with
`CFLinuxFS3` as a stack instead this is prevented by the CF API already:

```
For application \'test: Buildpack \"python_buildpack\" for stack
\"cflinuxfs3\" MUST be an existing admin buildpack or a valid git URI\
FAILED
```

The same would apply if the stack would be a remote container reference
and no own buildpack was provided and none of the system buildpacks can
be used.

##### Diego BBS API

If all the URI evaluation succeeds and boundary conditions like a custom buildpack, feature-flag etc. pass,
the CF API creates the LRP/Task in diego bbs in the [rootfs field](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#rootfs-required) of the LRP setup definition

Optionally also passing the credentials in the [ImageUsername](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#imageusername-optional) and [ImagePassword](https://github.com/cloudfoundry/bbs/blob/main/docs/031-defining-lrps.md#imagepassword-optional) fields.

```json
# Either
"rootfs": "precached:cflinuxfs4"
# or 
"rootfs": "docker://docker.io/cloudfoundry/cflinuxfs4:1.268.0"
# or 
"rootfs": "docker://myprivateregistry.example.com/cloudfoundry/cflinuxfs4:1.268.0",
"imageusername": "user",
"imagepassword": "123"
```

As the logic what to run in the staging process [resides in the CF API](https://github.com/cloudfoundry/cloud_controller_ng/blob/384b017c2e7cf02a492ccffdb6985348abdbf8bb/lib/cloud_controller/diego/buildpack/staging_action_builder.rb) no code change SHOULD be required in diego bbs to support this.
The same [diego actions](https://github.com/cloudfoundry/bbs/blob/main/docs/053-actions.md#available-actions) SHOULD be used as today when using `prechached` stacks as when using remote container images as stacks.

As they `rootfs` and `action` system is quite flexible in diego no code change in diego MAY be actually required to support this.

##### Providing a stack as remote container image

The CF Community also already uploads the stack and publishes it in
container registries e.g. in docker hub
<https://hub.docker.com/r/cloudfoundry/cflinuxfs4> and
<https://hub.docker.com/r/cloudfoundry/cflinuxfs3>

A comprehensive strategy SHOULD be introduced in which the stack images are distributed on multiple registries for redundancy and vendor independence. Proposing following registries wich offer free public container image hosting:

- Docker Hub
- RedHat`s Quay.io
- GitHub Container Registry

##### CF Tasks

The same stack shall be used also for tasks in respective calls to the
Diego API. When talking to diego BBS the same properties `rootfs`, `imageusername` and `imagepassword` exist in a BBS [Task](https://github.com/cloudfoundry/bbs/blob/main/docs/021-defining-tasks.md#rootfs-required)

##### CF Sidecars

###### User Provided Sidecars

User provided [sidecars](https://docs.cloudfoundry.org/devguide/sidecars.html) executed within the applications container are started in the original app container and thus use the proper stack the user wants beeing it a platform proivided stack or a remote container image.

###### Sidecars provided by CF

Cloud Foundry currently injects binaries like [diego-ssh](https://github.com/cloudfoundry/diego-ssh) automatically into an application container and starts them
as sidecar. Since these sidecars currently work already in arbitrary
containers of lifecycle docker, they are statically linked and thus
self-contained and will also function with any stack version alike as
they do not depend at all on OS functionality.

Other process that are started per app container like the envoy-proxy are started in their own container with a system defined stack by [the diego-release config](https://github.com/cloudfoundry/diego-release/blob/develop/jobs/rep/spec#L52-L56).

With the introduction of custom stacks, these sidecars part beeing it customer provided or CF provided sidecars SHOULD behave and function the same as they do today.

##### Compatibility Documentation

With CF having the scope of running arbitrary stacks and already arbitary container images that contain
unknown software e.g. glibc versions that interact with the host\`s
linux kernel, Cloud Foundry SHOULD start documenting, also for the already existing
docker lifecycle, what kernel versions MUST be supported by the
container and stack. And that the container MUST be able to run with that. On every
stemcell major update a deprication notice for the stack SHOULD be
propagated that informs of a major linux kernel update.

While the linux kernel has outstanding compatibility it SHOULD at least
formally defined to not expect support of the CF community if a
containers software/library is designed to interface against an ancient
old kernel version. Newer kernels might remove certain functionality,
have a braking Application Binary Interface change over a long-time span
and thus break older software when running in a containerized
environment. The [kernel
docs](https://www.kernel.org/doc/Documentation/ABI/README) `ABI ...
backward compatibility for them will be guaranteed for at least 2
years`. Also libraries like glibc drop support for certain kernel
versions e.g. with [glibc
2.24](https://sourceware.org/legacy-ml/libc-alpha/2016-08/msg00212.html)
they bumped the min kernel version from 2.6.32 to 3.2. It is not
guaranteed thus that any arbitrary old stemcell or container image will be functional in CF.

Additionally software compiled to interface against a newer kernel version MAY experience missing functionality, imagine a GLIBC compiled against a newer kernel version that uses a syscall that is not available in the older kernel version. This would lead to a runtime error when the software is executed in a container with an older kernel version provided by a stemcell.

Thus a minimum and maximum(current one in the stemcell) kernel version SHOULD be defined, documented and communicated by CloudFoundry. As a CF User i then know which what kernel versions i can build my software against and be able to run the compiled result in a CF Foundation.

Since most applications are using buildpacks that compile everything in the staging process this is not a problem for most CF Users. However, when using lifecycle docker or custom stacks this should be at least properly documented as constraints as it recieves more relevance when executing precompiled binaries in CF directly.

##### Wrap Up

We would enable CF Users to deliberately use a stack which was removed
as system stack and take over full responsibility and self-support if
they cannot follow the support cadence of CF. Similar how a customers on
e.g. AWS CAN decide to deliberately upload an old/own VM Image ISO on their own
risk and with self-support. The service itself remains in a usable
condition at any time.

We would allow CF Operators to programatically change the stack of all applications to a remote one, restage the applications and thus be able to remove the system stack from the CF Foundation as no usage of the stack exists anymore. This would allow to remove a stack without downtime of applications and without the need to keep the stack in the CF Foundation forever.

#### Positive

- When we would prevent staging with a deprecated/locked/removed stack ([RFC-0045](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0045-enhance-stack-handling.md))
  we still CAN offer the user a way forward in his full responsibility
  to be unblocked and to own the whole applications stack end-to-end to
  take their own decisions.

- When a CF Foundation operator wants to remove a system stack, he can
  programatically change the stack of all applications to a remote one,
  restage the applications and thus be able to remove the system stack
  from the CF Foundation as no usage of the stack exists anymore. This
  would allow to remove a stack without downtime of applications and
  without the need to keep the stack in the CF Foundation forever.

- Likely not a high effort to implement on diego level as the container
  images currently are handled the same and stacks are also container
  images saved as tar file. Also, just minor adoptions to the CF API
  logic CAN be expected as its merely accepting container image references
  in the stack and passing it through towards Diego bbs.

#### Negative

- Since the issue with container images - the app cannot be started when
  registry is unavailable - still exists, it is also applied to custom
  stacks. There exist ideas how to cache container images inside CF for
  better reliability and this would also benefit custom stacks, however
  currently this is not implemented or put into an RFC yet but likely
  then needs to be adressed if custom stacks find acceptance to provide the same
  high availability qualities as with system stacks.
