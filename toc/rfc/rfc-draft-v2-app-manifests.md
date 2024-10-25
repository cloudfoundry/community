# Meta
[meta]: #meta
- Name: App Manifests v2
- Start Date: 2024-10-25
- Author(s): @gerg @tcdowney
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

[Application Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html)
empower app developers to bulk-apply configuration to their applications and
persist that configuration in their source control, alongside their application
code.

This RFC proposes implementing a new major version (v2) of the application
manifest schema to add new functionality, ease future development, and enable
powerful user workflows. Notably, the v2 manifest will be
[declarative](https://en.wikipedia.org/wiki/Declarative_programming), bringing
them in-line with modern developer expectations and technologies like bosh and
Kubernetes.

## Problem

App manifests currently support much, but not all, of the developer-relevant
configuration available on Cloud Foundry. The existing manifest structure makes
it difficult to add new features. TK: Why?

TK: Declarative....

## Proposal

### Guiding Principles

#### Mirror v3 API Design

#### Resources Not Nested Under Apps

When possible, space-level resources should have their own top-level
configuration block, rather than being nested under apps. For example, routes
and service instances are now top-level objects, instead of being nested under
apps.

#### References to Resources are Objects

When referencing resources, use objects instead of simple strings. This makes
it easier to extend with additional configuration in the future. For example,
favor

```yaml
routes:
  - url: example.com
```

over

```yaml
routes:
  - example.com
```

#### Keys Use Underscores

Schema version 1 of app manifests use a combination of underscores and hyphens
for keys. Schema version 2 keys should only use underscores to match the
convention on the API. 

### Behavior

#### Version

As part of the move to server-side manifests, we introduced a new "version"
field in the manifest. This allows us to introduce different structures and
behaviors for application manifests, while still supporting older manifest
schemas.

#### Declarative

Should the schema version 2 app manifest be declarative? Put another way, should removing a resource from the manifest delete that resource?

Pros:
Declarative configuration is standard these days (see Bosh, Concourse, K8s).
We are making a schema version bump, so this is a good opportunity to do it.
Will enable GitOps workflows for Cloud Foundry app developers.

Cons:
This will be a pretty significant change to the behavior of the manifest and will make migrating to schema version 2 difficult.
This can make pushing an app or applying a manifest more dangerous, especially if we don't do a good job messaging what the impact will be (e.g. via manifest diffs).

Answer: We almost certainly want declarative manifests. This lets us enable GitOps-style workflows.

### Example v2 Manifest

```yaml
---
version: 2
routes:
  - url: route.example.com/path
    destinations:
      - app:
          name: app1
          process:
            type: other
        weight: 60
        port: 9999
      - app:
          name: app2
        weight: 40
  - url: tcp-route.example.com:5678
    protocol: tcp
    destinations:
      - app:
          name: app1
network_policies:
  - source: 
      app: 
        name: app1
    destination: 
      app: 
        name: app2
        port: 1234
    protocol: tcp
services:
  - name: my-service
    bindings:
      apps:
        - name: app1
        - name: app2
  - name: route-service
    bindings:
      routes:
        - url: route.example.com
  - name: service-with-arbitrary-params
    bindings:
      apps:
        - name: app1
          parameters:
            key1: value1
            key2: value2
apps:
  - name: app1
    package:
      path: /path/to/source/code
    buildpacks:
      - name: ruby_buildpack
      - name: java_buildpack
      - url: git.example.com/my_buildpack
    environment_variables:
      VAR1: value1
      VAR2: value2
    stack:
      name: cflinuxfs4
    features:
      ssh: true
    metadata:
      annotations:
        contact: bob@example.com jane@example.com
      labels:
        sensitive: true
    processes:
      - type: web
        command: start-web.sh
        disk_quota: 512M
        health_checks:
          liveness:
            http_endpoint: /health_check
            type: http
            invocation_timeout: 10
            timeout: 10
          readiness:
            type: port
        instances: 3
        memory: 500M
      - type: worker
        command: start-worker.sh
        disk_quota: 1G
        health_check:
          type: process
          timeout: 15
        instances: 2
        memory: 256M
  - name: app2
    package:
      docker:
        image: docker-image-repository/docker-image-name
        username: docker-user-name
    processes:
      - type: web
        instances: 1
        memory: 256M
    sidecars:
      - name: authenticator
        processes:
          - type: web
          - type: worker
        command: bundle exec run-authenticator
        memory: 800M
```

####  Notable Changes

For a full list of changes, see Appendix 2.
1. Renamed "applications" to "apps".
1. Moved "routes" to a top-level key.
1. Moved "services" to a top-level key.
1. Added "network_policies" top-level key.

