# Meta
[meta]: #meta
- Name: Java Buildpack Migration to Golang
- Start Date: 2025-12-18
- Author: @beyhan
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Migrate the Cloud Foundry Java Buildpack from its current Ruby-based implementation to a Go-based implementation to align with other buildpacks in the ecosystem. This migration will address the maintenance gap, improve consistency, and make it easier for the community to contribute and maintain the buildpack going forward.


## Problem

The Ruby-based Java Buildpack is currently unmaintained following the departure of its core maintainer from the CF community. Additionally, it has a historically grown unique implementation in Ruby, while all other Cloud Foundry buildpacks have been implemented in Go. This creates maintenance challenges and inconsistency across the buildpack ecosystem.

## Proposal

The Buildpacks and Stacks area of the App Runtime Interfaces working reimplements the Java Buildpack in Go to align with other Cloud Foundry buildpacks and restore active maintainability to this critical component. The new buildpack will be provided as a drop-in replacement for the current Ruby-based Java Buildpack under a new major version. We will reach out to the CF community to help validate the pre-release version and provide feedback to ensure a smooth transition.

### Release Plan

* `v5.0.x` - Experimental release intended to get broad feedback by users, incompatible changes may happen
* `v5.1.0` - First non-experimental GA release

### Breaking Changes

Please note the following breaking changes in the Go-based Java Buildpack:

#### Custom JRE Usage

Custom JRE usage will be supported only as documented in the [Custom JRE Usage Guide](https://github.com/cloudfoundry/java-buildpack/blob/feature/go-migration/docs/custom-jre-usage.md).

#### Changed Default Configuration

* SpringAutoReconfigurationFramework is now disabled by default. Please note that SpringAutoReconfigurationFramework is deprecated, and the recommended alternative is [java-cfenv](https://github.com/pivotal-cf/java-cfenv).
* JRE selection based on `JBP_CONFIG_COMPONENTS` is deprecated in the go-based buildpack and JRE selection based on `JBP_CONFIG_<JRE_TYPE>` is supported as described [here](https://github.com/cloudfoundry/java-buildpack/blob/feature/go-migration/README.md#jre-selection).

#### Frameworks Not Included

The following frameworks will not be migrated to the Go buildpack:

* Takipi Agent (OverOps) – Removed because the agent has moved behind a licensed login wall, making it inaccessible for automated buildpack integration
* Java Security – Rarely used and custom security policies should be implemented at the platform level or within application code
* Multi Buildpack – No longer needed as multi-buildpack support is now built into the libbuildpack architecture by default
* Spring Insight – Legacy monitoring tool that has been replaced by modern APM solutions (such as New Relic, AppDynamics, and Dynatrace)
* Configuration based on resource overlay - This is more of an anti-pattern and requires a fork of the buildpack.


