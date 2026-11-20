# Meta
[meta]: #meta
- Name: Deprecate the Warden & VirtualBox CPIs
- Start Date: 2026-11-12
- Author(s): @mkocher
- Status: Draft
- RFC Pull Request: [community#1702](https://github.com/cloudfoundry/community/pull/1702)
- Affected Component(s): bosh-warden-cpi-release, bosh-virtualbox-cpi-release, bosh-deployment, bosh-io-web

## Summary

The BOSH ecosystem maintains two container-based CPIs: the Warden CPI and the Docker CPI. Both are used to run a local BOSH director and BOSH deployments inside containers for local development and CI pipelines. The BOSH ecosystem also maintains the VirtualBox CPI, which has been superseded by containers for local workflows. This RFC proposes deprecating the Warden and VirtualBox CPIs in favor of the Docker CPI.

## Problem

We have redundant solutions to local BOSH development - the VirtualBox CPI, the Warden CPI and the Docker CPI. They require ongoing maintenance, such as the recent effort to make Warden and Docker work correctly under cgroups v2.

The practical concerns:

- The Warden CPI uses many privileged operations in its source code to work around Garden API limitations, eg creating loopback devices to use as volumes. As BOSH moves to running CPIs inside of BPM these operations are no longer possible. The right fix would be a large investment in both the CPI and Garden to expand the surface area of the API to encompass all of our needs.

- AI agents inherently know more about how to work with Docker. Agents are more adept when validating or troubleshooting with docker, making them faster and consuming fewer tokens. (eg: using the docker cli vs nsenter or [gaol](https://github.com/contraband/gaol))

- Local development on a Mac is easier with Docker than with Garden. There are any number of pre-made solutions which provide a Docker API locally on a Mac.

- The VirtualBox CPI is featured heavily on bosh.io, however containers have long since replaced it for local development.

- The BOSH team has successfully moved all BOSH pipelines that used to use Warden to the Docker CPI. The BOSH team no longer relies on the Warden CPI.

## Proposal

### Deprecate the Warden and VirtualBox CPIs

#### At RFC Approval
- Mark `bosh-warden-cpi-release` and `bosh-virtualbox-cpi-release` as deprecated. Add a deprecation notice to the repositories' READMEs with a date 3 months in the future.

#### Within 3 months
- Pipelines in the App Runtime Deployments WG that use the Warden CPI are migrated to the Docker CPI.
- Update bosh.io to remove bosh-lite, warden-cpi and virtualbox-cpi references. (leaving an updated BOSH Lite description under Terminology)

#### End of deprecation period

- Stop cutting new releases of `bosh-warden-cpi-release` and `bosh-virtualbox-cpi-release`.
- Remove CI pipelines and archive the repositories.

### Support the use of the docker-cpi container image

The BOSH team produces the [bosh/docker-cpi](https://ghcr.io/cloudfoundry/bosh/docker-cpi) container image which contains Docker, the releases necessary for launching a BOSH director, and a script which launches Docker and runs create-env.

This has proven very useful in many pipelines. An example of a task which uses it can be found in the [bosh-package-nginx-release test task](https://github.com/cloudfoundry/bosh-package-nginx-release/blob/main/ci/tasks/test.sh). We believe this will prove useful to many teams producing and testing BOSH releases.

Support will entail publishing timely updates, avoiding breaking changes if possible, and announcing any deprecation with plenty of advance notice.

## Workstreams

### Foundational Infrastructure WG

- Mark `bosh-warden-cpi-release` as deprecated on GitHub
- Mark `bosh-virtualbox-cpi-release` as deprecated on GitHub
- Open draft pull request to archive associated repos against the community repo
- Update bosh.io to no longer cover the deprecated CPIs
- Merge the pull request to archive the repos at the end of the deprecation period
- Remove the warden-cpi and virtualbox-cpi related ops files from bosh-deployment

### App Runtime Deployments WG

- Migrate any pipelines that use the Warden CPI to the Docker CPI
