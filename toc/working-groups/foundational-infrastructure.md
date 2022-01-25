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
execution_leads:
- name: Ruben Koster
  github: rkoster
technical_leads:
- name: Ruben Koster
  github: rkoster
- name: Beyhan Veli
  github: beyhan
areas:
- name: Credential Management (Credhub)
  approvers:
  - name: Peter Chen
    github: peterhaochen47
  repositories:
  - cloudfoundry-incubator/credhub-acceptance-tests
  - cloudfoundry-incubator/credhub-api-site
  - cloudfoundry-incubator/credhub-ci-locks
  - cloudfoundry-incubator/credhub-cli
  - cloudfoundry-incubator/credhub-perf-release
  - cloudfoundry-incubator/credhub
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
  - cloudfoundry-incubator/bosh-backup-and-restore
  - cloudfoundry-incubator/backup-and-restore-sdk-release
  - cloudfoundry-incubator/bosh-backup-and-restore-test-releases
  - cloudfoundry-incubator/bosh-disaster-recovery-acceptance-tests
  - cloudfoundry-incubator/disaster-recovery-acceptance-tests
  - cloudfoundry-incubator/exemplar-backup-and-restore-release
  - cloudfoundry/docs-bbr
- name: Identity and Auth (UAA)
  approvers:
  - name: Peter Chen 
    github: peterhaochen47
  - name: Markus Strehle
    github: strehle
  repositories:
  - cloudfoundry/cf-uaa-lib
  - cloudfoundry/cf-uaac
  - cloudfoundry/omniauth-uaa-oauth2
  - cloudfoundry/uaa-key-rotator
  - cloudfoundry/uaa-release
  - cloudfoundry/uaa-singular
  - cloudfoundry/uaa
- name: Integrated Databases
  approvers:
  - name: Andrew Garner 
    github: abg
  - name: Shaan Sapra
    github: ssapra
  repositories:
  - cloudfoundry-incubator/cf-mysql-ci
  - cloudfoundry-incubator/mysql-backup-release
  - cloudfoundry-incubator/mysql-monitoring-release
  - cloudfoundry-incubator/pxc-release
  - cloudfoundry/cf-mysql-deployment
  - cloudfoundry/cf-mysql-release
  - cloudfoundry/galera-init
  - cloudfoundry/postgres-release
- name: System logging and metrics
  approvers:
  - name: Ben Fuller
    github: Benjamintf1
  repositories:
  - cloudfoundry-incubator/event-log-release
  - cloudfoundry/syslog-release
  - cloudfoundry/windows-syslog-release
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
  - name: Felix Riegger
    github: friegger
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
  - cloudfoundry-incubator/bosh-alicloud-light-stemcell-builder
  - cloudfoundry-incubator/bosh-cpi-certification
  - cloudfoundry-incubator/bosh-windows-acceptance-tests
  - cloudfoundry-incubator/bosh-windows-stemcell-builder
  - cloudfoundry-incubator/resolvconf-manager-index
  - cloudfoundry-incubator/resolvconf-manager
  - cloudfoundry-incubator/sample-windows-bosh-release
  - cloudfoundry-incubator/stembuild
  - cloudfoundry-incubator/stemcells-alicloud-index
  - cloudfoundry-incubator/windows-utilities-release
  - cloudfoundry-incubator/windows-utilities-tests
  - cloudfoundry/bosh-acceptance-tests
  - cloudfoundry/bosh-agent-index
  - cloudfoundry/bosh-agent
  - cloudfoundry/bosh-aws-cpi-release
  - cloudfoundry/bosh-aws-light-stemcell-builder
  - cloudfoundry/bosh-azure-cpi-release
  - cloudfoundry/bosh-bbl-ci-envs
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
  - cloudfoundry/bosh-s3cli
  - cloudfoundry/bosh-softlayer-cpi-release
  - cloudfoundry/bosh-stemcell-ci-infra
  - cloudfoundry/bosh-stemcells-ci
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
  - cloudfoundry/gofileutils
  - cloudfoundry/gosigar
  - cloudfoundry/os-conf-release
  - cloudfoundry/socks5-proxy
  - cloudfoundry/tlsconfig
  - cloudfoundry/usn-resource
  - cloudfoundry/yagnats
  - cloudfoundry/windows-tools-release
```

