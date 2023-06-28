# Meta
[meta]: #meta
- Name: Readiness Healthchecks
- Start Date: 2023-06-26
- Author(s): @ameowlia, @mariash
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/630


## Summary

Add a readiness healthcheck option for apps. When the readiness healthcheck
passes, the app instance (AI) is marked "ready" and the AI will be routable.
When the readiness healthcheck fails, the AI is marked as "not ready" and its
route will be removed from gorouter's route table.

## Problem

With the current implementation of application healthchecks, when the
application healthcheck detects that an AI is unhealthy, then Diego will stop
the AI, delete the AI, and reschedule a new AI.

This is too aggressive from some apps. There could be many reasons why a single
request could fail, but the app is actually running fine. Additionally, many
applications have a warm up period where they are not ready to receive requests
immediately. For example, apps might need to populate caches, load data, or wait
for external services before they mark themselves as routable. In these cases,
the app should be kept alive, but in a non-routable state.

## Proposal

### Summary
We intend to support readiness healthchecks. (This was requested previously in
this [issue](https://github.com/cloudfoundry/cloud_controller_ng/issues/1706).)
This would be an additional healthcheck that app developers could configure.
When the readiness healthcheck passes, the AI is marked "ready" and the AI will
be routable. When the readiness healthcheck fails, the AI is marked as "not
ready" and its route will be removed from gorouter's route table. This new
readiness healthcheck will give users a healthcheck option that is less drastic
than the current option.

## Types of readiness healthcheck

Readiness healthcheck can be either "http" or "tcp" type. The format of healthcheck
type is [similar to liveness
healthcheck](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html).
The "process" healthcheck type will not be supported since it doesn't make sense
to have "process" readiness healthcheck type. Once any defined process exits AI
is marked as crashed.

### Architecture Overview
This feature will require changes in the following releases

* CF CLI
* Cloud Controller
* Diego
* Routing

1. The cloud controller will store this new data, before passing it onto the BBS
   as part of the desired LRP.
2. The Diego executor will see these new readiness healthchecks on the desired
   LRP and will run the healthchecker binary in the app container with
   configuration provided.
3. When the readiness healthcheck succeeds, the actual LRP will be marked as
   "ready". When the readiness healthcheck fails, the actual LRP will be marked
   as "not ready".
4. When the route emitter gets route information, it will inspect if the AI is
   ready or not ready. It will emit registration or unregistration messages as
   appropriate for the gorouter to consume.

### CC Design
Users will be able to set the healthcheck via the app manifest.

```
applications:
- name: test-app
  processes:
  - type: web
    health-check-http-endpoint: /health
    health-check-invocation-timeout: 2
    health-check-type: http
    timeout: 80
    readiness-health-check-http-endpoint: /ready       # 👈 new property
    readiness-health-check-invocation-timeout: 2       # 👈 new property
    readiness-health-check-type: http                  # 👈 new property
```

### LRP Design

The readiness healthcheck data will be apart of the desired LRP object.

```json
"check_definition": {
    "checks": [
      {
        "http_check": {
          "port": 8080,
          "path": "/health",
          "request_timeout_ms": 10000
        },
      }
    ],
    "readiness_checks": [                  # 👈 new property
      {
        "tcp_check": {
          "port": 8080,
          "connect_timeout_ms": 10000
        },
      }
    ],
    "log_source": ""
  },
```


### Open Questions
* What logging and metrics would be helpful for app devs and operators?

This work is ongoing. All comments and concerns are welcomed from the community.
Either add a comment here or reach out in slack in #wg-app-runtime-platform.


