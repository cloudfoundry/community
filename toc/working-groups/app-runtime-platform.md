# App Runtime Platform: Working Group Charter

## Mission

Provides operational components for the CF App Runtime, including those for application build, application execution, ingress and app-to-app routing, volume service adapters, and aggregation of application logs and metrics.


## Goals

- End-user platform teams have reliable, performant, and well-documented system components to provide core CF App Runtime capabilities within BOSH-based deployments.
- Community contributors can build against core CF App Runtime system components via stable, well-documented APIs.
- Community contributors can integrate tested CF App Runtime components into community reference deployments.


## Scope

- Develop system components that support core CF App Runtime capabilities, including building app artifacts from source code, running artifacts as apps, routing traffic to apps and between apps,  mouting stateful data to apps via volume services, and aggregating logs and metrics from applications for end-user consumption.
- Maintain public roadmaps for the CF App Runtime component systems above and ensure that system component development matches roadmap intent.
- Align component development to the priorities of App Runtime end users via collaboration with other Working Groups.
- Provide community contributors with tooling and reference pipelines needed to build, test, and release App Runtime system components.
- Collaborate with other Working Groups to ensure that App Runtime components are integrated regularly into the community reference deployments.
- Maintain documentation for system component APIs, including which API groups are stable for use or are experimental and which API groups are intended for end-user internal use.
- Ensure upgrade pathways for system components, with disruptive changes communicated clearly.



## Non-Goals

- Be responsible for these functional domain areas outside of the CF App Runtime system.

## Roles & Technical Assets

Components from the Diego, Garden, HAproxy, Logging and Metrics, Networking, Volume Services, Windows Containers projects.

```yaml
name: App Runtime Platform
execution_leads:
- name: Amelia Downs
  github: ameowlia
technical_leads:
- name: Amelia Downs
  github: ameowlia
bots:
- name: CI Bot
  github: tas-runtime-bot
- name: Networking CI Bot
  github: CFN-CI
- name: CF Logging and Metrics Bot
  github: cf-logging-metrics-bot
- name: Metric Store Bot
  github: svcboteos
- name: Cryogenics CI bot
  github: Cryogenics-CI
config:
  generate_rfc0015_branch_protection_rules: true
  github_project_sync:
    mapping:
      cloudfoundry: 41
areas:
- name: cnbapplifecycle
  approvers:
  - name: Jan von Löwenstein
    github: loewenstein-sap
  - name: Pavel Busko
    github: pbusko
  - name: Johannes Dillmann
    github: modulo11
  - name: Ralf Pannemans
    github: c0d1ngm0nk3y
  - name: Nicolas Bender
    github: nicolasbender
  repositories:
  - cloudfoundry/cnbapplifecycle
- name: Diego
  approvers:
  - name: Andrew Crump
    github: acrmp
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Brandon Roberson
    github: ebroberson
  - name: Geoff Franks
    github: geofffranks
  - name: Josh Russett
    github: jrussett
  - name: Maria Shaldybin
    github: mariash
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  - name: Amin Jamali
    github: winkingturtle-vmw
  - name: David Sabeti
    github: dsabeti
  - name: Marc Paquette
    github: marcpaquette
  - name: Vladimir Savchenko
    github: vlast3k
  - name: Plamen Doychev
    github: PlamenDoychev
  reviewers:
  - name: Konstantin Lapkov
    github: klapkov
  - name: Tim Downey
    github: tcdowney
  repositories:
  - cloudfoundry/archiver
  - cloudfoundry/auction
  - cloudfoundry/auctioneer
  - cloudfoundry/bbs
  - cloudfoundry/buildpackapplifecycle
  - cloudfoundry/bytefmt
  - cloudfoundry/cacheddownloader
  - cloudfoundry/certsplitter
  - cloudfoundry/cfdot
  - cloudfoundry/cfhttp
  - cloudfoundry/clock
  - cloudfoundry/debugserver
  - cloudfoundry/runtime-ci-pools
  - cloudfoundry/diego-logging-client
  - cloudfoundry/diego-release
  - cloudfoundry/diego-ssh
  - cloudfoundry/diego-upgrade-stability-tests
  - cloudfoundry/dockerapplifecycle
  - cloudfoundry/dockerdriver
  - cloudfoundry/durationjson
  - cloudfoundry/ecrhelper
  - cloudfoundry/eventhub
  - cloudfoundry/executor
  - cloudfoundry/fileserver
  - cloudfoundry/grace
  - cloudfoundry/healthcheck
  - cloudfoundry/inigo
  - cloudfoundry/lager
  - cloudfoundry/localdriver
  - cloudfoundry/localip
  - cloudfoundry/locket
  - cloudfoundry/operationq
  - cloudfoundry/rep
  - cloudfoundry/route-emitter
  - cloudfoundry/tlsconfig
  - cloudfoundry/vizzini
  - cloudfoundry/volman
  - cloudfoundry/workpool
  - cloudfoundry/wg-app-platform-runtime-ci

- name: Garden Containers
  approvers:
  - name: Danail Branekov
    github: danail-branekov
  - name: George
    github: georgethebeatle
  - name: Geoff Franks
    github: geofffranks
  - name: Josh Russett
    github: jrussett
  - name: Renee Chu
    github: reneighbor
  - name: Maria Shaldybin
    github: mariash
  - name: David Sabeti
    github: dsabeti
  - name: Marc Paquette
    github: MarcPaquette
  - name: Chris Selzo
    github: selzoc
  - name: Amin Jamali
    github: winkingturtle-vmw
  - name: Brandon Roberson
    github: ebroberson
  repositories:
  - cloudfoundry/cert-injector
  - cloudfoundry/commandrunner
  - cloudfoundry/diff-exporter
  - cloudfoundry/dontpanic
  - cloudfoundry/envoy-nginx-release
  - cloudfoundry/filelock
  - cloudfoundry/garden
  - cloudfoundry/garden-integration-tests
  - cloudfoundry/garden-performance-acceptance-tests
  - cloudfoundry/garden-runc-release
  - cloudfoundry/groot
  - cloudfoundry/groot-windows
  - cloudfoundry/grootfs
  - cloudfoundry/guardian
  - cloudfoundry/hwc
  - cloudfoundry/hydrator
  - cloudfoundry/idmapper
  - cloudfoundry/netplugin-shim
  - cloudfoundry/test-log-emitter
  - cloudfoundry/test-log-emitter-release
  - cloudfoundry/winc
  - cloudfoundry/winc-release
  - cloudfoundry/windows-tools-release
  - cloudfoundry/windows2016fs
  - cloudfoundry/windows2019fs-release
  - cloudfoundry/windowsfs-online-release

- name: Logging and Metrics
  approvers:
  - name: Andrew Crump
    github: acrmp
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Geoff Franks
    github: geofffranks
  - name: Josh Russett
    github: jrussett
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  - name: Carson Long
    github: ctlong
  - name: Matthew Kocher
    github: mkocher
  - name: Amin Jamali
    github: winkingturtle-vmw
  - name: Rebecca Roberts
    github: rroberts2222
  - name: Jovan Kostovski
    github: chombium
  reviewers:
  - name: Felix Hambrecht
    github: fhambrec
  - name: Glenn Oppegard
    github: oppegard
  - name: Ausaf Ahmed
    github: aqstack
  - name: Ivan Protsiuk
    github: iprotsiuk
  - name: Andrew Costa
    github: acosta11
  repositories:
  - cloudfoundry/app-runtime-platform-envs
  - cloudfoundry/bosh-system-metrics-forwarder-release
  - cloudfoundry/dropsonde
  - cloudfoundry/dropsonde-protocol
  - cloudfoundry/dropsonde-protocol-js
  - cloudfoundry/go-batching
  - cloudfoundry/go-diodes
  - cloudfoundry/go-envstruct
  - cloudfoundry/go-log-cache
  - cloudfoundry/go-loggregator
  - cloudfoundry/go-metric-registry
  - cloudfoundry/go-orchestrator
  - cloudfoundry/go-pubsub
  - cloudfoundry/log-cache-cli
  - cloudfoundry/log-cache-release
  - cloudfoundry/loggregator-agent-release
  - cloudfoundry/loggregator-api
  - cloudfoundry/loggregator-dotfiles
  - cloudfoundry/loggregator-release
  - cloudfoundry/loggregator-tools
  - cloudfoundry/metrics-discovery-release
  - cloudfoundry/noaa
  - cloudfoundry/otel-collector-release
  - cloudfoundry/service-metrics-release
  - cloudfoundry/sonde-go
  - cloudfoundry/statsd-injector-release
  - cloudfoundry/system-metrics-scraper-release

- name: Metric Store
  approvers:
  - name: Jeanette Booher
    github: jbooherl
  - name: Aditya Choudhary
    github: aditya267vmware
  - name: Chaitanya Krishna Mullangi
    github: chaitanyamullangi
  - name: Dibyajyoti Mohapatra
    github: dibya1947
  - name: Kanika Bathla
    github: kabathla
  - name: Karthik Seshadri
    github: karthikseshadri
  - name: Mervin Nirmal John M W
    github: jmervinnirma
  - name: Mohammed Thavaf A R
    github: m-thavaf
  - name: Mukesh Khicher
    github: mukeshkhicher-br
  - name: Nakul Ogale
    github: nakulogale-cb
  - name: Pranay Raj
    github: rpranay1
  - name: Puja Kumari
    github: kpujadev
  - name: Radhakrishnan Devarajan
    github: radhavmwtnz
  - name: Saloni Shah
    github: saloni-sshah
  - name: Sanand Dange
    github: dsanand22
  - name: Shefali Dubey
    github: dubeyshefali
  - name: Shrisha Chandrashekar
    github: shrisha-c
  - name: Siddartha Laxman Karibhimanvar
    github: siddarthalk
  - name: Srinivas Sunka
    github: ssunka
  - name: Sudharsan G V
    github: sg038444
  repositories:
  - cloudfoundry/metric-store-ci
  - cloudfoundry/metric-store-release
  - cloudfoundry/metric-store-dotfiles

- name: Networking
  approvers:
  - name: Andrew Crump
    github: acrmp
  - name: Tamara Boehm
    github: b1tamara
  - name: Benjamin Fuller
    github: Benjamintf1
  - name: Brandon Roberson
    github: ebroberson
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
  - name: Maria Shaldybin
    github: mariash
  - name: Matthew Kocher
    github: mkocher
  - name: Patrick Lowin
    github: plowin
  - name: Renee Chu
    github: reneighbor
  - name: Chris Selzo
    github: selzoc
  - name: Stefan Lay
    github: stefanlay
  - name: Amin Jamali
    github: winkingturtle-vmw
  - name: David Sabeti
    github: dsabeti
  - name: Maximilian Moehl
    github: maxmoehl
  - name: Marc Paquette
    github: MarcPaquette
  - name: Vladimir Savchenko
    github: vlast3k
  - name: Alexander Lais
    github: peanball
  - name: Plamen Doychev
    github: PlamenDoychev
  reviewers:
  - name: Soha Alboghdady
    github: Soha-Albaghdady
  - name: Daria Anton
    github: Dariquest
  - name: Clemens Hoffmann
    github: hoffmaen
  - name: Konstantin Lapkov
    github: klapkov
  - name: Alexander Nicke
    github: a18e
  - name: M Rizwan Shaik
    github: Mrizwanshaik
  - name: Michal Tekel
    github: mtekel
  - name: Tim Downey
    github: tcdowney
  repositories:
  - cloudfoundry/cf-lookup-route
  - cloudfoundry/cf-networking-helpers
  - cloudfoundry/cf-networking-onboarding
  - cloudfoundry/cf-networking-release
  - cloudfoundry/cf-routing-test-helpers
  - cloudfoundry/cf-tcp-router
  - cloudfoundry/gorouter
  - cloudfoundry/healthchecker-release
  - cloudfoundry/multierror
  - cloudfoundry/nats-release
  - cloudfoundry/policy_client
  - cloudfoundry/route-registrar
  - cloudfoundry/routing-acceptance-tests
  - cloudfoundry/routing-api
  - cloudfoundry/routing-api-cli
  - cloudfoundry/routing-concourse
  - cloudfoundry/routing-info
  - cloudfoundry/routing-release
  - cloudfoundry/silk-release

- name: Networking-Extensions
  approvers:
  - name: Alexander Lais
    github: peanball
  - name: Dominik Froehlich
    github: domdom82
  - name: Maximilian Moehl
    github: maxmoehl
  - name: Patrick Lowin
    github: plowin
  - name: Tamara Boehm
    github: b1tamara
  reviewers:
  - name: Soha Alboghdady
    github: Soha-Albaghdady
  - name: Daria Anton
    github: Dariquest
  - name: Clemens Hoffmann
    github: hoffmaen
  - name: Konstantin Lapkov
    github: klapkov
  - name: Alexander Nicke
    github: a18e
  - name: M Rizwan Shaik
    github: Mrizwanshaik
  - name: Michal Tekel
    github: mtekel
  repositories:
  - cloudfoundry/haproxy-boshrelease
  - cloudfoundry/pcap
  - cloudfoundry/pcap-release

- name: Volume Services
  approvers:
  - name: Geoff Franks
    github: geofffranks
  - name: Maria Shaldybin
    github: mariash
  - name: Amin Jamali
    github: winkingturtle-vmw
  - name: Marc Paquette
    github: marcpaquette
  bots:
  - name: Cryogenics CI Bot
    github: Cryogenics-CI
  - name: CI Bot
    github: tas-runtime-bot
  repositories:
  - cloudfoundry/existingvolumebroker
  - cloudfoundry/goshims
  - cloudfoundry/mapfs-release
  - cloudfoundry/migrate_mysql_to_credhub
  - cloudfoundry/nfs-volume-release
  - cloudfoundry/service-broker-store
  - cloudfoundry/smb-volume-release
  - cloudfoundry/volume-mount-options
  - cloudfoundry/volumedriver
  - cloudfoundry/cf-volume-services-acceptance-tests

```
