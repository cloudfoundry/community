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

## Timeline

We would like to get feedback on this through the first week or two of February and then implement the functionality on 
the Bosh Director in the second half of February. A new major release of the director would be released at the end
of February that has this available to release authors. A new major version of the CLI would have to be released at the
same time that includes the functionality to package up the `properties_schema.json` file when creating the release.

The `bosh create-env` functionality would probably not follow immediately. As we'll have to duplicate any custom schema
validations in both places, we'll probably wait for things to settle down a bit, but I could see this work getting
done in the second half of 2025.

## Examples
The very simple login_banner job of os-conf release has only a single property:
```yaml
properties:
  login_banner.text:
    description: Login banner text
```
and the schema to validate it as a string:
```yaml
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "login_banner": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string"
        }
      }
    }
  }
}
```

A more complicated example from the gorouter release nats certificate properties. Currently if you specify one, you must specify the other.
```yaml
properties:
  nats.cert_chain:
    description: Certificate chain used for client authentication to NATS. In PEM format.
  nats.private_key:
    description: Private key used for client authentication to NATS. In PEM format.
```
schema for just the required aspect of these two properties:
```yaml
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "nats": {
      "type": "object",
      "properties": {
        "cert_chain": {
          "type": "string"
        },
        "private_key": {
          "type": "string"
        }
      },
      "dependentRequired": {
        "cert_chain": ["private_key"],
        "private_key": ["cert_chain"]
      }
    }
  }
}
```
