# Meta
[meta]: #meta
- Name: Proposal for Ruby and Python Removal from the cflinuxfs4 Stack with a Deprecation Period
- Start Date: 2023-04-05
- Author(s): @stephanme @sklevenz @beyhan
- Status: Draft
- RFC Pull Request: [community#573](https://github.com/cloudfoundry/community/pull/573)

## Summary

The Python and Ruby runtimes have been [removed from the cflinuxfs4 stack](https://github.com/cloudfoundry/cflinuxfs4/releases/tag/1.0.0) shortly before its GA release. This is a backwards incompatible change for the buildpacks relying on those runtimes and for some of the CF applications having runtime dependencies to Ruby or Python without using the Ruby or Python buildpack.

This RFC addresses that by proposing a backwards compatible `cflinuxfs4` stack and leaving time for the affected parties to adopt to the removal.

## Problem

The CF stack contains Ruby and Python versions coming from the Ubuntu version the stack is based on. The Ruby and the Python versions included in Ubuntu are quite old and usually have their end of life (EOF) before the corresponding EOF of the Ubuntu version they are included in. The EOF of the CF stack is usually defined by the EOF of the Ubuntu version it’s based on. That means for certain time of period the CF stack is delivered with unmaintained Ruby and Python versions. This is a security issue and needs to be addressed but removing those runtimes from the stack is a backwards incompatible change because of:

* Some of the available buildpacks’ implementations require Ruby or Python. That is why those buildpacks must adopt and bring their own Ruby or Python version, which means that there is a compatibility dependency between the `cflinuxfs4` stack and those buildpacks. This needs to be considered by CF application developers and we know from experience that such changes require a lot of time to be executed. There are even CF users pinning their buildpack versions which could be an issue in this case.

* There are Cloud Foundry providers which already offer the new `cflinuxfs4` stack in `0.x` version to their end users and there are already applications running on that. CF applications could be impacted if there is a runtime dependency to Ruby or Python, which is provided by the stack. Those applications will crash during the app evacuation happening as part of a CF update. This is an unsupported use case, but we shouldn't break those applications without giving them a chance to adapt.

## Proposal

The CFF community will provide two flavours of the `cflinuxfs4` stack one without Ruby and Python and one with those runtimes as backwards compatible option. The two flavours of `cflinuxfs4` will be supported until the EOF of `cflinuxfs4`. In the following sections the flavour without Ruby and Python is called `cflinuxfs4` and the one with `cflinuxfs4-compat`.

### Creation

The two flavours of `cflinuxfs4` will be delivered as separate bosh-releases available on [bosh.io](https://bosh.io/releases/). The bosh-release of `cflinuxfs4-compat` will be called `cflinuxfs4-compat-release` and will have the same version as `cflinuxfs4-release`. The `cflinuxfs4-compat` flavour will include Ruby and Python in the versions, which were available at the time when a new `cflinuxfs4` stack needs to be released. CFF community wouldn't try to build a new `cflinuxfs4` stack when there is a new version of Ruby and/or Python. The benefits of this approach are that it keeps the version lines in sync, which reduces complexity and makes it slightly easier to create and to consume. The drawback is that, if there is a CVE in Ruby and/or Python or any of their transitive dependencies, that won't be resolved until the next time an upstream stack is released. This shouldn't be an issue because the Ruby and Python from the CF stack are deprecated and if an application requires Ruby and/or Python it should use the Ruby and Python buildpacks which provide more up-to-date versions.

Additionally, the `cflinuxfs4-compat` flavour won't be validated with the full set of tests usually executed for a stack release. It will be released after a successful validation of the `cflinuxfs4` flavour to avoid situations where the release of `cflinuxfs4` isn't possible because of failures in the extra validation.

The creation and the release of the two flavours should be part of the App Runtime Interfaces working group responsibilities because they own the process of making new CF stacks.

### Consumption
The `cflinuxfs4` flavour will be configured in `cf-deployment` as default to indicate the deprecation of Ruby and Python in the CF stack. To make the life of CF operators easier `cf-deployment` will offer an ops file for activation of `cflinuxfs4-compat`.

Both flavours will have the same stack name `cflinuxfs4` when they are added to CF. This approach won't allow the parallel use of both flavours in CF but has the advantage that no buildpacks changes are required.

This should be part of the App Runtime Deployments working group responsibilities because the working group provides the refence deployment of CF.

### Removal
With the next stack version, which most probably will be named `cflinuxfs5` the CFF community won't offer a stack flavour with Ruby and Python any more.
