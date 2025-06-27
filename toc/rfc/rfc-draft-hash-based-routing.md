# Meta
[meta]: #meta
- Name: Hash-based routing
- Start Date: 2025-04-07
- Author(s): b1tamara, Soha-Albaghdady
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Cloud Foundry uses round-robin and least-connection algorithms for load balancing between Gorouters and backends. Still, 
they are unsuitable for specific use cases, prompting a proposal to introduce hash-based routing on a per-route basis to 
enhance load distribution in particular scenarios.

## Motivation

Cloud Foundry offers two load balancing algorithms to manage request distribution between Gorouters and backends. The 
round-robin algorithm ensures the number of requests is distributed equally across all available backends, and the 
least-connection algorithm tries to keep the number of active requests equal across all backends. A recent enhancement 
allows these load balancing algorithms to be configured on the application route level.

However, these existing algorithms are not ideal for scenarios that require routing based on specific identifiers.

An example scenario: users from different tenants send requests to application instances that establish connections to 
tenant-specific databases. With the current load balancing algorithms, each tenant eventually creates a connection to each 
application instance, which then creates connection pools to every customer database. As a result, all tenants might span 
up a full mesh, leading to too many open connections to the customer databases, impacting performance. This limitation 
represents a gap in achieving optimal load distribution and can be solved with routing based on a tenant.

## Proposal

We propose introducing hash-based routing as a load balancing algorithm for use on a per-route basis. This algorithm 
optimizes load distribution and addresses the issues described in the earlier scenario.

The approach leverages an HTTP header, which is associated with each incoming request and contains the specific identifier. 
This one is used to compute a hash value, which will serve as the basis for routing decisions.

In the previously mentioned scenario, the tenant ID acts as the identifier included in the header and serves as the basis 
for hash calculation. This hash value determines the appropriate application instance for each request, ensuring that 
all requests with this identifier are consistently routed to the same instance or might be routed to another instance 
when the instance is saturated. Consequently, this load balancing algorithm effectively minimizes database connection 
overhead and optimizes connection pooling, enhancing efficiency and system performance.

### Requirements

#### Only Application Per-Route Load Balancing
The hash-based load balancing will be configured exclusively as an application per-route option and will not be available as a global setting.

#### Minimal rehashing over all Gorouter VMs
Rehashing should be minimized, especially when the number of application instances changes over time.

[Maglev hashing](https://storage.googleapis.com/gweb-research2023-media/pubtools/2904.pdf) can be considered as a possible solution.

N hashes can be associated with one application instance. The number of hashes is a multiple of the number of application instances. 

#### Considering a balance factor
Before routing a request, the current load on each application instance must be evaluated using a balance factor. This load is measured by the number of in-flight requests. For example, with a balance factor of 150, no application instance should exceed 150% of the average load across all instances. Consequently, requests must be distributed to different application instances that are not overloaded.
Example:

| Application instance | Current request count	 | Request count / average load |
|----------------------|------------------------|------------------------------|
| app_instance1        | 10                     | 20%                          |
| app_instance2        | 50                     | 100%                         |
| app_instance3        | 90                     | 180%                         |

Based on the average load of 50 requests, new requests to app_instance3 must be distributed to different application instances that are not overloaded.

#### Deterministic handling of overflow traffic to the next application instance
The application instance is considered overloaded when the current request load of this application exceeds the balance factor. Overflow traffic should always be directed to the same next instance rather than to a random one.

A possible presentation of deterministic handling can be a ring like:

![](rfc-draft-hash-based-routing/HashRing.drawio.png)

### Required Changes

#### Gorouter
- The Gorouter MUST be extended to take a specific identifier via request header
- The Gorouter MUST implement a new `EndpointIterator` to calculate hash, based on the provided header 
- The Gorouter MUST consider consistent hashing 
- The Gorouter SHOULD locally cache the computed hash values to avoid expensive recalculations for each request for which 
  hash-based routing should be applied
- Gorouters SHOULD NOT implement a shared hash cache across instances in the same deployment
- The Gorouter MUST assess the current request load across all application instances mapped to a particular route in order to prevent overload situations
- The Gorouter MUST update its local hash table following the registration or deregistration of an endpoint, ensuring minimal rehashing

#### Cloud Controller
- The `loadbalancing` property of the [route object](https://v3-apidocs.cloudfoundry.org/version/3.190.0/index.html#the-route-options-object) MUST be updated to include `hash` as an acceptable value
- The [route options object](https://v3-apidocs.cloudfoundry.org/version/3.190.0/index.html#the-route-options-object) MUST 
  include two new properties, `hash_header` and `hash_balance`, to configure a request header as the hashing key and the balance factor
- The CF API MUST implement the validation of the following requirements:
  - The `hash_header` property is mandatory when load balancing is set to hash
  - The `hash_balance` property is optional when load balancing is set to hash. Leaving out `hash_balance` means the load situation will not be considered
  - To account for overload situations, `hash_balance` values should be greater than 110. During the implementation phase, the values will be evaluated to identify the best fit for the recommended range
  - For load balancing algorithms other than hash, the `hash_balance` and `hash_header` properties SHOULD not be set

An example for manifest with these properties: 
```yaml
version: 1
applications:
- name: test
  routes:
  - route: test.example.com
    options:
      loadbalancing: hash
      hash_header: tenant-id
      hash_balance: 125
  - route: anothertest.example.com
    options:
      loadbalancing: least-connection
```

The decision to introduce plain keys was influenced by the following points:
- Simple to use
- It allows for easy addition of more hash-related properties if new requirements arise in the future.
- It complies with the [RFC](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0027-generic-per-route-features.md#proposal), which states that the map must use strings as keys and can use numbers, strings, and the literals true and false as values

### No Changes Required

#### CF cli
The [current implementation of route option](https://github.com/cloudfoundry/cli/blob/main/resources/options_resource.go) 
supports the use of `--option KEY=VALUE`, where the key and value are sent directly to CC for validation. Consequently, 
the `create-route`, `update-route`, and `map-route` commands require no modifications, as they already accept the proposed properties.
Example: 
```bash
cf create-route MY-APP example.com -n test -o loadbalancing=hash -o hash_header=tenant-id -o hash_balance=125
cf update-route MY-APP example.com -n test -o loadbalancing=hash -o hash_header=tenant-id -o hash_balance=125
cf update-route MY-APP example.com -n test -o loadbalancing=hash -o hash_header=tenant-id
cf update-route MY-APP example.com -n test -o loadbalancing=hash -o hash_balance=125
cf map-route MY-APP example.com -n test -o loadbalancing=hash -o hash_header=tenant-id -o hash_balance=125
```

#### BBS
The route object is maintained as a generic JSON object in the BBS, likely because the BBS doesn't use the route 
information itself. Therefore, it simply accepts and stores the route options provided by the Cloud Controller.

#### Route-Emitter
The options are raw JSON and will be passed directly to the Gorouter without any modifications.

#### Route-Registrar
No use cases are known to implement hash-based routing for the platform-related routes. 

### Diagrams

#### An activity diagram for routing decision for an incoming request

![](rfc-draft-hash-based-routing/ActivityDiagram.drawio.png)

#### A simplified activity diagram for Gorouter's endpoint registration process

![](rfc-draft-hash-based-routing/EndpointRegistration.drawio.png)
