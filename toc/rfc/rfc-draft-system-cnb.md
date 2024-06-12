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

- Introduce a new `lifecycle` column to the [buildpack object](https://v3-apidocs.cloudfoundry.org/version/3.164.0/index.html#the-buildpack-object) with ENUM values `cnb` or `buildpack`, with `buildpack` being the default.
- Add new parameter `lifecycle` to the [`POST /v3/buildpacks`](https://v3-apidocs.cloudfoundry.org/version/3.164.0/index.html#create-a-buildpack) API endpoint, with the default value being inferred from the `default_app_lifecycle` setting within the Cloud Controller config.
- Cloud Native Buildpacks MUST be stored in format of a gzipped OCI tarball. The layout of the tarball is outlined in the [OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
- Add support for gzipped OCI tarballs when uploading a buildpacks using [`POST /v3/buildpacks/:guid/upload`](https://v3-apidocs.cloudfoundry.org/version/3.164.0/index.html#upload-buildpack-bits) API endpoint
- `cf push` command without specifying an explicit list of buildpacks MUST perform auto-detection using the system buildpacks based on their priority. The type of the buildpacks is based on the `default_app_lifecycle` setting within the Cloud Controller config.
- `cf push --lifecycle cnb` command without an explicit list of buildpacks MUST perform auto-detection using system Cloud Native Buildpacks based on their priority.
- `cf push --lifecycle buildpack` command without specifying an explicit list of buildpacks MUST perform auto-detection using the classic buildpacks based on their priority.
- `cf push --lifecycle buildpack|cnb -b <system-cnb>` command MUST use only the selected system buildpacks with the lifecycle specified by the `--lifecycle` flag and fail the staging process if the buildpack's detection fails.
- `cf push -b <system_buildpack>` command MUST use only the selected system buildpacks, using the lifecycle specified by the `default_app_lifecycle` setting within the Cloud Controller config.
