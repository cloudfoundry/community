# Foundational Infrastructure: Working Group Charter

## Mission

Provide infrastructure automation and core capabilities shared across CF projects, including BOSH, identity management, credential management, and integrated data services.


## Goals

* Operators have a multi-cloud deployment system that can deploy Cloud Foundry onto VMs with a strong 
  set of day 2 operator features.
* Provide a flexible identity/authentication and credential management system for use within BOSH and Cloud Foundry.
* Maintain a set of databases, required for the self-contained deployment and operation of BOSH and Cloud Foundry. 

## Scope

* Maintain public roadmaps for BOSH, UAA, and Credhub
* Operate https://bosh.io
* Provide the community with a multi-cloud reference deployment of the BOSH Director
* Package up all infrastructure related components as BOSH releases 

## Non-Goals

* Provide generic operational databases for other use-cases
* Solve non-CF related identity and credential problems.

## Roles & Technical Assets

Components from the BOSH, BOSH Backup and Restore, CredHub, MySQL, Postgres, and UAA projects.

```yaml
name: Foundational Infrastructure
execution_leads:
- name: Ruben Koster
  github: rkoster
technical_leads:
- name: Ruben Koster
  github: rkoster
- name: Beyhan Veli
  github: beyhan
bots:
- name: bosh-admin-bot
  github: bosh-admin-bot
- name: cf-gitbot
  github: cf-gitbot
- name: runtime-bot
  github: tas-runtime-bot
- name: cf-uaa-ci-bot
  github: cf-identity
- name: cf-bosh-ci-bot
  github: cf-bosh-ci-bot
areas:
- name: Credential Management (Credhub)
  approvers:
  - name: Peter Chen
    github: peterhaochen47
  - name: Bruce Ricard
    github: bruce-ricard
  repositories:
  - cloudfoundry-incubator/credhub-api-docs
  - cloudfoundry/credhub
  - cloudfoundry/credhub-acceptance-tests
  - cloudfoundry/credhub-api-site
  - cloudfoundry/credhub-cli
  - cloudfoundry/credhub-ci-locks
  - cloudfoundry/credhub-perf-release
  - cloudfoundry/docs-credhub
  - cloudfoundry/secure-credentials-broker
- name: Disaster Recovery (BBR)
  approvers:
  - name: Diego Lemos
    github: dlresende
  - name: Fernando Naranjo
    github: fejnartal
  - name: Gareth Smith 
    github: totherme
  repositories:
  - cloudfoundry/backup-and-restore-sdk-release
  - cloudfoundry/bosh-backup-and-restore
  - cloudfoundry/bosh-backup-and-restore-test-releases
  - cloudfoundry/bosh-disaster-recovery-acceptance-tests
  - cloudfoundry/disaster-recovery-acceptance-tests
  - cloudfoundry/docs-bbr
  - cloudfoundry/exemplar-backup-and-restore-release
- name: Identity and Auth (UAA)
  approvers:
  - name: Peter Chen 
    github: peterhaochen47
  - name: Bruce Ricard
    github: bruce-ricard
  - name: Markus Strehle
    github: strehle
  repositories:
  - cloudfoundry/cf-identity-acceptance-tests-release
  - cloudfoundry/cf-uaa-lib
  - cloudfoundry/cf-uaac
  - cloudfoundry/docs-uaa
  - cloudfoundry/identity-tools
  - cloudfoundry/omniauth-uaa-oauth2
  - cloudfoundry/uaa
  - cloudfoundry/uaa-cli
  - cloudfoundry/uaa-k8s-release
  - cloudfoundry/uaa-key-rotator
  - cloudfoundry/uaa-release
  - cloudfoundry/uaa-singular
- name: Integrated Databases (Mysql / Postgres)
  approvers:
  - name: Andrew Garner 
    github: abg
  - name: Colin Shield
    github: colins
  - name: Kyle Ong
    github: ohkyle
  - name: Kim Basset
    github: kimago
  reviewers:
  - name: Ryan Wittrup
    github: ryanwittrup
  - name: Kevin Markwardt
    github: kmarkwardt-vmware
  repositories:
  - cloudfoundry/mysql-backup-release
  - cloudfoundry/mysql-monitoring-release
  - cloudfoundry/postgres-release
  - cloudfoundry/pxc-release
- name: System Logging and Metrics (rsyslog / event-log)
  approvers:
  - name: Ben Fuller
    github: Benjamintf1
  repositories:
  - cloudfoundry/blackbox
  - cloudfoundry/system-metrics-release
  - cloudfoundry/syslog-release
  - cloudfoundry/windows-syslog-release
- name: Stemcell Release Engineering (BOSH)
  approvers:
  - name: Joseph Palermo
    github: jpalermo
  - name: Rajan Agaskar
    github: ragaskar
  - name: Brian Upton
    github: ystros
  - name: Matthias Vach
    github: mvach
  - name: Long Nguyen
    github: lnguyen
  - name: Brian Cunnie
    github: cunnie
  - name: Ramon Makkelie
    github: ramonskie
  - name: Maya Rosecrance
    github: mrosecrance
  - name: Daniel Felipe Ochoa
    github: danielfor
  - name: Kenneth Lakin
    github: klakin-pivotal
  - name: Konstantin Kiess
    github: nouseforaname
  - name: Max Soest
    github: max-soe
  - name: Aram Price
    github: aramprice
  - name: Shilpa Chandrashekara
    github: ShilpaChandrashekara
  - name: Joerg W
    github: joergdw
  - name: Ansh Rupani
    github: anshrupani
  repositories:
  - cloudfoundry/bosh-community-stemcell-ci-infra
  - cloudfoundry/bosh-stemcells-ci
- name: VM deployment lifecycle (BOSH)
  approvers:
  - name: Joseph Palermo
    github: jpalermo
  - name: Long Nguyen
    github: lnguyen
  - name: Ramon Makkelie
    github: ramonskie
  - name: Benjamin Gandon 
    github: bgandon
  - name: Brian Cunnie
    github: cunnie
  - name: Aram Price
    github: aramprice
  reviewers:
  - name: Matthias Vach
    github: mvach
  repositories:
  - bosh-io/releases-index
  - bosh-io/releases
  - bosh-io/stemcells-core-index
  - bosh-io/stemcells-cpi-index
  - bosh-io/stemcells-legacy-index
  - bosh-io/stemcells-softlayer-index
  - bosh-io/stemcells-windows-index
  - bosh-io/web
  - bosh-io/worker
  - bosh-packages/cf-cli-release
  - bosh-packages/golang-release
  - bosh-packages/java-release
  - bosh-packages/nginx-release
  - bosh-packages/python-release
  - bosh-packages/ruby-release
  - cloudfoundry/bbl-state-resource
  - cloudfoundry/bosh-alicloud-light-stemcell-builder
  - cloudfoundry/bosh-cpi-certification
  - cloudfoundry/bosh-windows-acceptance-tests
  - cloudfoundry/bosh-windows-stemcell-builder
  - cloudfoundry/bosh-acceptance-tests
  - cloudfoundry/bosh-agent-index
  - cloudfoundry/bosh-agent
  - cloudfoundry/bosh-aws-cpi-release
  - cloudfoundry/bosh-aws-light-stemcell-builder
  - cloudfoundry/bosh-azure-cpi-release
  - cloudfoundry/bosh-bbl-ci-envs
  - cloudfoundry/bosh-bootloader
  - cloudfoundry/bosh-cli
  - cloudfoundry/bosh-community-stemcell-ci-infra
  - cloudfoundry/bosh-compiled-releases-index
  - cloudfoundry/bosh-cpi-environments
  - cloudfoundry/bosh-cpi-go
  - cloudfoundry/bosh-cpi-kb
  - cloudfoundry/bosh-cpi-ruby
  - cloudfoundry/bosh-davcli
  - cloudfoundry/bosh-deployment-resource
  - cloudfoundry/bosh-deployment
  - cloudfoundry/bosh-dns-aliases-release
  - cloudfoundry/bosh-dns-release
  - cloudfoundry/bosh-docker-cpi-release
  - cloudfoundry/bosh-gcscli
  - cloudfoundry/bosh-google-cpi-release
  - cloudfoundry/bosh-google-light-stemcell-builder
  - cloudfoundry/bosh-linux-stemcell-builder
  - cloudfoundry/bosh-openstack-cpi-release
  - cloudfoundry/bosh-psmodules
  - cloudfoundry/bosh-s3cli
  - cloudfoundry/bosh-softlayer-cpi-release
  - cloudfoundry/bosh-utils
  - cloudfoundry/bosh-virtualbox-cpi-release
  - cloudfoundry/bosh-vsphere-cpi-release
  - cloudfoundry/bosh-warden-cpi-release
  - cloudfoundry/bosh-workstation
  - cloudfoundry/bosh
  - cloudfoundry/bpm-release
  - cloudfoundry/bsdtar
  - cloudfoundry/config-server-release
  - cloudfoundry/config-server
  - cloudfoundry/docs-bosh
  - cloudfoundry/exemplar-release
  - cloudfoundry/go-socks5
  - cloudfoundry/gofileutils
  - cloudfoundry/gosigar
  - cloudfoundry/greenhouse-ci
  - cloudfoundry/jumpbox-deployment
  - cloudfoundry/os-conf-release
  - cloudfoundry/resolvconf-manager
  - cloudfoundry/resolvconf-manager-index
  - cloudfoundry/sample-windows-bosh-release
  - cloudfoundry/stembuild
  - cloudfoundry/stemcells-alicloud-index
  - cloudfoundry/socks5-proxy
  - cloudfoundry/bosh-system-metrics-server-release
  - cloudfoundry/tlsconfig
  - cloudfoundry/usn-resource
  - cloudfoundry/windows-utilities-release
  - cloudfoundry/windows-utilities-tests
  - cloudfoundry/windows-tools-release
  - cloudfoundry/yagnats
config:
  github_project_sync:
    mapping:
      cloudfoundry: 21
```
