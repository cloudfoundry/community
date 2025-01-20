# Meta
[meta]: #meta
- Name: Bosh Release Property Validation
- Start Date: 2024-01-20
- Author(s): jpalermo
- Status: Draft
- RFC Pull Request: [community#1049](https://github.com/cloudfoundry/community/pull/1049)

## Summary

Introduce a new optional component of bosh releases that allows release authors to specify the schema for their properties.
The bosh director, prior to rendering templates, will check for the schema, and if it exists, validate the deployment
properties against it, erroring if any are not valid.

## Problem

Bosh currently provides no property validation mechanism, so many release authors instead perform this validation
using ruby during template rendering. We discovered in the [draft RFC for a new templating language](https://github.com/cloudfoundry/community/pull/1004)
that there is a large need for property validation.

## Proposal

We adopt [JSON Schema](https://json-schema.org/), specifically the latest draft of the schema which is 2020-12.

Release authors would be able to place a `properties_schema.json` within a `job` folder. The bosh director
would then validate the deployment properties against the schema.

We may also duplicate this functionality within the bosh cli so `bosh create-env` deployments would also be able
to validate the deployment properties correctly.

JSON Schema defines several types, such as `string`, `number` and `object`. `object` allowing complex objects, the properties
of which can of their own type declarations and validations.

The various types also have type specific keywords that can be used for additional validation such as `minLength` or 
`pattern` which matches a string against a Regular Expression. `format` is another useful keyword, forcing a string to 
match a built in format such as `email` or `ipv4`.

[dependentRequired](https://json-schema.org/understanding-json-schema/reference/conditionals#dependentRequired) allows
certain properties to only be validated if other properties are present. There is also complicated [if-then-else](https://json-schema.org/understanding-json-schema/reference/conditionals#ifthenelse)
logic available within the Schema.

Something missing natively within JSON Schema is any sort of "Certificate" type. JSON Schema has extension points
although we probably don't want to use their more common "meta schemas" and define an actual schema for our certificate
validations. We performed a proof of concept and it was simple to simply add a new "Certificate" type and implement
custom validation of that data.

We do need help determining what custom validations to build.
- Validating a single Certificate?
- Validating a Certificate and Private Key match each other?
- Validating a single property has multiple Certificates and they are all valid?
- Validating particular attributes such as SAN match a specific value?

There are some existing property validations that may go beyond the scope of this effort though. For example, the 
[gorouter job](https://github.com/cloudfoundry/routing-release/blob/937bcd3cd96a75e0886fcc207f4fc38cdccf96ba/jobs/gorouter/spec#L617)
has the ability currently for the deployer to pass in validation rules for certificates. Those rules are then applied against
a different property entirely. This is probably possible to implement on the bosh director side in a custom certificate validator,
but it doesn't seem like something that would benefit more than this singular job.
