# Meta
[meta]: #meta
- Name: Add Paketo Stacks to CF Deployment
- Start Date: 2023-06-30
- Author: @gerg
- Contributing Authors: @robdimsdale, @dsabeti, @dsboulder, @sophiewigmore, @geofffranks
- Status: Draft
- RFC Pull Request: TBD

## Summary

This RFC is a continuation of
[RFC 0017: Add Cloud Native Buildpacks](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0017-add-cnbs.md)
introduced by
[community#591](https://github.com/cloudfoundry/community/pull/591).

The [Paketo](https://paketo.io/) project releases a series of stacks. These
stacks are rootFS for the build and run containers for apps using the Paketo
buildpacks. Now that CF Deployment is adopting the Paketo Cloud Native
Buildpacks (CNBs), there is an opportunity to also adopt the Paketo stacks.
Adopting Paketo stacks would further unify the Cloud Foundry ecosystem and
provide some benefits to Cloud Foundry users, as discussed in this RFC.

## Problem

Security scanning technology has advanced significantly in recent years,
allowing Cloud Foundry operators to more easily scan app containers for CVEs.
This, combined with a renewed industry focus on CVE management, has increased
Cloud Foundry operator sensitivity to the CVEs present in app containers.

Currently, a major source of these CVEs is the collection of Ubuntu packages
that are included in cflinuxfs4. Cloud Foundry has made some improvements in
this area, for example by excluding Ruby and Python from cflinuxfs4, but there
is still room for improvement. Adopting the Paketo stacks in CF Deployment will
provide Cloud Foundry operators and app developers with tools to reduce CVE
exposure in running app containers.

## Proposal

### Background

A primary benefit of Paketo is that built app images have a reduced number of
operating system packages. Paketo accomplishes this through two mechanisms:
lightweight stacks and separate build and run images.

#### Lightweight Stacks

Ignoring Windows stacks, CF Deployment currently only offers a single stack:
cflinuxfs4. In contrast,
[Paketo offers four "weights" of stacks](https://paketo.io/docs/concepts/stacks/#what-paketo-stacks-are-available)
with varying sets of included Operating System packages:
[Full](https://github.com/paketo-buildpacks/jammy-full-stack),
[Base](https://github.com/paketo-buildpacks/jammy-base-stack),
[Tiny](https://github.com/paketo-buildpacks/jammy-tiny-stack),
and [Static (experimental)](https://github.com/paketo-buildpacks/jammy-static-stack)
. The Paketo Full stack is roughly equivalent to cflinuxfs4, whereas the Base,
Tiny, and Static stacks include progressively fewer Ubuntu packages.

#### Separate Build and Run Images

CF Deployment uses the same rootFS for building and running applications. This
means that packages that are only needed for building applications (e.g.
compilers like `gcc`) are also present in running app containers. The Paketo
stacks instead [come with both Build and Run images](https://paketo.io/docs/concepts/stacks/#what-is-a-stack)
, where build-time Ubuntu packages are only included in the Build image.

#### Conclusion

Accounting for both of these factors, there are two "dimensions" to Paketo
stacks that affect the number of Ubuntu packages included in app containers:
weight and build/run. CF Deployment could one day offer all of these options,
so Cloud Foundry users can select the stack that matches their app's Ubuntu
package needs and security posture.

### Goals

1. Align CF Deployment with the main focus of the Buildpacks & Stacks team
1. Bring new capabilities to CF Deployment users, including:
    1. Lightweight Stacks
    1. Separate Build and Run Images
1. Increase cohesion and app portability between CF Deployment and Korifi, via
   shared Paketo stacks
1. Increase user base for the Paketo stacks
1. Open the door for eventual deprecation of the cflinuxfs* stacks, reducing
   maintenance costs (cflinuxfs* deprecation is NOT included in this RFC)

### High-Level Implementation

Instead of using cflinuxfs4, apps using the new CNBs will use the
[Paketo Jammy Full stack](https://github.com/paketo-buildpacks/jammy-full-stack)
. The Jammy Full stack will include two rootFSs: build and run. The Paketo
Jammy Full stack is very similar to cflinuxfs4, which will reduce the
difficulty of migrating existing Cloud Foundry apps to the Paketo stacks and
buildpacks. This will also lay the groundwork for eventually supporting the
remaining Paketo Jammy stacks, which will offer better security posture for
interested Cloud Foundry users.

#### App Developer Experience

The Paketo Full stack will be modeled as a single Cloud Foundry stack with two
associated rootFSs. The details of selecting the rootFS for build and run
containers will be handled by CAPI, depending on whether it is staging an app
or running a process/task. This means that app developers will not need to be
aware that separate build and run rootFSs are being used, they only need to
push their app with the new stack:

```sh
cf push my-app --stack=paketo_jammy_full
```

#### Initial Scope

1. Produce a tarball of the Paketo Full stack (instead of an OCI image)
1. Create a BOSH release for the Paketo Full stack
1. Update CNB shims to use the Paketo Full stack instead of cflinuxfs4
1. Add CF support for separate build and run rootFSs
1. Update CATs to test the Paketo Full stack integration
1. CI for Cloud Foundry + Paketo Full stack integration
1. Add ops file for the Paketo Full stack to CF Deployment

### Governance and Release

A `paketo_jammy_full_release` repository will be added to the Application
Runtime Interfaces working group. This will contain the BOSH release for the
Paketo Jammy full stack.

The Paketo stacks will initially be opt-in for CF Deployment operators via an
experimental ops file. When installed, the Paketo stacks will be named
`paketo_<ubuntu version>_<weight>`, e.g. "paketo_jammy_full". Once the CF
Deployment integration of the Paketo stacks and buildpacks has reached a
suitable level of maturity and stability, the Paketo stacks will be added to
the default set stacks installed as part of CF Deployment.

