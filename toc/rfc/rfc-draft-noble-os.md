# Meta
[meta]: #meta
- Name: Support Noble Numbat (24.04) as the CF Linux
- Start Date: 2024-03-01
- Author: @beyhan
- Contributing Authors: @rkoster, @jochenehret
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

The CFF community should add support for Noble Numbat (24.04) as CF Operating System.

## Problem

The current Operating System for CF is Jammy Jellyfish (22.04), which has the end of standard support planned for 2027.06. The next planned long term support (LTS) releases for Ubuntu are Noble Numbat (24.04) and most probably one in 26.04 because Ubuntu has a two year lifecycle for LTS releases. If we skip the Noble Numbat support we will have approximately one year to implement the support and adoption for the next LTS release. In the past the CFF community decided to [skip Ubuntu Focal](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0001-jammy-os.md) and move directly to Jammy Jellyfish (22.04) LTS, which turned out to be quite challenging due to:
- The short time available for the overall execution
- The implementation effort is unknown upfront because it depends on the changes introduced with the new OS version
- Almost impossible to introduce backwards incompatible changes like removal of unneeded libraries because of the short time available for validation and adoption


## Proposal

The CFF community should not skip the Noble Numbat (24.04) release. The CFF community should start work on publishing a stemcell line based on Noble Numbat starting in March or April of 2024. This means that until the end of planned support for Jammy two stemcell lines (Jammy and Noble) will be supported, which can affect the tests and validations of the CF components. The CF components should take the responsibility to decide what kind of tests and validation makes sense for the two stemcell lines. The Slack channel [bosh-noble](https://cloudfoundry.slack.com/archives/C06HTDT78N9) should be used for communication around this effort.

## Workstreams

The major milestones have been documented below in more details per working group.

### Foundational Infrastructure WG

The Foundational Infrastructure Working Group is responsible for making new stemcells. As soon as Noble Numbat (24.04) packages from Ubuntu are available the WG can start working on the new stemcell. The effort in the FI WG includes following rough list of steps:
- Extend [bosh-linux-stemcell-builder](https://github.com/cloudfoundry/bosh-linux-stemcell-builder) for Noble Numbat
- Noble Numbat stemcell is produce by CI
- BOSH agent works
- BOSH Director works
- BOSH acceptance tests run successfully
- Make a 0.x beta version of the stemcell available for CFF community validation
- After successful validation in the community publish 1.x GA stemcell version on [bosh.io](http://bosh.io)


The end of planned support for Jammy Jellyfish (22.04) is 06.2027. That is why for Noble Numbat we can take some time to look into topics from the [wish list](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/milestone/1). The RFC suggests targeting a beta stemcell available for the end of Q3 2024, which could be used by the App Runtime Deployment for validation. The FI WG will implement the same release validation for Noble like the one existing currently for Jammy.

### App Runtime Deployments WG

Once initial confidence has been gained by validating the Noble Numbat stemcell against the BOSH director it is time to validate against cf-deployment. A simular validation like the one existing for Jammy stemcell should be set up for Noble which will use the beta 0.x version of the stemcell provided by the FI WG. GCP will be used as the initial validation environment but if required validation on AWS could be added. Issues discovered by this validation should be distributed to the related CF components. It is their responsibility to address them. If CF components want to have faster feedback on Noble Numbat issues they can add their own validation. When the cf-deployment validation of Noble is successful the FI WG will release the 1.x GA version of the Noble Numbat stemcell. The Noble Numbat validation in cf-deployment will be kept also after the 1.x GA release. At this point cf-deployment will also provide an `ops-file`, which can be used by CF operators to switch to Noble Numbat. Additionally, cf-deployment should decide to make the Noble stemcell the default one well before the EOF for Jammy so that CF operators have enough time to migration from Jammy to Noble.