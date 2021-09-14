# Foundational Infrastructure: Working Group Charter

## Mission

Provide infrastructure automation and core capabilities shared across CF projects, including BOSH, identity management, credential management, and integrated data services.


## Goals

* Operators have a multi-cloud deployment system that can  deploy Cloud Foundry onto VMs with a strong 
  set of day 2 operators features.
* Provide a flexible identity/authentication and credential management system for use within BOSH and Cloud Foundry
* Maintain a set of databases, required for the self-contained deployment and operation of BOSH and Cloud Foundry. 

## Scope

* Maintain public roadmaps for BOSH, UAA, and Credhub
* Operate https://bosh.io
* Provide the community with a multi-cloud reference deployment of the BOSH Director
* Package up all infrastructure related components as BOSH releases 

## Non-Goals

* Provide generic operational databases for other use-cases
* Solve non-CF related identity and credential problems.

## Proposed Membership

Technical Lead(s): 
- Ruben Koster (@rkoster)

Execution Lead(s):
- Ruben Koster (@rkoster)

Approvers: 
- Joseph Palermo (@jpalermo)
- Long Nguyen (@lnguyen)
- Peter Chen (@peterhaochen47)
- Andrew Garner (@abg)
- Ramon Makkelie (@ramonskie)
- Markus Strehle (@strehle)
- Beyhan Veli (@beyhan)
- Benjamin Gandon (@bgandon)

## Technical Assets

Components from the BOSH, BOSH Backup and Restore, CredHub, MySQL, Postgres, and UAA projects.

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
- [cloudfoundry-incubator/backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release)
- [cloudfoundry-incubator/bosh-alicloud-light-stemcell-builder](https://github.com/cloudfoundry-incubator/bosh-alicloud-light-stemcell-builder)
- [cloudfoundry-incubator/bosh-backup-and-restore-test-releases](https://github.com/cloudfoundry-incubator/bosh-backup-and-restore-test-releases)
- [cloudfoundry-incubator/bosh-cpi-certification](https://github.com/cloudfoundry-incubator/bosh-cpi-certification)
- [cloudfoundry-incubator/bosh-disaster-recovery-acceptance-tests](https://github.com/cloudfoundry-incubator/bosh-disaster-recovery-acceptance-tests)
- [cloudfoundry-incubator/bosh-windows-acceptance-tests](https://github.com/cloudfoundry-incubator/bosh-windows-acceptance-tests)
- [cloudfoundry-incubator/bosh-windows-stemcell-builder](https://github.com/cloudfoundry-incubator/bosh-windows-stemcell-builder)
- [cloudfoundry-incubator/cf-mysql-ci](https://github.com/cloudfoundry-incubator/cf-mysql-ci)
- [cloudfoundry-incubator/credhub-acceptance-tests](https://github.com/cloudfoundry-incubator/credhub-acceptance-tests)
- [cloudfoundry-incubator/credhub-api-site](https://github.com/cloudfoundry-incubator/credhub-api-site)
- [cloudfoundry-incubator/credhub-ci-locks](https://github.com/cloudfoundry-incubator/credhub-ci-locks)
- [cloudfoundry-incubator/credhub-cli](https://github.com/cloudfoundry-incubator/credhub-cli)
- [cloudfoundry-incubator/credhub-perf-release](https://github.com/cloudfoundry-incubator/credhub-perf-release)
- [cloudfoundry-incubator/credhub](https://github.com/cloudfoundry-incubator/credhub)
- [cloudfoundry-incubator/disaster-recovery-acceptance-tests](https://github.com/cloudfoundry-incubator/disaster-recovery-acceptance-tests)
- [cloudfoundry-incubator/event-log-release](https://github.com/cloudfoundry-incubator/event-log-release)
- [cloudfoundry-incubator/exemplar-backup-and-restore-release](https://github.com/cloudfoundry-incubator/exemplar-backup-and-restore-release)
- [cloudfoundry-incubator/greenhouse-ci](https://github.com/cloudfoundry-incubator/greenhouse-ci)
- [cloudfoundry-incubator/hey](https://github.com/cloudfoundry-incubator/hey)
- [cloudfoundry-incubator/mysql-backup-release](https://github.com/cloudfoundry-incubator/mysql-backup-release)
- [cloudfoundry-incubator/mysql-monitoring-release](https://github.com/cloudfoundry-incubator/mysql-monitoring-release)
- [cloudfoundry-incubator/pxc-release](https://github.com/cloudfoundry-incubator/pxc-release)
- [cloudfoundry-incubator/resolvconf-manager-index](https://github.com/cloudfoundry-incubator/resolvconf-manager-index)
- [cloudfoundry-incubator/resolvconf-manager](https://github.com/cloudfoundry-incubator/resolvconf-manager)
- [cloudfoundry-incubator/sample-windows-bosh-release](https://github.com/cloudfoundry-incubator/sample-windows-bosh-release)
- [cloudfoundry-incubator/stembuild](https://github.com/cloudfoundry-incubator/stembuild)
- [cloudfoundry-incubator/stemcells-alicloud-index](https://github.com/cloudfoundry-incubator/stemcells-alicloud-index)
- [cloudfoundry-incubator/windows-utilities-release](https://github.com/cloudfoundry-incubator/windows-utilities-release)
- [cloudfoundry-incubator/windows-utilities-tests](https://github.com/cloudfoundry-incubator/windows-utilities-tests)
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
- [cloudfoundry/cf-acceptance-tests](https://github.com/cloudfoundry/cf-acceptance-tests)
- [cloudfoundry/cf-deployment](https://github.com/cloudfoundry/cf-deployment)
- [cloudfoundry/cf-identity-acceptance-tests-release](https://github.com/cloudfoundry/cf-identity-acceptance-tests-release)
- [cloudfoundry/cf-mysql-deployment](https://github.com/cloudfoundry/cf-mysql-deployment)
- [cloudfoundry/cf-mysql-release](https://github.com/cloudfoundry/cf-mysql-release)
- [cloudfoundry/cf-uaa-lib](https://github.com/cloudfoundry/cf-uaa-lib)
- [cloudfoundry/cf-uaac](https://github.com/cloudfoundry/cf-uaac)
- [cloudfoundry/config-server-release](https://github.com/cloudfoundry/config-server-release)
- [cloudfoundry/config-server](https://github.com/cloudfoundry/config-server)
- [cloudfoundry/docs-bbr](https://github.com/cloudfoundry/docs-bbr)
- [cloudfoundry/docs-book-cloudfoundry](https://github.com/cloudfoundry/docs-book-cloudfoundry)
- [cloudfoundry/docs-bosh](https://github.com/cloudfoundry/docs-bosh)
- [cloudfoundry/docs-credhub](https://github.com/cloudfoundry/docs-credhub)
- [cloudfoundry/docs-dev-guide](https://github.com/cloudfoundry/docs-dev-guide)
- [cloudfoundry/galera-init](https://github.com/cloudfoundry/galera-init)
- [cloudfoundry/gofileutils](https://github.com/cloudfoundry/gofileutils)
- [cloudfoundry/gosigar](https://github.com/cloudfoundry/gosigar)
- [cloudfoundry/omniauth-uaa-oauth2](https://github.com/cloudfoundry/omniauth-uaa-oauth2)
- [cloudfoundry/os-conf-release](https://github.com/cloudfoundry/os-conf-release)
- [cloudfoundry/postgres-release](https://github.com/cloudfoundry/postgres-release)
- [cloudfoundry/secure-credentials-broker](https://github.com/cloudfoundry/secure-credentials-broker)
- [cloudfoundry/socks5-proxy](https://github.com/cloudfoundry/socks5-proxy)
- [cloudfoundry/syslog-release](https://github.com/cloudfoundry/syslog-release)
- [cloudfoundry/tlsconfig](https://github.com/cloudfoundry/tlsconfig)
- [cloudfoundry/uaa-key-rotator](https://github.com/cloudfoundry/uaa-key-rotator)
- [cloudfoundry/uaa-release](https://github.com/cloudfoundry/uaa-release)
- [cloudfoundry/uaa-singular](https://github.com/cloudfoundry/uaa-singular)
- [cloudfoundry/uaa](https://github.com/cloudfoundry/uaa)
- [cloudfoundry/usn-resource](https://github.com/cloudfoundry/usn-resource)
- [cloudfoundry/windows-tools-release](https://github.com/cloudfoundry/windows-tools-release)
- [cloudfoundry/yagnats](https://github.com/cloudfoundry/yagnats)
