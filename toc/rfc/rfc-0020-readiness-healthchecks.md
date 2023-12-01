# Meta
[meta]: #meta
- Name: Readiness Healthchecks
- Start Date: 2023-06-26
- Author(s): @ameowlia, @mariash
- Status: Accepted
- RFC Pull Request: [community#630](https://github.com/cloudfoundry/community/pull/630)


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

[Similar to liveness healthchecks](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html), readiness healthcheck can be of type "http", "port", or "process".
However, when a user selects the "process" healthcheck type, nothing will be passed to the LRP, because once a process exits the AI
is marked as crashed and Diego will attempt a restart. The default readiness healthcheck type is "process", which is backwards compatible.

## Rolling deploys

Rolling deploys should take into account the AI routable status. Old AI should
be replaced with the new once new is running and routable.

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
Users will be able to set the readiness healthcheck via the app manifest.

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
    readiness-health-check-interval: 5                 # 👈 new property
```

New `routable` field in CC API [process stats
object](https://v3-apidocs.cloudfoundry.org/version/3.141.0/index.html#the-process-stats-object)
with values `true` or `false` will display the routable status of the process.

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

### CLI Changes

The `routable` field of the process stats API object property will be used in
CF CLI `cf app` output.

```
     state     routable   since                  cpu    memory          disk         logging            details
#0   running   yes        2023-06-27T15:07:14Z   0.6%   46.8M of 192M   179M of 1G   0/s of unlimited
#1   running   no         2023-06-27T15:11:43Z   0.0%   0 of 0          0 of 0       0/s of 0/s
#2   running   yes        2023-06-27T15:11:43Z   0.0%   0 of 192M       0 of 1G      0/s of 0/s
```

New CLI options will be added to `cf push` command:

* `--readiness-endpoint` will set the endpoint for http readiness
  checks.
* `--readiness-health-check-type` will set the type of the readiness
  check: "http", "port", or "process".
* `--readiness-health-check-interval` will set the interval of the readiness
  check. Must be an integer greater than 0."

New CLI commands will be added:

* `get-readiness-health-check` shows the readiness health check performed on an
  app instance
* `set-readiness-health-check` updates the readiness health check performed on
  an app instance

### Logging and Metrics

#### App logs

When AI readiness healthcheck succeeds a log line is printed to AI logs:
"Container passed the readiness health check. Container marked ready and added
to route pool". When AI readiness healthcheck fails a log line is printed to AI
logs: "Container failed the readiness health check. Container marked not ready
and removed from route pool".

#### App Audit events

When the liveness healthchecks fail, it results in the following audit events:
`audit.app.process.crash` and `audit.app.process.rescheduling`.

Similarly, when AI readiness healthcheck succeeds a new application event should be emitted:
`audit.app.process.ready`. And when AI readiness healthcheck fails a new event should be emitted:
`audit.app.process.notready`.

### Open Questions
* What metrics would be helpful for app devs and operators?

This work is ongoing. All comments and concerns are welcomed from the community.
Either add a comment here or reach out in slack in #wg-app-runtime-platform.


