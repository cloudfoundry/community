# Meta
[meta]: #meta
- Name: Add OTel Collector for aggregate metric egress
- Start Date: 2023-07-07
- Author(s): @ctlong, @mkocher, @acrmp, @rroberts2222
- Status: Draft <!-- Acceptable values: Draft, Approved, On Hold, Superseded -->
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Members of the [App Runtime Platform WG](https://github.com/cloudfoundry/community/blob/main/toc/working-groups/app-runtime-platform.md) propose adding an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) to every CF-D VM to forward all app and platform metrics on those VMs to external drains. Operators would be able to choose between different protocols and settings provided by the Collector out-of-the-box when inputting their metric destinations.

We believe the Collector deployed in this manner would not only solve our current problem. In the long run we could leverage it for other interesting new functionality with logs and traces, as well as reducing our agent suite footprint.

## Problem

Many operators and Cloud Foundry maintainers have problems with the firehose. The firehose requires two sets of coordinating vms, which is inherently unscalable, and a Cloud Foundry-specific nozzle translation layer, which no one wants to maintain. We would like to retire the firehose, and to that end built out the syslog drain system. However, we continue to see operators stay on the firehose, using barely supported nozzles. In order to retire the firehose completely, operators need a way to egress metrics, as well as logs, off the platform to their monitoring tools of choice.

Our agent suite currently provides metrics via a prometheus endpoint. However using this endpoint requires being on the local network and having certificates provisioned via bosh. This is challenging when the monitoring tool is run by another department, and even more challenging when the monitoring tool is a hosted SaaS product.

## Proposal

Diagram link: https://drive.google.com/file/d/1-cuOwPdKokeeNvUoZ4bpcbh60Vv5J5JX/view?usp=sharing

### OpenTelemetry Collector Add-On

Provide a new experimental ops file in the cf-deployment repo (that could later be promoted, if desired). This ops file would add a OpenTelemetry Collector BOSH job to all CF-D VMs.

It would accept [Exporter configuration](https://opentelemetry.io/docs/collector/configuration/#exporters) as a new BOSH property, for example:

```yaml
exporters:
  description: "Exporter configuration for aggregate metric egress"
  default: {}
  example: |
    otlp:
      endpoint: otelcol:4317
    otlp/2:
      endpoint: otelcol2:4317
```

The BOSH job would register itself with the Forwarder Agent to receive OTLP metrics.

### Forwarder Agent

Update the Forwarder Agent to support forwarding metrics to the OpenTelemetry Collector via OTLP.

### Option to Shut Down the Firehose

Add an experimental ops file to the cf-deployment repo allowing operators to “turn off” the firehose by removing Loggregator v1 and v2 components.

## FAQ

### Why OpenTelemetry over other potential solutions (e.g. Fluent, Telegraf, etc.)?

The majority of the OpenTelemetry codebase is written in Go, and the project seems to have more open source backing than comparable projects. We quickly decided that using an agent written in a language that many of us are unfamiliar with would be too much of a maintenance burden (i.e. Fluent Bit which is written in C), and discounted those projects. Some projects were also written in Go (i.e. Telegraf) but weren’t as strongly disposed to open source engagement, which we think will be important for adding features we care about, if necessary.

### Why place the OpenTelemetry Collector on each VM?

When deciding where to place the OpenTelemetry Collector, we considered placing it in a sidecar, creating a separate instance group, and placing the collector on each VM. After weighing the pros and cons of each, we decided that colocation on each VM was the best option. This option ensures that the OpenTelemetry Collector is scaled proportionally to the size of the platform. If it was located in a separate instance group, it would have to be scaled individually and could result in a noisy neighbor antipattern. Colocation also allows both app and component metrics to be forwarded, unlike the sidecar solution which would only provide app metrics. Finally, having the Collector on each VM follows the pattern set in Shared Nothing of having logging agents on each VM. Because of the above, we found it to be the fastest and most intuitive placement.

### How will the OpenTelemetry Collector perform?

We have done some performance testing of the Collector and determined that it should be performant enough to function as intended. In particular: running the Collector on a BOSH VM to scrape the Metrics Agent every 5 seconds, and export over OTLP to Honeycomb, over the course of 15 minutes resulted in the following observed memory usage and CPU Time:
* Resident set size: 151M.
* CPU Time: 0:06.49.

### Won’t this require rolling all my VMs if I add a new aggregate metric drain, or update an existing drain?

Unfortunately, yes. We considered integrating OpAmp, or writing our own supervisor for the OpenTelemetry Collector. However, OpAmp is still in development and doesn't seem stable enough to commit to. Additionally, writing our own supervisor proved difficult due to limitations with the Collector (e.g. no hot reloading, limited configuration reload options) and BPM (e.g. cannot put two processes in the same namespace). We could look to add either in the future if it becomes necessary.
