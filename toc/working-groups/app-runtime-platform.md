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


## Proposed Membership

Technical and Execution Lead: @ameowlia

### Approvers by area

Diego:
- @acrmp
- @aminjam
- @Benjamintf1
- @geofffranks
- @IvanHristov98
- @jrussett
- @pivotalgeorge
- @reneighbor
- @selzoc

Garden Containers:
- @aemengo
- @danail-branekov
- @gcapizzi
- @georgethebeatle
- @kieron-dev
- @mnitchev

Logging and Metrics:
- @acrmp
- @aminjam
- @Benjamintf1
- @geofffranks
- @jrussett
- @pivotalgeorge
- @reneighbor
- @selzoc

Networking:
- @46bit
- @acrmp
- @aminjam
- @Benjamintf1
- @ctlong
- @domdom82
- @geofffranks
- @Gerg
- @jrussett
- @mkocher
- @pivotalgeorge
- @plowin
- @reneighbor
- @selzoc
- @stefanlay


## Technical Assets

Components from the Diego, Garden, HAproxy, Logging and Metrics, Networking, Windows Containers projects.

### Diego
* https://github.com/cloudfoundry/diego-release
  * https://github.com/cloudfoundry/archiver
  * https://github.com/cloudfoundry/auction
  * https://github.com/cloudfoundry/auctioneer
  * https://github.com/cloudfoundry/bbs
  * https://github.com/cloudfoundry/benchmarkbbs
  * https://github.com/cloudfoundry/bytefmt
  * https://github.com/cloudfoundry/cacheddownloader
  * https://github.com/cloudfoundry/certsplitter
  * https://github.com/cloudfoundry/cfdot
  * https://github.com/cloudfoundry/cf-volume-services-acceptance-tests
  * https://github.com/cloudfoundry/clock
  * https://github.com/cloudfoundry/consuladapter
  * https://github.com/cloudfoundry/debugserver
  * https://github.com/cloudfoundry/diego-dockerfiles
  * https://github.com/cloudfoundry/diego-logging-client
  * https://github.com/cloudfoundry/diego-upgrade-stability-tests
  * https://github.com/cloudfoundry/dockerdriver
  * https://github.com/cloudfoundry/docker_driver_integration_tests
  * https://github.com/cloudfoundry/durationjson
  * https://github.com/cloudfoundry/ecrhelper
  * https://github.com/cloudfoundry/eventhub
  * https://github.com/cloudfoundry/executor
  * https://github.com/cloudfoundry/fileserver
  * https://github.com/cloudfoundry/healthcheck
  * https://github.com/cloudfoundry/inigo
  * https://github.com/cloudfoundry/localdriver
  * https://github.com/cloudfoundry/localip
  * https://github.com/cloudfoundry/locket
  * https://github.com/cloudfoundry/operationq
  * https://github.com/cloudfoundry/rep
  * https://github.com/cloudfoundry/route-emitter
  * https://github.com/cloudfoundry/systemcerts
  * https://github.com/cloudfoundry/tlsconfig
  * https://github.com/cloudfoundry/vizzini
  * https://github.com/cloudfoundry/volman
  * https://github.com/cloudfoundry/volumedriver
  * https://github.com/cloudfoundry/workpool

### Garden Containers
* https://github.com/cloudfoundry/garden-runc-release
  * https://github.com/cloudfoundry/dontpanic/
  * https://github.com/cloudfoundry/garden
  * https://github.com/cloudfoundry/garden-integration-tests
  * https://github.com/cloudfoundry/grootfs
  * https://github.com/cloudfoundry/guardian
  * https://github.com/cloudfoundry/idmapper
  * https://github.com/cloudfoundry/netplugin-shim
  * https://github.com/cloudfoundry/cpu-entitlement-plugin
  * https://github.com/cloudfoundry/cpu-entitlement-admin-plugin
* https://github.com/cloudfoundry/winc-release
  * https://github.com/cloudfoundry/winc
  * https://github.com/cloudfoundry/groot-windows
  * https://github.com/cloudfoundry-incubator/diff-exporter
  * https://github.com/cloudfoundry/cert-injector


### Logging and Metrics
* https://github.com/cloudfoundry/bosh-system-metrics-forwarder-release
* https://github.com/cloudfoundry/log-cache-release
* https://github.com/cloudfoundry/loggregator-release
* https://github.com/cloudfoundry/loggregator-agent-release
* https://github.com/cloudfoundry/metrics-discovery-release
* https://github.com/cloudfoundry/statsd-injector-release
* https://github.com/cloudfoundry/syslog-release
* https://github.com/cloudfoundry/system-metrics-scraper-release

### Networking
* http://github.com/cloudfoundry/routing-release
  * https://github.com/cloudfoundry/routing-acceptance-tests
  * https://github.com/cloudfoundry/routing-api
  * https://github.com/cloudfoundry/routing-api-cli
  * https://github.com/cloudfoundry/routing-perf-release
  * https://github.com/cloudfoundry/cf-tcp-router
  * https://github.com/cloudfoundry/routing-info
  * https://github.com/cloudfoundry/gorouter
  * https://github.com/cloudfoundry/route-registrar
* https://github.com/cloudfoundry-incubator/haproxy-boshrelease
* https://github.com/cloudfoundry/cf-networking-release
  * https://github.com/cloudfoundry/networking-oss-deployments
  * https://github.com/cloudfoundry/cf-networking-helpers
* https://github.com/cloudfoundry/silk-release
  * https://github.com/cloudfoundry/silk/
* https://github.com/cloudfoundry/nats-release




