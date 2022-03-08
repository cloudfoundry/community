# App Runtime Platform: Working Group Charter

## Mission

Provides operational components for the CF App Runtime, including those for application build, application execution, ingress and app-to-app routing, and aggregation of application logs and metrics.


## Goals

- End-user platform teams have reliable, performant, and well-documented system components to provide core CF App Runtime capabilities within BOSH-based deployments.
- Community contributors can build against core CF App Runtime system components via stable, well-documented APIs.
- Community contributors can integrate tested CF App Runtime components into community reference deployments.


## Scope

- Develop system components that support core CF App Runtime capabilities, including building app artifacts from source code, running artifacts as apps, routing traffic to apps and between apps, and aggregating logs and metrics from applications for end-user consumption.
- Maintain public roadmaps for the CF App Runtime component systems above and ensure that system component development matches roadmap intent.
- Align component development to the priorities of App Runtime end users via collaboration with other Working Groups.
- Provide community contributors with tooling and reference pipelines needed to build, test, and release App Runtime system components.
- Collaborate with other Working Groups to ensure that App Runtime components are integrated regularly into the community reference deployments.
- Maintain documentation for system component APIs, including which API groups are stable for use or are experimental and which API groups are intended for end-user internal use.
- Ensure upgrade pathways for system components, with disruptive changes communicated clearly.



## Non-Goals

- Be responsible for these functional domain areas outside of the CF App Runtime system.

## Roles & Technical Assets

Components from the Diego, Garden, HAproxy, Logging and Metrics, Networking, Windows Containers projects.

```yaml
name: App Runtime Platform
execution_leads:
- name: Amelia Downs
  github: ameowlia
technical_leads:
- name: Amelia Downs
  github: ameowlia
areas:
- name: Diego
  approvers:
  - name: Andrew Crump
    github: acrmp
  - name: Amin Jamali
    github: aminjam
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Geoff Franks
    github: geofffranks
  - name: Ivan Hristov
    github: IvanHristov98
  - name: Josh Russett
    github: jrussett
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  repositories:
  - cloudfoundry/diego-team
  - cloudfoundry/diego-release
  - cloudfoundry/archiver
  - cloudfoundry/auction
  - cloudfoundry/auctioneer
  - cloudfoundry/bbs
  - cloudfoundry/benchmarkbbs
  - cloudfoundry/bytefmt
  - cloudfoundry/cacheddownloader
  - cloudfoundry/certsplitter
  - cloudfoundry/cfdot
  - cloudfoundry/cf-volume-services-acceptance-tests
  - cloudfoundry/consuladapter
  - cloudfoundry/debugserver
  - cloudfoundry/diego-ci
  - cloudfoundry/diego-dockerfiles
  - cloudfoundry/diego-logging-client
  - cloudfoundry/diego-upgrade-stability-tests
  - cloudfoundry/dockerdriver
  - cloudfoundry/docker_driver_integration_tests
  - cloudfoundry/durationjson
  - cloudfoundry/ecrhelper
  - cloudfoundry/eventhub
  - cloudfoundry/executor
  - cloudfoundry/fileserver
  - cloudfoundry/grace
  - cloudfoundry/healthcheck
  - cloudfoundry/inigo
  - cloudfoundry/localdriver
  - cloudfoundry/localip
  - cloudfoundry/locket
  - cloudfoundry/operationq
  - cloudfoundry/rep
  - cloudfoundry/route-emitter
  - cloudfoundry/systemcerts
  - cloudfoundry/tlsconfig
  - cloudfoundry/vizzini
  - cloudfoundry/volman
  - cloudfoundry/workpool

- name: Docs
  approvers:
  - name: Melinda Jeffs Gutermuth
    github: mjgutermuth
  repositories:
  - cloudfoundry/docs-book-cloudfoundry
  - cloudfoundry/docs-cf-admin
  - cloudfoundry/docs-loggregator
  - cloudfoundry/docs-running-cf

- name: Garden Containers
  approvers:
  - name: Anthony Emengo
    github: aemengo
  - name: Danail Branekov
    github: danail-branekov
  - name: Giuseppe Capizzi
    github: gcapizzi
  - name: George
    github: georgethebeatle
  - name: Kieron Browne
    github: kieron-dev
  - name: Mario Nitchev
    github: mnitchev
  repositories:
  - cloudfoundry/garden-ci
  - cloudfoundry/garden-runc-release
  - cloudfoundry/dontpanic
  - cloudfoundry/garden
  - cloudfoundry/garden-integration-tests
  - cloudfoundry/grootfs
  - cloudfoundry/guardian
  - cloudfoundry/idmapper
  - cloudfoundry/netplugin-shim
  - cloudfoundry/cpu-entitlement-plugin
  - cloudfoundry/cpu-entitlement-admin-plugin
  - cloudfoundry/winc-release
  - cloudfoundry/winc
  - cloudfoundry/groot-windows
  - cloudfoundry-incubator/diff-exporter
  - cloudfoundry/cert-injector

- name: Logging and Metrics
  approvers:
  - name: Andrew Crump
    github: acrmp
  - name: Amin Jamali
    github: aminjam
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Geoff Franks
    github: geofffranks
  - name: Josh Russett
    github: jrussett
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  repositories:
  - cloudfoundry/bosh-system-metrics-forwarder-release
  - cloudfoundry/log-cache-release
  - cloudfoundry/go-log-cache
  - cloudfoundry/loggregator-release
  - cloudfoundry/go-diodes
  - cloudfoundry/go-envstruct
  - cloudfoundry/go-loggregator
  - cloudfoundry/go-metric-registry
  - cloudfoundry/go-pubsub
  - cloudfoundry/loggregator-agent-release
  - cloudfoundry/dropsonde
  - cloudfoundry/go-batching
  - cloudfoundry/sonde-go
  - cloudfoundry/metrics-discovery-release
  - cloudfoundry/statsd-injector-release
  - cloudfoundry/system-metrics-scraper-release

- name: Networking
  approvers:
  - name: Miki Mokrysz
    github: 46bit
  - name: Andrew Crump
    github: acrmp
  - name: Amin Jamali
    github: aminjam
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Carson Long
    github: ctlong
  - name: Dominik Froehlich
    github: domdom82
  - name: Geoff Franks
    github: geofffranks
  - name: Greg Cobb
    github: Gerg
  - name: Josh Russett
    github: jrussett
  - name: Matthew Kocher
    github: mkocher
  - name: George Gelashvili
    github: pivotalgeorge
  - name: Patrick Lowin
    github: plowin
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  - name: Stefan Lay
    github: stefanlay
  repositories:
  - cloudfoundry/networking-oss-deployments
  - cloudfoundry/routing-release
  - cloudfoundry/routing-acceptance-tests
  - cloudfoundry/routing-api
  - cloudfoundry/routing-api-cli
  - cloudfoundry/routing-perf-release
  - cloudfoundry/cf-tcp-router
  - cloudfoundry/routing-info
  - cloudfoundry/gorouter
  - cloudfoundry/route-registrar
  - cloudfoundry/haproxy-boshrelease
  - cloudfoundry/cf-networking-release
  - cloudfoundry/cf-networking-helpers
  - cloudfoundry/silk-release
  - cloudfoundry/silk
  - cloudfoundry/nats-release
```
