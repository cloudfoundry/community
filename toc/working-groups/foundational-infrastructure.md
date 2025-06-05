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
- name: runtime-bot
  github: tas-runtime-bot
- name: cf-bosh-ci-bot
  github: cf-bosh-ci-bot
- name: cf-uaa-ci-bot
  github: cf-identity
- name: Cryogenics-CI
  github: Cryogenics-CI
- name: mysql-ci
  github: pcf-core-services-writer
areas:
- name: Credential Management (Credhub)
  approvers:
  - name: Peter Chen
    github: peterhaochen47
  - name: Hongchol Sinn
    github: hsinn0
  - name: Prateek Gangwal
    github: coolgang123
  - name: Joe Eltgroth
    github: joeeltgroth
  - name: Markus Strehle
    github: strehle
  reviewers:
  - name: Duane May
    github: duanemay
  - name: Behrouz Soroushian
    github: bsoroushian
  - name: Ajita Jain
    github: jajita
  - name: Andrew Costa
    github: acosta11
  - name: Greg Cobb
    github: Gerg
  repositories:
  - cloudfoundry-incubator/credhub-api-docs
  - cloudfoundry/credhub
  - cloudfoundry/credhub-acceptance-tests
  - cloudfoundry/credhub-api-site
  - cloudfoundry/credhub-cli
  - cloudfoundry/credhub-ci-locks
  - cloudfoundry/credhub-oss-ci
  - cloudfoundry/credhub-perf-release
  - cloudfoundry/secure-credentials-broker
- name: Disaster Recovery (BBR)
  reviewers:
  - name: claire t.
    github: Spimtav
  - name: Greg Meyer
    github: gm2552
  - name: Harish Yayi
    github: yharish991
  - name: Indira Chandrabhatta
    github: ichandrabhatta
  - name: Janice Bailey
    github: bjanice75
  - name: Nader Ziada
    github: nader-ziada
  - name: Nitin Ravindran
    github: xtreme-nitin-ravindran
  - name: Rui Yang
    github: xtremerui
  - name: Rizwan Reza
    github: rizwanreza
  - name: Wayne Adams
    github: wayneadams
  approvers:
  - name: Aram Price
    github: aramprice
  - name: Brian Upton
    github: ystros
  - name: Chris Selzo
    github: selzoc
  - name: Diego Lemos
    github: dlresende
  - name: George Blue
    github: blgm
  - name: Iain Findlay
    github: ifindlay-cci
  - name: Konstantin Kiess
    github: nouseforaname
  - name: Long Nguyen
    github: lnguyen
  - name: Maya Rosecrance
    github: mrosecrance
  - name: Rajan Agaskar
    github: ragaskar
  - name: Rajath Agasthya
    github: rajathagasthya
  - name: Ming Xiao
    github: mingxiao
  repositories:
  - cloudfoundry/backup-and-restore-sdk-release
  - cloudfoundry/bosh-backup-and-restore
  - cloudfoundry/bosh-backup-and-restore-test-releases
  - cloudfoundry/bosh-disaster-recovery-acceptance-tests
  - cloudfoundry/exemplar-backup-and-restore-release
  bots:
  - name: tas-operability-bot
    github: tas-operability-bot
- name: Identity and Auth (UAA)
  approvers:
  - name: Peter Chen
    github: peterhaochen47
  - name: Markus Strehle
    github: strehle
  - name: Hongchol Sinn
    github: hsinn0
  - name: Florian Tack
    github: tack-sap
  - name: Torsten Luh
    github: torsten-sap
  - name: Adrian Hoelzl
    github: adrianhoelzl-sap
  - name: Duane May
    github: duanemay
  - name: Prateek Gangwal
    github: coolgang123
  - name: Daniel Garnier-Moiroux
    github: kehrlann
  - name: Filip Hanik
    github: fhanik
  - name: Joe Mahady
    github: joemahady-comm
  repositories:
  - cloudfoundry/cf-identity-acceptance-tests-release
  - cloudfoundry/cf-uaa-lib
  - cloudfoundry/cf-uaac
  - cloudfoundry/identity-tools
  - cloudfoundry/omniauth-uaa-oauth2
  - cloudfoundry/uaa
  - cloudfoundry/uaa-cli
  - cloudfoundry/uaa-key-rotator
  - cloudfoundry/uaa-release
  - cloudfoundry/uaa-singular
  - cloudfoundry/uaa-ci
- name: Identity and Auth (UAA) Go Client
  approvers:
  - name: Joe Fitzgerald
    github: joefitzgerald
  - name: Peter Chen
    github: peterhaochen47
  - name: Markus Strehle
    github: strehle
  - name: Hongchol Sinn
    github: hsinn0
  - name: Florian Tack
    github: tack-sap
  - name: Torsten Luh
    github: torsten-sap
  - name: Adrian Hoelzl
    github: adrianhoelzl-sap
  - name: Filip Hanik
    github: fhanik
  - name: Duane May
    github: duanemay
  reviewers:
  - name: Prateek Gangwal
    github: coolgang123
  repositories:
  - cloudfoundry/go-uaa
- name: Integrated Databases (Mysql / Postgres)
  approvers:
  - name: Andrew Garner
    github: abg
  - name: Colin Shield
    github: colins
  - name: Kim Basset
    github: kimago
  - name: Ryan Wittrup
    github: ryanwittrup
  reviewers:
  - name: Pascal Zimmermann
    github: ZPascal
  repositories:
  - cloudfoundry/mysql-backup-release
  - cloudfoundry/mysql-monitoring-release
  - cloudfoundry/postgres-release
  - cloudfoundry/pxc-release
- name: System Logging and Metrics (rsyslog / event-log)
  approvers:
  - name: Ben Fuller
    github: Benjamintf1
  - name: Carson Long
    github: ctlong
  - name: Ivan Protsiuk
    github: iprotsiuk
  - name: Jovan Kostovski
    github: chombium
  reviewers:
  - name: Ausaf Ahmed
    github: aqstack
  - name: Glenn Oppegard
    github: oppegard
  repositories:
  - cloudfoundry/blackbox
  - cloudfoundry/bosh-system-metrics-server-release
  - cloudfoundry/system-metrics-release
  - cloudfoundry/syslog-release
  - cloudfoundry/windows-syslog-release
- name: Stemcell Release Engineering (BOSH)
  approvers:
  - name: Rajan Agaskar
    github: ragaskar
  - name: Maya Rosecrance
    github: mrosecrance
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
  - name: Chris Selzo
    github: selzoc
  - name: Nitin Ravindran
    github: xtreme-nitin-ravindran
  - name: Nader Ziada
    github: nader-ziada
  - name: Rajath Agasthya
    github: rajathagasthya
  - name: Ming Xiao
    github: mingxiao
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Felix Moehler
    github: fmoehler
  - name: Ahmed Hassanin
    github: a-hassanin
  reviewers:
  - name: Greg Meyer
    github: gm2552
  - name: Jamie van Dyke
    github: fearoffish
  - name: Sascha Stojanovic
    github: Sascha-Stoj
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Nishad Mathur
    github: alphasite
  repositories:
  - cloudfoundry/concourse-infra-for-fiwg
  - cloudfoundry/bosh-stemcells-ci
- name: VM deployment lifecycle (BOSH)
  approvers:
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
  - name: Konstantin Kiess
    github: nouseforaname
  - name: Rajan Agaskar
    github: ragaskar
  - name: Maya Rosecrance
    github: mrosecrance
  - name: Brian Upton
    github: ystros
  - name: Chris Selzo
    github: selzoc
  - name: Matthias Vach
    github: mvach
  - name: Ahmed Hassanin
    github: a-hassanin
  - name: Ansh Rupani
    github: anshrupani
  - name: Nitin Ravindran
    github: xtreme-nitin-ravindran
  - name: Nader Ziada
    github: nader-ziada
  - name: Rajath Agasthya
    github: rajathagasthya
  - name: Ming Xiao
    github: mingxiao
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Felix Moehler
    github: fmoehler
  reviewers:
  - name: Greg Meyer
    github: gm2552
  - name: Jamie van Dyke
    github: fearoffish
  - name: Benjamin Gandon
    github: bgandon
  - name: Sascha Stojanovic
    github: Sascha-Stoj
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Nishad Mathur
    github: alphasite
  - name: Alexander Lais
    github: peanball
  repositories:
  - cloudfoundry/bbl-state-resource
  - cloudfoundry/bosh
  - cloudfoundry/bosh-acceptance-tests
  - cloudfoundry/bosh-agent
  - cloudfoundry/bosh-agent-index
  - cloudfoundry/bosh-aws-cpi-release
  - cloudfoundry/bosh-aws-light-stemcell-builder
  - cloudfoundry/bosh-azure-cpi-release
  - cloudfoundry/bosh-azure-storage-cli
  - cloudfoundry/bosh-apt-resources
  - cloudfoundry/bosh-bbl-ci-envs
  - cloudfoundry/bosh-bootloader
  - cloudfoundry/bosh-cli
  - cloudfoundry/bosh-common
  - cloudfoundry/bosh-cpi-certification
  - cloudfoundry/bosh-cpi-go
  - cloudfoundry/bosh-cpi-ruby
  - cloudfoundry/bosh-davcli
  - cloudfoundry/bosh-deployment
  - cloudfoundry/bosh-deployment-resource
  - cloudfoundry/bosh-dns-aliases-release
  - cloudfoundry/bosh-dns-release
  - cloudfoundry/bosh-docker-cpi-release
  - cloudfoundry/bosh-gcscli
  - cloudfoundry/bosh-google-cpi-release
  - cloudfoundry/bosh-io-releases
  - cloudfoundry/bosh-io-releases-index
  - cloudfoundry/bosh-io-stemcells-core-index
  - cloudfoundry/bosh-io-stemcells-cpi-index
  - cloudfoundry/bosh-io-stemcells-legacy-index
  - cloudfoundry/bosh-io-stemcells-windows-index
  - cloudfoundry/bosh-io-web
  - cloudfoundry/bosh-io-worker
  - cloudfoundry/bosh-linux-stemcell-builder
  - cloudfoundry/bosh-openstack-cpi-release
  - cloudfoundry/bosh-package-golang-release
  - cloudfoundry/bosh-package-nginx-release
  - cloudfoundry/bosh-package-python-release
  - cloudfoundry/bosh-package-ruby-release
  - cloudfoundry/bosh-psmodules
  - cloudfoundry/bosh-s3cli
  - cloudfoundry/bosh-shared-ci
  - cloudfoundry/bosh-utils
  - cloudfoundry/bosh-virtualbox-cpi-release
  - cloudfoundry/bosh-vsphere-cpi-release
  - cloudfoundry/bosh-warden-cpi-release
  - cloudfoundry/bosh-windows-acceptance-tests
  - cloudfoundry/bosh-windows-stemcell-builder
  - cloudfoundry/bpm-release
  - cloudfoundry/bsdtar
  - cloudfoundry/config-server
  - cloudfoundry/config-server-release
  - cloudfoundry/docs-bosh
  - cloudfoundry/exemplar-release
  - cloudfoundry/go-socks5
  - cloudfoundry/gofileutils
  - cloudfoundry/gosigar
  - cloudfoundry/greenhouse-ci
  - cloudfoundry/jumpbox-deployment
  - cloudfoundry/os-conf-release
  - cloudfoundry/sample-windows-bosh-release
  - cloudfoundry/socks5-proxy
  - cloudfoundry/stembuild
  - cloudfoundry/usn-resource
  - cloudfoundry/windows-utilities-release
- name: Ali Cloud VM deployment lifecycle (BOSH)
  approvers:
  - name: He Guimin
    github: xiaozhu36
  repositories:
  - cloudfoundry/bosh-alicloud-cpi-release
  - cloudfoundry/bosh-alicloud-light-stemcell-builder
  - cloudfoundry/bosh-ali-storage-cli
  - cloudfoundry/stemcells-alicloud-index

- name: Prometheus (Bosh)
  approvers:
    - name: Benjamin Guttmann
      github: benjaminguttmann-avtq
    - name: Gilles Miraillet
      github: gmllt
    - name: Mario Di Miceli
      github: mdimiceli
    - name: Nicolas Herbst
      github: nmaurer23
  repositories:
    - cloudfoundry/bosh_exporter
    - cloudfoundry/cf_exporter
    - cloudfoundry/firehose_exporter
    - cloudfoundry/node-exporter-boshrelease
    - cloudfoundry/prometheus-boshrelease
  bots:
    - name: cf-prometheus-ci-bot
      github: cf-prometheus-ci-bot

config:
  github_project_sync:
    mapping:
      cloudfoundry: 21
```
