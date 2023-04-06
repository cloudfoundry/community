# Meta
[meta]: #meta
- Name: Proposal for Ruby and Python Removal from the cflinuxfs4 Stack with a Deprecation Period
- Start Date: 2023-04-05
- Author(s): @stephanme @sklevenz @beyhan
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

The Python and Ruby runtimes have been [removed from the cflinuxfs4 stack](https://github.com/cloudfoundry/cflinuxfs4/releases/tag/1.0.0) shortly before its GA release. This is a backwards incompatible change for the buildpacks relying on those runtimes and for some of the CF applications having runtime dependencies to Ruby or Python without using the Ruby or Python buildpack.

This RFC addresses that by proposing a backwards compatible cflinuxfs4 stack and leaving time for the affected parties to adopt to the removal.

## Problem

The CF stack contains Ruby and Python versions coming from the Ubuntu version the stack is based on. The Ruby and the Python versions included in Ubuntu are quite old and usually have their end of life before the corresponding end of life of the Ubuntu version they are included in. The end of life of the CF stack is usually defined by the end of life of the Ubuntu version it’s based on. That means for certain time of period the CF stack is delivered with unmaintained Ruby and Python versions. This is a security issue and needs to be addressed but removing those runtimes from the stack is a backwards incompatible change because of:

* Some of the available buildpacks’ implementations require Ruby or Python. That is why those buildpacks must adopt and bring their own Ruby or Python version, which means that there is a compatibility dependency between the `cflinuxfs4` stack and those buildpacks. This needs to be considered by CF application developers and we know from experience that such changes require a lot of time to be executed. There are even CF users pinning their buildpack versions which could be an issue in this case.

* There are Cloud Foundry providers which already offer the new `cflinuxfs4` stack in `0.x` version to their end users and there are already applications running on that. CF applications could be impacted if there is a runtime dependency to Ruby or Python which is provided by the stack. Those applications will crash during the app evacuation happening as part of a CF update. This is an unsupported use case, but we shouldn't break those application without giving them a chance to adapt.

## Proposal

The CFF community should provide two versions of the `cflinuxfs4` stack one without Ruby and Python and one with those runtimes as backwards compatible version. The CFF community will deprecate the Python and Ruby provided by the `cflinuxfs4` stack and remove those runtimes from the stack latest with the `cflinuxfs5` stack. This should be part of the App Runtime Interfaces Working Group responsibilities because they own the process of making new CF stacks. Additionally, CF operators requires the option to choose between the two `cflinxufs4` stack flavours. This should be part of the App Runtime Deployments responsibilities because the working provides the refence deployment of CF.

