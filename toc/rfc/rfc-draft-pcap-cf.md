# Meta
[meta]: #meta
- Name: Integrate pcap feature for Cloud Foundry applications
- Start Date: 2025-09-10
- Author(s): @domdom82 @maxmoehl @peanball @ameowlia @mariash
- Status: Draft
- RFC Pull Request: [community#1309](https://github.com/cloudfoundry/community/issues/1309)

## Summary

Add a feature to Cloud Foundry that provides application developers with the
ability to perform packet capture (tcpdump) operations within their
application containers for debugging purposes. This RFC complements 
[RFC-0019 (pcap-bosh)](rfc-0019-pcap-bosh.md) by extending packet capture
capabilities from BOSH-level infrastructure debugging to application-level
debugging.

The main goal is to allow app developers to capture network traffic from
their applications when troubleshooting issues that require elevated
privileges, while maintaining security through operator controls and a
reduced-functionality custom tool.

## Problem

Application developers frequently need to perform in-depth troubleshooting
of their applications when deployed via Cloud Foundry buildpacks. Currently,
there is no possibility for app developers to perform privileged debugging
actions such as packet captures (tcpdump) within their application
containers.

When troubleshooting applications, it is common to require elevated
privileges for operations such as:
* Dumping network packets to analyze traffic patterns
* Investigating connectivity issues between application components
* Debugging network-related performance problems

While [RFC-0019 (pcap-bosh)](rfc-0019-pcap-bosh.md) addresses packet capture
at the BOSH infrastructure level for operators, there remains a gap for
application developers who need similar capabilities scoped to their
individual applications.

The challenge is providing this functionality while maintaining the security
model of Cloud Foundry, where applications run in isolated, unprivileged
containers.

## Proposal: Custom Packet Capturing Tool

This RFC proposes implementing a reduced-functionality packet capturing tool
written in Go using the `gopacket` library. This custom tool would be
injected into application containers via Diego, similar to how `diego-ssh`
currently provides SSH access.

### Key Features

**Reduced Attack Surface**: The custom tool supports only essential packet
capture operations:
* Specifying a network interface
* Applying packet filters (pcap-filter format)
* Setting snapshot length (snaplen)
* No support for arbitrary code execution or complex operations

**Injection Mechanism**: The tool would be injected via Diego using a mechanism
similar to `diego-ssh`, ensuring:
* Consistent deployment across all application instances
* Proper integration with Cloud Foundry's security model
* Ability to control access through feature flags

**Operator Controls**: 
* Platform-wide feature flag to enable/disable packet capture functionality
* Per-application feature flag support for granular control
* Integration with Cloud Foundry's existing permission model

**Security Model**:
* Tool runs with necessary capabilities (`CAP_NET_RAW` and `CAP_NET_ADMIN`)
  but limited functionality
* No shell access or ability to execute arbitrary code
* Scoped to the application's network namespace

### Usage Example

```bash
# Capture HTTP traffic for myapp
cf pcap myapp --interface eth0 --filter "tcp port 80" --snaplen 1500

# Capture specific instance with custom filter
cf pcap myapp --instance 1 --filter "host database.example.com"
```

## Other Options Considered

#### Option 1: `sudo` Access

Adding a platform switch to make the `vcap` user a sudoer was considered but
discarded due to:
* Significant security risks of providing full root access
* Potential for privilege escalation beyond intended packet capture use
* Inconsistency with Cloud Foundry's security-first design principles

#### Option 2: `setcap` on `tcpdump` Binary  

Setting capabilities on the existing `tcpdump` binary was considered but
discarded because:
* `tcpdump` offers functionality to run arbitrary code in its security
  context
* Demonstrated security vulnerabilities allowing code execution
* Difficulty in hiding behind feature flags due to unconditional
  deployment
* Broader attack surface compared to a purpose-built tool

### Relationship to Existing Solutions

This RFC complements [RFC-0019 (pcap-bosh)](rfc-0019-pcap-bosh.md) by
addressing different use cases:

* **pcap-bosh**: Infrastructure-level debugging for operators across BOSH
  deployments
* **pcap-cf**: Application-level debugging for developers within CF
  applications

## Implementation Considerations

#### diego-release: Custom Packet Capturing Tool

A new package will be added to diego-release which implements packet capturing
in go through the `gopacket` library. The resulting binary will be included in
the various lifecycle archives that are added to the final app container and
the necessary capabilities (`CAP_NET_RAW` and `CAP_NET_ADMIN`) will be assigned
to the executable via file capabilities. This allows regular users to gain those
capabilities when executing the binary.

#### CF CLI: New `pcap` command

Similar to the `bosh pcap` command a `cf pcap` command will be added. Like its
predecessor it will connect to the desired instances via SSH and execute the new
packet capturing tool and stream back the captured packets via stdout. If there
are multiple streams, the CLI will merge them and write them out to a single
file in the pcap format.

## References

* Prior discussions:
  * https://github.com/cloudfoundry/diego-release/issues/1023
  * https://cloudfoundry.slack.com/archives/C0DEQSW9W/p1744034414856129?thread_ts=1744034414.856129&cid=C0DEQSW9W
  * https://cloudfoundry.slack.com/archives/C033RE5D6/p1744299390390049
* https://github.com/cloudfoundry/pcap-release
* https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0019-pcap-bosh.md
* https://github.com/gopacket/gopacket
