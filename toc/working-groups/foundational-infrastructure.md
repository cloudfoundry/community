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
    github: gerg
  - name: Daniel Linsley
    github: dlinsley
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
  - name: Nader Ziada
    github: nader-ziada
  - name: Nitin Ravindran
    github: xtreme-nitin-ravindran
  approvers:
  - name: Aram Price
    github: aramprice
  - name: Brian Upton
    github: ystros
  - name: Chris Selzo
    github: selzoc
  - name: Clay Kauzlaric
    github: KauzClay
  - name: Diego Lemos
    github: dlresende
  - name: George Blue
    github: blgm
  - name: Long Nguyen
    github: lnguyen
  - name: Maya Rosecrance
    github: mrosecrance
  - name: Nishad Mathur
    github: alphasite
  - name: Rajan Agaskar
    github: ragaskar
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Ming Xiao
    github: mingxiao
  repositories:
  - cloudfoundry/backup-and-restore-sdk-release
  - cloudfoundry/bosh-backup-and-restore
  - cloudfoundry/bosh-backup-and-restore-test-releases
  - cloudfoundry/bosh-disaster-recovery-acceptance-tests
  - cloudfoundry/exemplar-backup-and-restore-release
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
  reviewers:
  - name: Irene Gonzalez Ruiz
    github: ireneGonzalezRuiz
  - name: Praveen K Kumar
    github: praveenkalluri18
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
  - name: Pascal Zimmermann
    github: ZPascal
  reviewers:
  - name: Andreas Kyrian
    github: Jobsby
  repositories:
  - cloudfoundry/mysql-backup-release
  - cloudfoundry/mysql-monitoring-release
  - cloudfoundry/postgres-release
  - cloudfoundry/pxc-release
- name: System Logging and Metrics (rsyslog / event-log)
  approvers:
  - name: Ben Fuller
    github: Benjamintf1
  - name: Jovan Kostovski
    github: chombium
  reviewers:
  - name: Wei Li
    github: weili-broadcom
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
  - name: Ramon Makkelie
    github: ramonskie
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
  - name: Nishad Mathur
    github: alphasite
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Ming Xiao
    github: mingxiao
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Felix Moehler
    github: fmoehler
  - name: Ahmed Hassanin
    github: a-hassanin
  - name: Clay Kauzlaric
    github: KauzClay
  reviewers:
  - name: Sascha Stojanovic
    github: Sascha-Stoj
  - name: Ivaylo Ivanov
    github: ivaylogi98
  - name: Ned Petrov
    github: neddp
  - name: Yuri Adam
    github: yuriadam-sap
  - name: Danitsa Kostova
    github: lunaticomic-vc
  - name: Saumya Dudeja
    github: dudejas
  repositories:
  - cloudfoundry/concourse-infra-for-fiwg
  - cloudfoundry/bosh-stemcells-ci
- name: VM deployment lifecycle (BOSH)
  approvers:
  - name: Long Nguyen
    github: lnguyen
  - name: Ramon Makkelie
    github: ramonskie
  - name: Aram Price
    github: aramprice
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
  - name: Nishad Mathur
    github: alphasite
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Ming Xiao
    github: mingxiao
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Felix Moehler
    github: fmoehler
  - name: Clay Kauzlaric
    github: KauzClay
  - name: Sebastian Heid
    github: s4heid
  reviewers:
  - name: Sascha Stojanovic
    github: Sascha-Stoj
  - name: Alexander Lais
    github: peanball
  - name: Ivaylo Ivanov
    github: ivaylogi98
  - name: Ned Petrov
    github: neddp
  - name: Yuri Adam
    github: yuriadam-sap
  - name: Danitsa Kostova
    github: lunaticomic-vc
  - name: Saumya Dudeja
    github: dudejas
  repositories:
  - cloudfoundry/bbl-state-resource
  - cloudfoundry/bosh
  - cloudfoundry/bosh-acceptance-tests
  - cloudfoundry/bosh-agent
  - cloudfoundry/bosh-agent-index
  - cloudfoundry/bosh-aws-cpi-release
  - cloudfoundry/bosh-aws-light-stemcell-builder
  - cloudfoundry/bosh-azure-cpi-release
  - cloudfoundry/bosh-apt-resources
  - cloudfoundry/bosh-bbl-ci-envs
  - cloudfoundry/bosh-bootloader
  - cloudfoundry/bosh-cli
  - cloudfoundry/bosh-common
  - cloudfoundry/bosh-cpi-certification
  - cloudfoundry/bosh-cpi-go
  - cloudfoundry/bosh-cpi-ruby
  - cloudfoundry/bosh-deployment
  - cloudfoundry/bosh-deployment-resource
  - cloudfoundry/bosh-dns-aliases-release
  - cloudfoundry/bosh-dns-release
  - cloudfoundry/bosh-docker-cpi-release
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
  - cloudfoundry/bosh-shared-ci
  - cloudfoundry/bosh-utils
  - cloudfoundry/bosh-virtualbox-cpi-release
  - cloudfoundry/bosh-vsphere-cpi-release
  - cloudfoundry/bosh-warden-cpi-release
  - cloudfoundry/bosh-windows-stemcell-builder
  - cloudfoundry/bpm-release
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

- name: Storage CLI
  approvers:
  - name: Long Nguyen
    github: lnguyen
  - name: Ramon Makkelie
    github: ramonskie
  - name: Aram Price
    github: aramprice
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
  - name: Julian Hjortshoj
    github: julian-hj
  - name: Ming Xiao
    github: mingxiao
  - name: Benjamin Guttmann
    github: benjaminguttmann-avtq
  - name: Felix Moehler
    github: fmoehler
  - name: He Guimin
    github: xiaozhu36
  - name: Florian Braun
    github: FloThinksPi
  - name: Philipp Thun
    github: philippthun
  - name: Johannes Haass
    github: johha
  - name: Michael Oleske
    github: moleske
  - name: Nishad Mathur
    github: alphasite
  - name: Seth Boyles
    github: sethboyles
  - name: Sven Krieger
    github: svkrieger
  - name: Tim Downey
    github: tcdowney
  - name: Katharina Przybill
    github: kathap
  - name: Ben Fuller
    github: Benjamintf1
  - name: Sam Gunaratne
    github: samze
  - name: Alex Rocha
    github: xandroc
  - name: Jochen Ehret
    github: jochenehret
  - name: Greg Cobb
    github: gerg
  - name: Stephan Merker
    github: stephanme
  - name: Clay Kauzlaric
    github: KauzClay
  reviewers:
  - name: Sascha Stojanovic
    github: Sascha-Stoj
  - name: Alexander Lais
    github: peanball
  - name: Al Berez
    github: a-b
  - name: Evan Farrar
    github: evanfarrar
  - name: Shwetha Gururaj
    github: gururajsh
  - name: Sriram Nookala
    github: nookala
  repositories:
  - cloudfoundry/bosh-ali-storage-cli
  - cloudfoundry/bosh-azure-storage-cli
  - cloudfoundry/bosh-davcli
  - cloudfoundry/bosh-gcscli
  - cloudfoundry/bosh-s3cli
  - cloudfoundry/storage-cli

config:
  github_project_sync:
    mapping:
      cloudfoundry: 21
```
