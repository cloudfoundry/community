# Meta

[meta]: #meta
- Name: Cloud Native Buildpacks Lifecycle
- Start Date: 2024-03-19
- Author(s): @c0d1ngm0nk3y, @pbusko, @nicolasbender, @modulo11
- Status: Accepted
- RFC Pull Request: [community#831](https://github.com/cloudfoundry/community/pull/831)
- Updates: [RFC 0017](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0017-add-cnbs.md)

## Summary

[Cloud Native Buildpacks (CNBs)](https://buildpacks.io/), also known as v3 buildpacks, are the current generation of buildpacks and offer some improvements over the v2 buildpacks that CF Deployment currently uses. The Cloud Foundry Foundation already has an implementation of Cloud Native Buildpacks via the [Paketo](https://paketo.io/) project, however these CNBs can't currently be used in CF.

This RFC introduces a new optional lifecycle to Cloud Foundry which enables users to build their applications using Cloud Native Buildpacks.

## Problem

The v2 buildpacks are effectively in maintenance mode and do not receive substantial new features. By not integrating with v3 buildpacks, Cloud Foundry is missing out on new buildpacks (e.g. Java Native and Web Servers CNBs) as well as any new features that are added to the still-actively-developed v3 buildpacks.

## Proposal

- Introduce a new [lifecycle type](https://v3-apidocs.cloudfoundry.org/index.html#lifecycles) `cnb` and its lifecycle data
- Introduce a new [app lifecycle](https://github.com/cloudfoundry/diego-design-notes#app-lifecycles) called `cnbapplifecycle` which interacts with the [CNB Lifecycle](https://github.com/buildpacks/lifecycle)
- Reuse [cflinuxfs4](https://github.com/cloudfoundry/cflinuxfs4) as the base for staging and running apps
- Introduce a new flag to CLI and the [app manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html) to be able to use Cloud Native Buildpacks instead of v2 buildpacks

### Architecture

This will require changes in the following releases:

- CF CLI
- Cloud Controller
- Diego

No changes to how Diego runs workloads are necessary to implement this RFC.

- The cli will forward a new app lifecycle type to the cloud controller.
- The cloud controller will use a new `cnbapplifecycle` for the application.

Affected cloud controller APIs (all that interact with [lifecycles](https://v3-apidocs.cloudfoundry.org/index.html#lifecycles)):

- [apps](https://v3-apidocs.cloudfoundry.org/index.html#apps)
- [builds](https://v3-apidocs.cloudfoundry.org/index.html#builds)
- [droplets](https://v3-apidocs.cloudfoundry.org/index.html#droplets)
- [manifests](https://v3-apidocs.cloudfoundry.org/index.html#manifests)

### Goals

- Establish the latest generation of buildpacks in CF as first-class citizen
- Increase cohesion and app portability between CF Deployment and [Korifi](https://www.cloudfoundry.org/technology/korifi/), via mutual Paketo integration
- Increase adoption of Cloud Native Buildpacks
- Open the door for eventual deprecation of the v2 buildpacks, reducing maintenance costs (v2 buildpack deprecation is NOT included in this RFC)
- No fundamental changes to the architecture of CF
  - Result of the staging process will be a droplet
  - No OCI registry necessary
  - Reuse cflinuxfs4 as rootfs during build and run
  - No change to how the Cloud Foundry platform provides service binding information (see [#804](https://github.com/cloudfoundry/community/pull/804) for how this will be covered in a separate RFC)

### High Level Implementation

#### CNB App Lifecycle

Introduce a new `lifecycle type` that enables the cloud controller to differentiate between the classical buildpacks and Cloud Native Buildpacks. On a high level, it will be very similar to the existing buildpackapplifecycle (v2 buildpacks). The new app lifecycle acts as a CNB [platform](https://buildpacks.io/docs/for-app-developers/concepts/platform/) and will:

1. Download the app source code from the blobstore
1. Download the CNB app lifecycle from the blobstore
1. Download the configured buildpacks
1. Write an [order.toml](https://github.com/buildpacks/spec/blob/main/platform.md#ordertoml-toml) with configured buildpacks
1. Execute [detect](https://github.com/buildpacks/spec/blob/main/platform.md#detector) and [build](https://github.com/buildpacks/spec/blob/main/platform.md#builder) phases using the [CNB lifecycle](https://github.com/buildpacks/lifecycle)
1. Package the result into a droplet and upload it to the blobstore
1. Write a result.json file with the [Staging Result](https://github.com/cloudfoundry/buildpackapplifecycle/blob/f4b2bc9ff6cc6229402d7c27e887763154cf0378/models.go#L73-L80)

#### CNB Lifecycle Type

Introduce a new type of lifecycle type which indicates that Cloud Native Buildpacks should be used. In future, this can be enhanced with additional CNB inputs. For this RFC we’d start with:

```json
{
  "type": "cnb",
  "data": {
    "buildpacks": ["docker://gcr.io/paketo-buildpacks/java"],
    "stack": "cflinuxfs4"
  }
}
```

Both, building and running an app will be based on the configured stack. If no stack is provided, the platform default is used. An empty (or not provided) list of buildpacks will lead to an error. This essentially means, that no auto-detection is supported at the moment. Once [system CNBs](#system-buildpacks) are supported, this behavior will change.

#### CF CLI

New flag `–-lifecycle [buildpack|docker|cnb]` will be introduced to the `cf push` command.

#### App Manifest

New property `lifecycle: buildpack|docker|cnb` will be added to the App manifest. It will default to `lifecycle: buildpack`. Using `docker-*` properties implies `lifecycle: docker`.
The buildpack URL must start with one of the following schemas: `docker://`, `http://` or `https://`.

```yaml
---
applications:
  - name: test-app
    instances: 1
    lifecycle: cnb
    buildpacks:
      - docker://gcr.io/paketo-buildpacks/java
```

Both changes (CLI and manifest) were chosen because they are simple (from a user perspective), easy to implement and remove, if CNBs will become the standard lifecycle in future.

### Alternative APIs

- Instead of a lifecycle type switch, introduce a `buildpack-type` (`v2`/`v3` or `cf`/`cnb` or `classic`/`cnb`) to distinguish between different lifecycles.

#### Diego Release

The new lifecycle package `cnb_app_lifecycle` will be added to the Diego BOSH release, next to the existing `buildpack_app_lifecycle` and `docker_app_lifecycle`. This lifecycle package should be served by the File Server in the same way as existing lifecycle packages.

### Possible Future Work

#### Add Paketo Stack(s)

This RFC does not include the addition of a new stack to Cloud Foundry, rather the resulting droplet would run on top of the existing `cflinuxfs4`. This should work for most, if not all apps, as the stack is much bigger (in terms of native packages installed) than the stacks used by Paketo.

Paketo provides multiple stacks that are compatible with the Paketo buildpacks. There is an opportunity to adopt some or all of the Paketo stacks into CF Deployment. The Paketo buildpacks have greater cohesion with the Paketo stacks than with `cflinuxfs4`, and the Paketo "base" and "tiny" stacks could offer security-conscious CF Deployment users stacks with far fewer native packages than are currently included with `cflinuxfs4`.

This RFC does not cover the adoption of additional stacks into CF Deployment, but it does open the door to add these stacks in the future.

#### System Buildpacks

This RFC enables only the use of custom buildpacks. CNBs could be added as system buildpacks later to support some auto detection as for the existing v2 buildpacks.

#### Better SBoM Support

This RFC already introduces some SBoM capabilities offered by CNBs. Yet, it is not complete (runtime OS information is missing) and buried in the layers of the droplet. This could be further improved in future.

### Open Questions

#### Pulling Buildpacks from private registries

Cloud Foundry currently supports only a single set of credentials together with a single docker image being passed as part of a `cf push --docker`. However, with Cloud Native Buildpacks multiple images, from multiple registries, using different credentials is possible. Deducting the registry from the passed Cloud Native Buildpacks is not possible e.g. when they are consumed from unauthenticated (e.g. DockerHub) and authenticated registries.

Options:

- Require environment variable with docker config content.

```json
{
  "auths": {
    "registry.io": {
      "auth": "dXNlcjpwYXNzd29yZA=="
    }
  }
}
```

- Require environment variable pointing to docker config file. CF CLI must parse the file and invoke helpers if needed for required registries.
- Require custom credentials configuration e.g.

```bash
CNB_REGISTRY_CREDS='{"registry.io":{"user":"password"}}' cf push ...
```

```json
{
  "type": "cnb",
  "data": {
    "buildpacks": ["docker://gcr.io/paketo-buildpacks/java"],
    "stack": "cflinuxfs4",
    "credentials": {
      "registry.io": {
        "user": "password"
      }
    }
  }
}
```
