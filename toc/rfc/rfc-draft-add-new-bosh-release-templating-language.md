# Meta
[meta]: #meta
- Name: Bosh Templating Language
- Start Date: 2024-10-21
- Author(s): jpalermo
- Status: Draft
- RFC Pull Request: [community#1004](https://github.com/cloudfoundry/community/pull/1004)


## Summary

Introduce new custom templating language that can be used by bosh releases. Ideally gather feedback from release
authors as part of the RFC process to define the MVP of the language.

## Problem

Currently all bosh release templates are rendered using ERB using the Bosh Director's Ruby process, or whatever
Ruby process is available when a `bosh create-env` is being run.

We've had multiple release breakages over the years as we upgrade the Bosh Director Ruby version and the Ruby
language changes in a way that release templates were not expecting.

A secondary problem is that template rendering can be slow when rendering templates for large CF deployments.

## Proposal

Write a library/cli that defines a strict grammar suitable for basic template rendering within Bosh releases.

A proof of concept can be found [here](https://github.com/jpalermo/bosh-template-renderer).

We would NOT be removing ERB rendering as an option anytime in the near future. We would update many of the Bosh
Releases in the Foundational Infrastructure Working Group to use the new templates and then target releases
that are on Diego Cells as large CF deployments render those same templates a large number of times.

Having a grammar under our control means we can ensure it does not change or break through golang and dependency
upgrades.

The Bosh Director is written in Ruby, so it will be able to shell out to the CLI to render templates. While
the Bosh CLI is written in golang so it will be able to import the library and use it directly.

The grammar would be kept relatively small. We will not be providing a direct replacement for ERB. Many validations
and data transformations are happening within ERB templates right now that should be happening at different layers
of the deployment process.

Data transformation should be happening within the release runtimes or pre-start scripts. Validation can also happen
there, although it's possible we want to expand the Bosh Release `spec` files to provide some level of validation so
errors can be caught early in the deploy process (that work is NOT part of this RFC).
