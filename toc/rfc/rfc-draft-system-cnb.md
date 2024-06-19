# Meta
[meta]: #meta
- Name: System Cloud Native Buildpacks
- Start Date: 30.04.2024
- Author(s): @c0d1ngm0nk3y, @pbusko, @nicolasbender, @modulo11
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)
- Predecessor: https://github.com/cloudfoundry/community/pull/796

## Summary

This RFC proposes extending the Cloud Foundry functionality to introduce and support system Cloud Native Buildpacks (CNBs). It will allow users to initiate the `cf push --lifecycle cnb` command without providing an explicit list of buildpacks, relying instead on the list of system buildpacks and the built-in auto-detection mechanism.

## Problem

Despite the recent integration of CNBs in the Cloud Foundry platform, the feature still has limitations that could hinder user experience and efficiency. Currently, only custom buildpacks are supported. Users have to manually provide a list of buildpacks (at least one) for their application to run with the `cnb` lifecycle type.

## Proposal

- Make it possible to configure the default application lifecycle with the following options: `buildpack` or `cnb`. The value of this setting will be further reffered to as the *default lifecycle*.
- Introduce a new `lifecycle` column to the [buildpack object](https://v3-apidocs.cloudfoundry.org/index.html#the-buildpack-object) with ENUM values `cnb` or `buildpack`. If the value is not provided, the default lifecycle MUST be used.
- Add new parameter `lifecycle` to the [`POST /v3/buildpacks`](https://v3-apidocs.cloudfoundry.org/index.html#create-a-buildpack) API endpoint. If the value is not provided, the default lifecycle MUST be used.
- Cloud Native Buildpacks MUST be stored in format of a gzipped OCI tarball. The layout of the tarball is outlined in the [OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
- Add support for gzipped OCI tarballs when uploading a buildpacks using [`POST /v3/buildpacks/:guid/upload`](https://v3-apidocs.cloudfoundry.org/index.html#upload-buildpack-bits) API endpoint
- `cf push` command without specifying an explicit list of buildpacks MUST perform auto-detection using the system buildpacks based on their priority. The type of the buildpacks and the lifecycle are based on the default lifecycle.
- `cf push --lifecycle buildpack|cnb` command without an explicit list of buildpacks MUST perform auto-detection using the selected lifecycle, based on their priority.
- `cf push --lifecycle buildpack|cnb -b <system-cnb>` command MUST use only the selected system buildpacks with the lifecycle specified by the `--lifecycle` flag and fail the staging process if the buildpack's detection fails.
- `cf push -b <system_buildpack>` command MUST use only the selected system buildpacks, using the lifecycle specified by the default lifecycle.
