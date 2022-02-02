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

## Technical Lead(s):
- Ruben Koster (@rkoster)
- Beyhan Veli (@beyhan)

## Execution Lead(s):
- Ruben Koster (@rkoster)

## Approvers (by Area):
### VM deployment lifecycle (BOSH)
- Joseph Palermo (@jpalermo)
- Long Nguyen (@lnguyen)
- Ramon Makkelie (@ramonskie)
- Benjamin Gandon (@bgandon)
- Kai Hofstetter (@KaiHofstetter)
- Felix Riegger (@friegger)

### Disaster Recovery (BBR)
- Diego Lemos (@dlresende)
- Fernando Naranjo (@fejnartal)
- Gareth Smith (@totherme)

### Identity and Auth (UAA)
- Peter Chen (@peterhaochen47)
- Markus Strehle (@strehle)

### Credential Management (Credhub)
- Peter Chen (@peterhaochen47)

### Integrated Databases
- Andrew Garner (@abg)
- Shaan Sapra (@ssapra)

### System logging and metrics
- Ben Fuller (@Benjamintf1)

## Technical Assets

Components from the BOSH, BOSH Backup and Restore, CredHub, MySQL, Postgres, and UAA projects.

### VM deployment lifecycle (BOSH)
- [bosh-io/releases-index](https://github.com/bosh-io/releases-index)
- [bosh-io/releases](https://github.com/bosh-io/releases)
- [bosh-io/stemcells-core-index](https://github.com/bosh-io/stemcells-core-index)
- [bosh-io/stemcells-cpi-index](https://github.com/bosh-io/stemcells-cpi-index)
- [bosh-io/stemcells-legacy-index](https://github.com/bosh-io/stemcells-legacy-index)
- [bosh-io/stemcells-softlayer-index](https://github.com/bosh-io/stemcells-softlayer-index)
- [bosh-io/stemcells-windows-index](https://github.com/bosh-io/stemcells-windows-index)
- [bosh-io/web](https://github.com/bosh-io/web)
- [bosh-io/worker](https://github.com/bosh-io/worker)
- [bosh-packages/cf-cli-release](https://github.com/bosh-packages/cf-cli-release)
- [bosh-packages/golang-release](https://github.com/bosh-packages/golang-release)
- [bosh-packages/java-release](https://github.com/bosh-packages/java-release)
- [bosh-packages/nginx-release](https://github.com/bosh-packages/nginx-release)
- [bosh-packages/python-release](https://github.com/bosh-packages/python-release)
- [bosh-packages/ruby-release](https://github.com/bosh-packages/ruby-release)
- [cloudfoundry/bosh-alicloud-light-stemcell-builder](https://github.com/cloudfoundry/bosh-alicloud-light-stemcell-builder)
- [cloudfoundry/bosh-cpi-certification](https://github.com/cloudfoundry/bosh-cpi-certification)
- [cloudfoundry/bosh-windows-acceptance-tests](https://github.com/cloudfoundry/bosh-windows-acceptance-tests)
- [cloudfoundry/bosh-windows-stemcell-builder](https://github.com/cloudfoundry/bosh-windows-stemcell-builder)
- [cloudfoundry/resolvconf-manager-index](https://github.com/cloudfoundry/resolvconf-manager-index)
- [cloudfoundry/resolvconf-manager](https://github.com/cloudfoundry/resolvconf-manager)
- [cloudfoundry/sample-windows-bosh-release](https://github.com/cloudfoundry/sample-windows-bosh-release)
- [cloudfoundry/stembuild](https://github.com/cloudfoundry/stembuild)
- [cloudfoundry/stemcells-alicloud-index](https://github.com/cloudfoundry/stemcells-alicloud-index)
- [cloudfoundry/windows-utilities-release](https://github.com/cloudfoundry/windows-utilities-release)
- [cloudfoundry/windows-utilities-tests](https://github.com/cloudfoundry/windows-utilities-tests)
- [cloudfoundry/bosh-acceptance-tests](https://github.com/cloudfoundry/bosh-acceptance-tests)
- [cloudfoundry/bosh-agent-index](https://github.com/cloudfoundry/bosh-agent-index)
- [cloudfoundry/bosh-agent](https://github.com/cloudfoundry/bosh-agent)
- [cloudfoundry/bosh-aws-cpi-release](https://github.com/cloudfoundry/bosh-aws-cpi-release)
- [cloudfoundry/bosh-aws-light-stemcell-builder](https://github.com/cloudfoundry/bosh-aws-light-stemcell-builder)
- [cloudfoundry/bosh-azure-cpi-release](https://github.com/cloudfoundry/bosh-azure-cpi-release)
- [cloudfoundry/bosh-bbl-ci-envs](https://github.com/cloudfoundry/bosh-bbl-ci-envs)
- [cloudfoundry/bosh-cli](https://github.com/cloudfoundry/bosh-cli)
- [cloudfoundry/bosh-community-stemcell-ci-infra](https://github.com/cloudfoundry/bosh-community-stemcell-ci-infra)
- [cloudfoundry/bosh-compiled-releases-index](https://github.com/cloudfoundry/bosh-compiled-releases-index)
- [cloudfoundry/bosh-cpi-environments](https://github.com/cloudfoundry/bosh-cpi-environments)
- [cloudfoundry/bosh-cpi-go](https://github.com/cloudfoundry/bosh-cpi-go)
- [cloudfoundry/bosh-cpi-kb](https://github.com/cloudfoundry/bosh-cpi-kb)
- [cloudfoundry/bosh-cpi-ruby](https://github.com/cloudfoundry/bosh-cpi-ruby)
- [cloudfoundry/bosh-davcli](https://github.com/cloudfoundry/bosh-davcli)
- [cloudfoundry/bosh-deployment-resource](https://github.com/cloudfoundry/bosh-deployment-resource)
- [cloudfoundry/bosh-deployment](https://github.com/cloudfoundry/bosh-deployment)
- [cloudfoundry/bosh-dns-aliases-release](https://github.com/cloudfoundry/bosh-dns-aliases-release)
- [cloudfoundry/bosh-dns-release](https://github.com/cloudfoundry/bosh-dns-release)
- [cloudfoundry/bosh-docker-cpi-release](https://github.com/cloudfoundry/bosh-docker-cpi-release)
- [cloudfoundry/bosh-gcscli](https://github.com/cloudfoundry/bosh-gcscli)
- [cloudfoundry/bosh-google-cpi-release](https://github.com/cloudfoundry/bosh-google-cpi-release)
- [cloudfoundry/bosh-google-light-stemcell-builder](https://github.com/cloudfoundry/bosh-google-light-stemcell-builder)
- [cloudfoundry/bosh-linux-stemcell-builder](https://github.com/cloudfoundry/bosh-linux-stemcell-builder)
- [cloudfoundry/bosh-openstack-cpi-release](https://github.com/cloudfoundry/bosh-openstack-cpi-release)
- [cloudfoundry/bosh-s3cli](https://github.com/cloudfoundry/bosh-s3cli)
- [cloudfoundry/bosh-softlayer-cpi-release](https://github.com/cloudfoundry/bosh-softlayer-cpi-release)
- [cloudfoundry/bosh-stemcell-ci-infra](https://github.com/cloudfoundry/bosh-stemcell-ci-infra)
- [cloudfoundry/bosh-stemcells-ci](https://github.com/cloudfoundry/bosh-stemcells-ci)
- [cloudfoundry/bosh-utils](https://github.com/cloudfoundry/bosh-utils)
- [cloudfoundry/bosh-virtualbox-cpi-release](https://github.com/cloudfoundry/bosh-virtualbox-cpi-release)
- [cloudfoundry/bosh-vsphere-cpi-release](https://github.com/cloudfoundry/bosh-vsphere-cpi-release)
- [cloudfoundry/bosh-warden-cpi-release](https://github.com/cloudfoundry/bosh-warden-cpi-release)
- [cloudfoundry/bosh-workstation](https://github.com/cloudfoundry/bosh-workstation)
- [cloudfoundry/bosh](https://github.com/cloudfoundry/bosh)
- [cloudfoundry/bpm-release](https://github.com/cloudfoundry/bpm-release)
- [cloudfoundry/bsdtar](https://github.com/cloudfoundry/bsdtar)
- [cloudfoundry/config-server-release](https://github.com/cloudfoundry/config-server-release)
- [cloudfoundry/config-server](https://github.com/cloudfoundry/config-server)
- [cloudfoundry/docs-bosh](https://github.com/cloudfoundry/docs-bosh)
- [cloudfoundry/gofileutils](https://github.com/cloudfoundry/gofileutils)
- [cloudfoundry/gosigar](https://github.com/cloudfoundry/gosigar)
- [cloudfoundry/greenhouse-ci](https://github.com/cloudfoundry/greenhouse-ci)
- [cloudfoundry/os-conf-release](https://github.com/cloudfoundry/os-conf-release)
- [cloudfoundry/socks5-proxy](https://github.com/cloudfoundry/socks5-proxy)
- [cloudfoundry/tlsconfig](https://github.com/cloudfoundry/tlsconfig)
- [cloudfoundry/usn-resource](https://github.com/cloudfoundry/usn-resource)
- [cloudfoundry/yagnats](https://github.com/cloudfoundry/yagnats)
- [cloudfoundry/windows-tools-release](https://github.com/cloudfoundry/windows-tools-release)

### Disaster Recovery (BBR)
- [cloudfoundry/bosh-backup-and-restore](https://github.com/cloudfoundry/bosh-backup-and-restore)
- [cloudfoundry/backup-and-restore-sdk-release](https://github.com/cloudfoundr/backup-and-restore-sdk-release)
- [cloudfoundry/bosh-backup-and-restore-test-releases](https://github.com/cloudfoundry/bosh-backup-and-restore-test-releases)
- [cloudfoundry/bosh-disaster-recovery-acceptance-tests](https://github.com/cloudfoundry/bosh-disaster-recovery-acceptance-tests)
- [cloudfoundry/disaster-recovery-acceptance-tests](https://github.com/cloudfoundry/disaster-recovery-acceptance-tests)
- [cloudfoundry/exemplar-backup-and-restore-release](https://github.com/cloudfoundry/exemplar-backup-and-restore-release)
- [cloudfoundry/docs-bbr](https://github.com/cloudfoundry/docs-bbr)

### Identity and Auth (UAA)
- [cloudfoundry/cf-uaa-lib](https://github.com/cloudfoundry/cf-uaa-lib)
- [cloudfoundry/cf-uaac](https://github.com/cloudfoundry/cf-uaac)
- [cloudfoundry/docs-uaa](https://github.com/cloudfoundry/docs-uaa)
- [cloudfoundry/omniauth-uaa-oauth2](https://github.com/cloudfoundry/omniauth-uaa-oauth2)
- [cloudfoundry/uaa-key-rotator](https://github.com/cloudfoundry/uaa-key-rotator)
- [cloudfoundry/uaa-release](https://github.com/cloudfoundry/uaa-release)
- [cloudfoundry/uaa-singular](https://github.com/cloudfoundry/uaa-singular)
- [cloudfoundry/uaa](https://github.com/cloudfoundry/uaa)

### Credential Management (Credhub)
- [cloudfoundry/credhub-acceptance-tests](https://github.com/cloudfoundry-incubator/credhub-acceptance-tests)
- [cloudfoundry/credhub-api-docs](https://github.com/cloudfoundry/credhub-api-docs)
- [cloudfoundry/credhub-api-site](https://github.com/cloudfoundry/credhub-api-site)
- [cloudfoundry/credhub-ci-locks](https://github.com/cloudfoundry/credhub-ci-locks)
- [cloudfoundry/credhub-cli](https://github.com/cloudfoundry/credhub-cli)
- [cloudfoundry/credhub-perf-release](https://github.com/cloudfoundry/credhub-perf-release)
- [cloudfoundry/credhub](https://github.com/cloudfoundry/credhub)
- [cloudfoundry/docs-credhub](https://github.com/cloudfoundry/docs-credhub)
- [cloudfoundry/secure-credentials-broker](https://github.com/cloudfoundry/secure-credentials-broker)

### Integrated Databases
- [cloudfoundry/cf-mysql-bootstrap](https://github.com/cloudfoundry/cf-mysql-bootstrap)
- [cloudfoundry/cf-mysql-ci](https://github.com/cloudfoundry/cf-mysql-ci)
- [cloudfoundry/cf-mysql-cluster-health-logger](https://github.com/cloudfoundry/cf-mysql-cluster-health-logger)
- [cloudfoundry/mysql-backup-release](https://github.com/cloudfoundry/mysql-backup-release)
- [cloudfoundry/mysql-monitoring-release](https://github.com/cloudfoundry/mysql-monitoring-release)
- [cloudfoundry/pxc-release](https://github.com/cloudfoundry/pxc-release)
- [cloudfoundry/cf-mysql-deployment](https://github.com/cloudfoundry/cf-mysql-deployment)
- [cloudfoundry/cf-mysql-release](https://github.com/cloudfoundry/cf-mysql-release)
- [cloudfoundry/galera-healthcheck](https://github.com/cloudfoundry/galera-healthcheck)
- [cloudfoundry/galera-init](https://github.com/cloudfoundry/galera-init)
- [cloudfoundry/postgres-release](https://github.com/cloudfoundry/postgres-release)
- [cloudfoundry/switchboard](https://github.com/cloudfoundry/switchboard)

### System logging and metrics
- [cloudfoundry/event-log-release](https://github.com/cloudfoundry/event-log-release)
- [cloudfoundry/syslog-release](https://github.com/cloudfoundry/syslog-release)
- [cloudfoundry/windows-syslog-release](https://github.com/cloudfoundry/windows-syslog-release)
