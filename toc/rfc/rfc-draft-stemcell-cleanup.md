# Meta
[meta]: #meta
- Name: Stemcell Cleanup
- Start Date: 2022-06-14
- Author(s): @rkoster
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/308


## Summary

In an effort to reduce ongoing IaaS spend of the Cloud Foundry Foundation this RFC proposes cleanup schedules for light and heavy stemcells.

## Problem

Currently heavy stemcells (full stemcell images stored in s3/gcs) are stored indefinitly. This is also true for the images backing light stemcells.
This becomes a costly endevour, especially on AWS where we need to keep an EBS snapshot per region per light stemcell.

It has been estimated that cleaning up old stemcells could save tens of thousands of dollars.

In addition to published stemcells we also store candiate stemcells which never have been published indefinitly.
These should be safe to cleanup after we are sure we are not going to publish them.

## Proposal

- Clean up stemcells (heavy, light, windows, etc.) older than 3 years.
- Clean up unpublished candidate stemcells after 2 months.

