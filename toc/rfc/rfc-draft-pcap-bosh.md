# Meta
[meta]: #meta
- Name: Integrate pcap feature into BOSH
- Start Date: 2023-07-06
- Author(s): @domdom82 @maxmoehl
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/640


## Summary

Members of the [App Runtime Platform WG](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-platform.md) are developing a BOSH release called [pcap-release](https://github.com/cloudfoundry/pcap-release) which adds network traffic capturing tools to both BOSH deployments and Cloud Foundry applications.
The release was created after an initial discussion was started on the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/issues/980) repository.

Since then, the project has evolved into a BOSH use case and a Cloud Foundry use case. This RFC discusses a proposal to get the BOSH use case integrated with BOSH director and BOSH cli.

The main goal of the pcap feature is to allow users (BOSH operator in this case) to easily capture network traffic across multiple VMs by specifying various parameters in PCAP CLI:
- BOSH deployment
- BOSH instance group(s)
- BPF [Berkeley Packet Filter](https://www.tcpdump.org/manpages/pcap-filter.7.html) filter to apply

PCAP CLI will form a capture request and send it to PCAP API. The capture will then take place in real-time similar to running [tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html) in a distributed fashion across multiple machines. The PCAP API will contact PCAP AGENT on all nodes involved and trigger a network capture. The PCAP AGENTs will concurrently stream all captured traffic back to PCAP AGENT where all streams are merged into one contiguous stream that is sent back to the PCAP CLI where it is then stored as a PCAP FILE on disk.

Trust is established as follows:
1. PCAP CLI uses the BOSH CLI `access_token` and sends them to PCAP API
2. PCAP API verifies `access_token` against BOSH UAA and establishes mTLS with PCAP AGENT
3. PCAP AGENT only accepts mTLS connections from PCAP AGENT via a trusted CA

## Problem

The current architecture for "PCAP for BOSH" is depicted as follows:

![PCAP BOSH Architecture](rfc-draft-pcap-bosh/tcpdump-for-bosh.svg)


There are several flaws with this architecture that are the result of missing integration:
1. The PCAP BOSH CLI does not share context with BOSH CLI (because unlike CF CLI, BOSH CLI has no plugin mechanism).
2. PCAP BOSH CLI reads the user's `access_token` and `refresh_token`, talk to BOSH UAA to get a new `access_token` using the `refresh_token` and write both back to `.bosh/config` - a file which is also accessed by BOSH CLI.
3. The `access_token` is then sent to PCAP API which uses it as a credential to talk to BOSH DIRECTOR
4. PCAP API needs to speak to BOSH DIRECTOR in order to find the endpoints (IP:PORT) of each PCAP AGENT needed for the capture.
5. In order to make this feature work, PCAP AGENT needs to be available on all BOSH managed VMs. The only way today would be to use it as an [addon](https://bosh.io/docs/runtime-config/#addons)

## Proposal

### Integrate PCAP CLI as a "pcap" keyword into BOSH CLI

- This would allow PCAP BOSH CLI to share context with BOSH CLI and have access to the user's login session as well as the currently used BOSH environment.

- Another benefit would be that users would not have to download the PCAP BOSH CLI separately. 

### Integrate PCAP AGENT with BOSH AGENT

- This would make network capture a "built-in" feature of BOSH. It removes the need to manually add PCAP AGENT as a job to deployment manifests or configure it as an addon.

### Co-locate PCAP API with BOSH DIRECTOR

- This would make it very easy for PCAP CLI to find the right endpoint of PCAP API, likely via the `/info` endpoint of BOSH DIRECTOR.
- No route-registrar or gorouter would be needed to announce any routes. The endpoint would be implicitly known via the BOSH CLI.
- Possible caveat: Large network dumps could strangle network bandwidth on BOSH DIRECTOR. Therefore an option to have several PCAP API nodes (load-balanced via BOSH DNS) deployed separately may be considered as an alternative.