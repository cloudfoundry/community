# Meta
[meta]: #meta
- Name: CF components support FIPS certified stemcells
- Start Date: 2023-10-17
- Author(s): @beyhan
- Status: Draft
- RFC Pull Request: TBD


## Summary
The CFF community should make sure that CF components aswell as the BOSH Director are compatible with FIPS stemcells.

## Problem
Some of the foundation members want to run CF on FIPS certified Ubuntu stemcells. At the moment the CF community is not performing FIPS validation. Instead individual members are performing these validations downstream which is inefficient, because of the slow feedback cycle:
- Run FIPS validation downstream
- Raise component level issue
- Component release
- Component bump in cf-deployment
- Cf-deployment bump in member release

To further complicate things there is no way to validate submitted fixes addressing the issue, because there is no way of replicating FIPS issues using CF Foundation resources.


## Proposal
Work with Canonical to get approval for using Ubuntu FIPS packages for testing / validation purposes within the CF Foundation. This work has been completed, and approval has been granted to the CFF.
Using the Ubuntu FIPS packages provided by Canonical, create a CFF internal FIPS jammy stemcell (may not be published on bosh.io) and use it to validate CF components during integration testing in cf-deployment.

To shorten the feedback cycle even further, working group areas may decide to add unit or integration testing in their component level pipelines using the FIPS packages provided by Canonical, by requesting access to these packages via the CFF TOC or use the community internal FIPS stemcell.

This RFC only captures the work required to get cf-deployment in a state where it can run on a stemcell build with FIPS packages. All components actually using those FIPS packages are out of scope for this RFC.

## Workstreams
The major milestones have been documented below in more details per working group.

### Foundational Infrastructure WG


#### CFF internal FIPSstemcell
As a first step the `bosh-linux-stemcell-buider` will need to be extended with support for building a Jammy FIPS stemcell variant. As an initial target, support for AWS, GCP and Azure should be added. Once the foundation internal FIPS stemcell can be built the next step should be an automation which can produce stemcells for CFF internal validation by using the FIPS packages provided by Canonical. The stemcells can be made available to other WGs via a private bucket. It is important to notice that this stemcell must not be distributed for public consumption.

#### BOSH supports FIPS stemcell
As the next step the Foundational Infrastructure WG should validate that the BOSH director can run on a FIPS based stemcell. This can be done by using the BOSH director acceptance test. The validation should be automated and used for every candidate release of the Director.


#### Reproducible build for stemcells (Optional)
While compatibility testing is underway, a second track of work can be picked up, which has to do with the fact that the `bosh-linux-stemcell-buider` currently does not produce reproducible artifacts. The various Ubuntu packages that are installed during the build process are not pinned down, which is great from a security perspective, but not great if downstream vendors want to build a FIPS stemcell version internally using their own Ubuntu Pro license.


Without being too prescriptive, the desired outcome would be some sort of snapshot file containing the package versions being committed to the stemcell-builder repository, before actually building a stemcell. Effectively decoupling building from the act of bumping package versions. Package bumps should be automated and triggered using the same USN feed used to trigger builds now. This functionality should also be contributed to the non-FIPS Jammy pipeline.

### App Runtime Deployments WG

Once initial confidence has been gained by validating the FIPS stemcell against the BOSH director it is time to validate against cf-deployment. Just like with the BOSH director, an automation should be set up to run the CATS test suite against a Cloud Foundry environment which uses the FIPS stemcell from the private foundation bucket. Currently, cf-deployment is validated on AWS and GCP. The WG can decide whether they execute the FIPS validation on AWS or/and GCP. Validation on Azure is out of scope for now to reduce efforts and costs. If there is reasons to have validation on Azure this should be discussed with the App Runtime Deployments WG. Issues discovered by the validation should be distributed to the related CF components. It is their responsibility to address them. If CF components want to have faster feedback on FIPS issues they can add their own validation.





