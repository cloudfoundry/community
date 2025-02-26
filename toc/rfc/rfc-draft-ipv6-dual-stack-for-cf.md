# Meta

- Name: IPv6 Dual Stack Support for Cloud Foundry
- Start Date: 2025-02-07
- Author(s): @peanball, @a-hassanin, @fmoehler, @dimitardimitrov13, @plamen-bardarov
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)

## Summary

IPv6 becomes increasingly prevalent on the internet and slowly also in the networks of large customers.

This RFC proposes to add IPv6 support to various Cloud Foundry components in addition to the existing networking in CF that is based on IPv6. The goal is to support Dual Stack, i.e. IPv4 *and* IPv6 at the same time. This support is particularly relevant for basic extension and migration of existing CF foundations that are based on IPv4 and allow them to also communicate via IPv6.

Furthermore, the goal is to add support IPv6 (i.e. allow Dual Stack) for both ingress and egress traffic, ensuring that Cloud Foundry can handle inbound and outbound network communication using IPv4 and IPv6, further enhancing compatibility and future-proofing the platform.

## Problem

IPv6 support in Cloud Foundry has only reached a few CF components so far. Furthermore, the existing support often only supports one type of networking exclusively.

Additionally, there are areas in the CF design informed by the limited address space of IPv4:

* Workloads in Diego are interconnected via an overlay network managed by the Silk CNI. An overlay network is primarily needed to provide enough address space for the apps running within Diego and offer a network that spans all workloads.
* On hyperscalers, egress traffic from apps requires a NAT gateway. Providing public IP addresses for all Diego cells is often not economical.
* BOSH allows assigning a single IP address per BOSH network entry for a VM, not CIDR ranges.

Adding IPv6 support should not transfer those same issues onto the IPv6 implementation.

## Proposal

The goal is to use IPv6 best practices and benefits to the full extent with the following high-level goals:

1. NAT and port forwarding are avoided wherever possible when using IPv6
2. Application workloads have their own IPv6 address. This allows better correlation between requests and their origin. It is important to note that application workloads shall not be addressable directly from external networks. The ingress and load balancing via Gorouter must remain.
3. Support of dual stack networking, i.e. IPv4 and IPv6 at the same time. This is primarily for a smoother migration because the IPv6 changes can then be additive.
4. IPv6 is additive to IPv4 functionality

The ultimate future goal would be to allow a configuration based on pure IPv6 communication, i.e. to allow disabling IPv4 entirely. This is not a current priority and is not covered in this proposal. Options to still connect to IPv4 from an IPv6-only cloud foundry foundation at the edges would be via NAT64 and similar technologies.

Backward compatibility is an important topic. Any changes that would change the default behavior should be placed behind appropriate configuration flags and turned off by default. The absence of IPv6 specific configuration must also remain without side effects to existing CF foundations.

### Overview

The largest conceptual change is providing individual addressing for application instances. Diego is a container runtime that is closely integrated with various other components. By extending the addressing schema to per-container addresses, all components that touch application workload information need to be adjusted.

The baseline dual stack support for networks deployed via BOSH is another pillar of the proposed change.

The following sections outline the changes necessary for various core components of  a typical CF foundation.

### BOSH

BOSH is used to provision and configure the VMs that run the components of Cloud Foundry. The following features are needed to support the goals of this proposal:

1. Assignment of IPv6 addresses in addition to IPv4, ideally to the same NIC
2. Assignment of IPv6 CIDR ranges (prefix delegation), e.g. assign a `/80` address, while avoiding overlapping. This is relevant for the use case of address delegation to application workloads hosted on Diego cells.

#### BOSH Director

Depending on the configuration of the prefix in the cloud config networks section. The Director should:

1. Either pass the desired ipv6 CIDR range directly to the cpi (networks.cloud_properties section) the cpi then must figure out which range to attach (e.g. if multiple instances use the same network).
2. Select the next available IPv6 prefix from the overall CIDR range (networks section) and send that to the cpi.

The IP address range configuration and prefix delegation are configured via cloud config, e.g. as follows:

```yaml
networks:
  - name: diego_cells_ipv6
    subnets:
      - az: z1
        cloud_properties:
          # assign non-overlapping `/80` cidrs from `range`
          ipv6_prefix_delegation_size: 80
          security_groups:
            - sg-abcd...
          subnet: subnet-12345
        dns:
          - 2001:db8:4e04:D139:0000:0000:0000:0253
        gateway: 2001:db8:4e04:D139:0000:0000:0000:0001
        range: 2001:db8:4e04:D139:0000:0000:0000:0000/64
        reserved:
          - 2001:db8:4e04:D139:0000:0000:0000:0000/80
```

This defines the CIDR range for diego_cells_ipv6 as 2001:db8:4e04:D139::/64, which is then subdivided into `/80` CIDR ranges that are assigned to each next VM in that network.

The “first” CIDR (2001:db8:4e04:D139:0::/80) is then reserved for “internal” use, e.g. DNS, gateway addresses. Accordingly, the following CIDRs could then be assigned to Diego cells:

* `2001:db8:4e04:D139:0001:0000:0000:0000/80`
* `2001:db8:4e04:D139:0002:0000:0000:0000/80`
* …

#### BOSH Cloud Provider Interfaces (CPIs)

The Cloud Provider Interfaces abstract the underlying infrastructure and apply the logical configuration defined in BOSH to concrete infrastructure elements. Accordingly, the CPIs must be aware and capable of assigning and managing IPv6 addresses for BOSH managed networks.

The following functionality is required in each CPI that supports dual stack networking:

1. Enable dual stack mode if two manual networks refer to the same subnet
This is [done](https://github.com/cloudfoundry/bosh-aws-cpi-release/pull/174) for AWS, but pending for other hyperscalers and infrastructures.
2. Depending on the decided configuration in the cloud config and director implementation the cpi should:
   * Assign an IPv6 prefix to a single VM where possible. The size of the prefix to be assigned must be configurable. Assignment must be done from a known pool, i.e. a larger CIDR range for the deployment that is then subdivided for each VM. This pool is also configurable. The CPI is responsible of providing information about available CIDR ranges, verifying that configuration is consistent and communicating with the infrastructure to apply the necessary assignments and mappings.
   * Try to attach the IPv6 prefix passed in from the director

#### BOSH Agent

The BOSH Agent that is running on BOSH managed VMs is ultimately responsible for applying operating system level configuration. This includes network interface configuration.

For supporting dual stack networking, the BOSH agent must support the following:

1. Allow the agent to accept having multiple network settings for the same network

   The BOSH Agent has a limitation that allows only a single BOSH network to be assigned to a Network Interface Card (NIC) in a virtual machine. When multiple BOSH networks are defined for the same hyperscaler subnet,
   This limitation [has been resolved with bosh-agent#344 already.](https://github.com/cloudfoundry/bosh-agent/pull/344)

2. With the BOSH CPI being able to delegate IPv6 prefixes to single VMs, the BOSH agent MUST be able to assign such CIDRs to VMs or at least not interfere with the setup (e.g. https://github.com/cloudfoundry/bosh-agent/pull/347 ), if the target infrastructure allows.

#### BOSH Stemcells

BOSH stemcells up to Ubuntu Jammy Jellyfish have IPv6 support disabled at kernel level. While it can be enabled, the resulting configuration change requires a VM reboot.

The goal is to keep the already enabled IPv6 support from Ubuntu upstream enabled.
This will be the case starting with Ubuntu Noble stemcell. Enabling IPv6 in older stemcell releases such as “Ubuntu Jammy” might be seen as backwards incompatible change.

This topic is being discussed and tracked via the [issue os-conf-release#71](https://github.com/cloudfoundry/os-conf-release/issues/71) and must be followed up with appropriate fixes.

### Diego

Currently, the Silk CNI is used to create an overlay network, but also to assign IP addresses for the application containers. This assignment is done from a centrally managed pool of IP addresses.

The goal of having distinct IPv6 addresses for the various containers can be achieved without such a central assignment. A Linux machine can receive a CIDR range on its network interface, e.g. `/80` or smaller, and receive traffic for any address within that range.

The delegation of IPv6 addresses within the cells is managed through the host-local CNI plugin. Each cell is assigned an IPv6 prefix at the configuration level, which is then provided to the host-local IPAM plugin. Using this prefix, the plugin allocates unique IPv6 addresses to individual containers within the cell. To prevent address conflicts and ensure proper tracking, a state file is maintained at the cell level, keeping a record of all assigned addresses.

This single machine, i.e. a Diego cell, then has sole control over this network range and can use it to assign specific IP addresses to its containers. At a network level, traffic is still sent to the Diego cell, and within the Diego cell can be forwarded to the application container based on its IP address directly as part of the networking stack.

Network traffic from and to application containers needs to be controlled, also for IPv6:

1. For inter-container communication, Application Security Groups (ASGs) need to add support for IPv6.
2. When publicly routable addresses (Global Unicast Addresses (GUAs) in IPv6) are assigned to each application container, traffic from outside the foundation needs to be blocked.

BBS, Executor and Garden components need to be extended to support the ICMPv6 protocol for ASGs.

Finally, some adaptations for the containerized workloads are necessary:

1. The [environment variables](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#app-system-env) `CF_INSTANCE_IP` and `CF_INSTANCE_INTERNAL_IP` will need IPv6 equivalents, or extension.
2. Instance identity IDs, i.e. the certificates used by Envoy in the app container, need to support IPv6 addresses. Currently, they are issued for the IPv4 address only.

### Silk
1. Silk Daemon is responsible for retrieving the network lease for the cell from Silk Controller and providing it to the CNI Plugin.
   - Enhancement: Add a new configuration property for an IPv6 prefix.
   - Behavior:
     - If an IPv6 prefix is provided and the host is IPv6 enabled, Silk Daemon returns both IPv4 and IPv6 networks.
     - If no IPv6 prefix is provided, the system defaults to IPv4-only behavior.
2. CNI Plugin is responsible for setting up the network devices on both container and host side. It delegates the IPv4 CIDR from the silk daemon to the IPAM host-local plugin, which allocates addresses from the network.
   - Enhancements:
     - Extend the existing logic to support IPv6 address assignment on already created devices.
     - Configure point-to-point communication, routing tables, and static neighbors (similar to ARP tables in IPv4).
     - Enable IPv6-specific sysctl security settings.
     - Store the IPv6 address in the Silk datastore.
   - Behavior:
     - The plugin only configures IPv6 if Silk Daemon returns an IPv6 prefix and the host supports IPv6.
3. CNI Wrapper Plugin currently creates default iptables rules (`netin-*`, `netout-*`, `overlay-*` chains) with default `REJECT` rules and `ALLOW` rules for DNS and "host services." In deployments without vxlan-policy-agent enabled, it also manages iptables egress rules.
   - Enhancement: Extend it to apply IPv6 firewall rules using ip6tables:
     - Maintain default REJECT rules for IPv6.
     - Allow DNS and host service traffic.
     - Ensure IPv6 egress rules are correctly handled when vxlan-policy-agent is disabled.
4. VXLAN Policy Agent creates the dynamic iptables rules for ASGs and C2C Policies.
   - Enhancement: Extend it to support IPv6 ASGs, ensuring that:
     - Security group rules from Policy Server are properly filtered and applied based on IP version.
     - The system supports both IPv4-only and dual-stack ASG enforcement.

General Behavior and Compatibility: 
- The existing IPv4 functionality remains unchanged.
- If the host supports IPv6 and a prefix is provided to Silk Daemon, additional IPv6 configuration will be applied on top of the current setup.
- If VXLAN Policy Agent is configured with IPv6 support, dynamic ASGs will also be created as ip6tables rules.

### Cloud Controller

Changes to the cloud controller are primarily in the following areas:

1. Support forwarding and retrieving of IPv6 addresses in any records that may have IP addresses
2. Support binding to IPv4 and IPv6 for the CAPI server, depending on the VM’s configuration
3. Support of IPv6 in metadata, e.g. Application Security Groups

### Cloud Foundry CLI

The Cloud Foundry CLI shows the application workload’s addresses in various places. Those places need to be extended to support the display of IPv6 addresses, as retrieved via the CF API:

1. IPv6 support for configuring application security groups
2. …

### Networking

Network Policies that are stored in [the policy-server-api which is part of cf-networking-release](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/08-policy-server-api.md).

Network policies may reference IP address ranges as destination. Destinations are stored as strings. The underlying IP ranges are also [strings with a start and end address](https://github.com/cloudfoundry/cf-networking-release/blob/aa25a3f96dc21e8a3e25db10f741e4f678c78464/src/code.cloudfoundry.org/policy-server/api/api.go#L37-L49). The data is ultimately serialized JSON that is stored in a database column. As IPv6 addresses are longer than IPv4 addresses, we might need to bump the table size, when IPv6 is added.

### Routing

The largest impact on routing is Gorouter and in tcp-router via and routing-api. They all consume endpoint information provided by route-registrar or route-emitter. Such endpoint information usually points to an IP address and port.

Endpoint information must support IPv6 address + port information in addition to IPv4 addresses.

![Routing architecture](https://docs.cloudfoundry.org/concepts/images/cf-routing-architecture.png)

#### Gorouter

Gorouter is largely based on the Golang implementation for HTTP request processing and routing. This implementation is capable of IPv6 address resolution and communication. Gorouter’s route registry and its endpoint handling are also well contained

For the scope of this RFC, testing and fixes for small unforeseen issues are considered, but no direct work is expected for supporting IPv6 targets.

#### TCP-Router and Routing API

routing-api and tcp-router need to be verified, and if necessary extended, to support IPv6 addresses in addition to IPv4 addresses.

### cf-deployment

There shall be an (experimental) opsfile that enables IPv6 / dual stack support. This opsfile shall be updated, as new components add support for dual stack networking.

This opsfile should also be used in a new validation pipeline that tests the current state of cf-deployment with dual stack enabled.

### General IPv6 / Dual Stack Communication Support

Daemons providing endpoints (HTTP(s) or others), shall support listening on IPv4 and IPv6 sockets.

Most fundamental networking libraries used in those already support binding to IPv6 or dual stack socket configurations. Implementation must ensure that a configruation to listen on all protocol versions is possible, e.g. by listening on `::$PORT`.

#### Server Sockets and API Ports

The following components need to be verified (non-exhaustive list. All components that run on IPv6 enabled/Dual Stack stemcells need to support binding to IPv6):
* Cloud Controller
* Policy Server
* UAA
* Credhub
* BBS
* Routing API
* NATS
* BOSH
  * DNS
  * Director
  * Agent

Where a listening address can be provided, we need to ensure that IPv6 or dual stack listening configurations can be provided.

#### Client Support

The BOSH CLI and CF CLI must allow connecting via IPv4 and IPv6. The on-disk configuration must support IPv4 and IPv6 addresses, when the endpoints are not defined as DNS names.

## Testing

Besides tests in the respective components, integration tests need to be created that utilize IPv6.

### Cloud Foundry Acceptance Tests (CATs)

Cloud Foundry acceptance tests shall be extended to also exercise IPv6 communication. This can either be specfic new tests, or execution of the test suite in a full IPv6 configuration, in addition to the existing IPv4 configuration.

### bosh-bootstrap (`bbl` environments)

bosh-bootstrap shall be extended to support IPv6 / dual stack configuration.

bosh-bootstrap is used, among other things, for setting up the environments that are running CATs.


## Other Topics

### Windows Support

Windows support does not require additional requirements or specification in addition to the above. Windows supports IPv6, and IPv6 support is available in the Windows stemcell.
