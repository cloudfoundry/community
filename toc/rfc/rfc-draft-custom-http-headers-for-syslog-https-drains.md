# Meta
[meta]: #meta
- Name: Support Custom HTTP Headers for Syslog HTTPS Drains
- Start Date: 2025-06-30
- Author(s): ZPascal
- Status: Draft
- RFC Pull Request: [community#1228](https://github.com/cloudfoundry/community/pull/1228)

## Summary

This proposal introduces support for specifying **custom HTTP headers** in **HTTPS syslog drains** for Cloud Foundry's Loggregator system. It enables native, secure integration with third-party logging systems that require authentication via bearer tokens or custom headers, such as **Splunk HEC**, **Datadog**, and similar modern log routing solutions.

## Problem

Modern observability platforms increasingly rely on HTTP-based ingestion with authentication through bearer tokens or custom headers (Splunk, Datadog). Currently, Loggregator supports HTTPS drains but **does not allow adding custom headers**, making integration with key services (e.g., Splunk HEC, Datadog, New Relic, Elastic) difficult or impossible without proxies or custom sidecar containers. Using proxies adds complexity and operational burden, while putting authentication in drain URLs is insecure and often not compatible.

## Proposal

We propose the following enhancements:

1. **Extend the syslog drain binding specification** to allow a `headers` field (key-value map).
2. Modify Metron Agent and Syslog Adapter components to **inject the custom headers** into outbound HTTPS syslog requests.
3. Implement **validation logic** to block prohibited/unsafe headers (such as `Host`, `Content-Length`).
4. Ensure the headers field is visible in drain metadata available to platform operators and log integration tools.

### Example configuration

#### Example CUPS call
```bash
cf create-user-provided-service DRAIN-NAME -l SYSLOG-URL -p '{"headers": {"Authorization": "Bearer abc123xyz", "X-Splunk-Request-Source": "cloudfoundry"}}'
```

#### Forwarded JSON details
```json
{
  "headers": {
    "Authorization": "Bearer abc123xyz",
    "X-Splunk-Request-Source": "cloudfoundry"
  }
}
```