# Meta
[meta]: #meta
- Name: Support Org- and Space-Based Certificates for Loggregator Syslog TLS/mTLS Drains
- Start Date: 2025-06-30
- Author(s): ZPascal
- Status: Draft
- RFC Pull Request: [community#1229](https://github.com/cloudfoundry/community/pull/1229)


## Summary

This RFC proposes to introduce support for **organization- and space-scoped client certificates** for Cloud Foundry Loggregator syslog drains using mutual TLS (mTLS), covering both **HTTPS** and **syslog+TLS** protocols. By issuing certificates at the org or space level instead of per application, this initiative will simplify certificate lifecycle management, enable centralized rotation, and facilitate integration with central certificate authorities. The change targets the reduction of operational overhead and the enhancement of tenant-level security.

## Problem

Currently, Cloud Foundry syslog drains using mTLS rely on **application-specific client certificates**. This causes high operational overhead, especially in large environments, because:

- Certificates are tied to individual app instances and require frequent re-issuance.
- Rotating certificates across many apps is error-prone and challenging to coordinate.
- Managing a large number of app-level certificates leads to poor scalability and maintainability.

Without org/space-scoped certificates, operators struggle with scaling, secure rotation, and integration with enterprise PKI.

## Proposal

The following capabilities are proposed:

1. **Org/space-scoped certificate issuance**: When a syslog drain is created, the drain metadata will include the associated org and space. The Loggregator system must retrieve or generate a client certificate scoped to that org or space.
2. **Drain-level mTLS configuration**: The syslog adapter or HTTPS forwarder must use the org/space certificate when establishing mTLS connections to the remote drain endpoint.
3. **Centralized and automatic rotation support**: Certificates should be automatically renewed and reloaded with minimal or zero impact to traffic flow.
4. **Audit and visibility**: Logs and drain metadata must include the org/space identity used for certificate-based authentication.

### Example configuration

```bash
cf create-user-provided-service ORG-NAME -p '{"ca":"-----BEGIN CERTIFICATE-----\nMIIH...-----END CERTIFICATE-----"}'
```

or

```bash
cf create-user-provided-service SPACE-NAME -p '{"ca":"-----BEGIN CERTIFICATE-----\nMIIH...-----END CERTIFICATE-----", "cert":"-----BEGIN CERTIFICATE-----\nMIIH...-----END CERTIFICATE-----","key":"-----BEGIN PRIVATE KEY-----\nMIIE...-----END PRIVATE KEY-----"}'
```

### Configuration Flow

- When an app binds a syslog drain, the Cloud Controller should include org and space GUIDs in the drain metadata.
- The system retrieves a Certifacte Authority for that org or space from a binding.
- The drain connection must use this certificate for TLS/mTLS authentication.
