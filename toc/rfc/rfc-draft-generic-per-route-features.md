# Meta
[meta]: #meta
- Name: Generic Per-Route Features
- Start Date: 2024-01-08
- Author(s): @maxmoehl, @domdom82
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

## Problem

Implementing per-route features in Cloud Foundry is a tedious process because it requires
changes to multiple components in multiple working groups. Most components will only need to be
made aware of new fields without adding any significant logic but the overhead of making the
change still exists.

On the other side are the components that actually need to be aware of the change. Mostly the
routing components (gorouter, maybe route-emitter / -registrar), the API (cloud controller)
and UIs (CLI).

## Proposal

To reduce the overall overhead of implementing new per-route features we propose to add a generic
key-value map to the definition of a route across all components. All components handling the map
SHOULD ignore the contents of the map except gorouter, cloud controller and cf CLI which MUST handle
the map and its values accordingly. Other components MAY limit the size of the map or size of
keys / values for technical reasons.

The following constraints apply (types are as specified in [RFC 8259](https://rfc-editor.org/rfc/rfc8259)):
* The map MUST be representable as an object.
* The map MUST only use strings as keys.
* The map MUST only use numbers, strings and the literal values `true` and `false` as values.

### Required Changes

#### CLI

There MAY be either individual command line flags or a single flag which supports generic key-value
pairs for the `map-route` sub-command.

#### Cloud Controller

The API MUST specify and implement a new field to carry the map inside the route object. The API
MUST implement per-field validations as features of the map are specified. The route MUST be
rejected with an appropriate error message if the provided map is invalid and MUST be passed on
as-is otherwise. The API also MUST store the map as a generic key-value map to ensure changes to
the map do not require a change to the database schema.

Support for a generic map MUST be added to the manifest. The updated routes section in a manifest
MAY look like this:

```yml
version: 1
applications:
- name: test
  routes:
  - route: example.com
    options:
      loadbalancing-algorithm: round-robin
      connection-limit: 15
      session-cookie: FOOBAR
      trim-path: true
  - route: www.example.com/foo
    protocol: http2
  - route: tcp-example.com:1234
```

Implementation details:
* Add a new field to the [route model](https://github.com/cloudfoundry/cloud_controller_ng/blob/main/app/models/runtime/route.rb).
* Add validation to the [route validator](https://github.com/cloudfoundry/cloud_controller_ng/blob/e719d017ea4625397a97c2c14352ebdee66febe9/lib/cloud_controller/route_validator.rb#L2).

#### BBS, Rep, Executor, Route-Emitter

The diego components MUST add support for the new field specified by the API and forward the
contents as-is without modification or, if the field exceeds technical limitations, MUST raise an
error.

### Route-Registrar

Route-registrar MUST offer the new features in its config as they are added to the other
components.

#### Gorouter

Gorouter MUST accept the new field and parse its contents. If the map cannot be parsed it MUST
be ignored. If individual key-value pairs are invalid those MUST be ignored and other key-value
pairs MUST still be parsed and acted upon.

It MAY be decided to implement one feature as part of this RFC which would be implemented together
with the generic logic for supporting the new map.

As new features are specified they MUST be implemented in gorouter.

Example `router.register` NATS message containing additional options (field names and values are not
final):

```json
{
  "host": "127.0.0.1",
  "port": 4567,
  "tls_port": 1234,
  "protocol": "http1",
  "uris": [
    "my_first_url.localhost.routing.cf-app.com",
    "my_second_url.localhost.routing.cf-app.com/some-path"
  ],
  "tags": {
    "another_key": "another_value",
    "some_key": "some_value"
  },
  "options": {
    "lb-algo": "least-conn",
    "conn-limit": 100,
    "cookie": "my-session-cookie",
    "trim-path": true
  },
  "app": "some_app_guid",
  "stale_threshold_in_seconds": 120,
  "private_instance_id": "some_app_instance_id",
  "isolation_segment": "some_iso_seg_name",
  "server_cert_domain_san": "some_subject_alternative_name"
}
```

To-Do:
* Can we somehow report errors from gorouter back to the user?

### Specifying Features

It's the responsibility of the App Runtime Platform Working Group (ARP-WG) to specify new
features based on what is specified in this RFC. When a new feature is proposed the ARP-WG uses
the process it would use for any new feature to decide whether and how it should be implemented. It
MAY involve other working groups in the process.

### Features Which Could be Implemented

So far we have collected a list of features which would benefit from a more flexible approach to
per-route features:

- Custom Load-Balancing Algorithm
- Custom Connection Limits
- Custom session cookie name (currently set on platform level, mostly to `JSESSIONID`)
- Option to trim path mapping on request (i.e. an app mapped to `/some-path/` receiving a request `GET /some-path/books` will see the request as `GET /books` if the `trim-path` option is set, instead of the full path)

To-Do:
* Collect more feedback and extend the list.

All of these options are already (or could easily be made) configurable for the entire CF
installation. Changing them will almost certainly break existing scenarios which is why we
are looking for a cheap way to gradually allow for more configuration per route.
