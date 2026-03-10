# Meta
[meta]: #meta
- Name: Domain-Scoped mTLS for GoRouter
- Start Date: 2026-02-16
- Author(s): @rkoster, @beyhan, @maxmoehl
- Status: Draft
- RFC Pull Request: [community#1438](https://github.com/cloudfoundry/community/pull/1438)


## Summary

Enable per-domain mutual TLS (mTLS) on GoRouter with optional identity extraction and authorization enforcement. Operators configure domains that require client certificates, specify how to handle the XFCC header, and optionally enable platform-enforced access control.

This infrastructure supports multiple use cases: authenticated CF app-to-app communication via internal domains (e.g., `apps.mtls.internal`), external client certificate validation for partner integrations, and cross-CF federation between installations.

For CF app-to-app routing, this follows the same default-deny model as container-to-container network policies: all traffic is blocked unless explicitly allowed.


## Problem

Cloud Foundry applications can communicate via external routes (through GoRouter) or container-to-container networking (direct). Neither provides per-domain mTLS requirements with platform-enforced authorization:

- **External routes**: Traffic leaves the VPC to reach the load balancer, adding latency and cost. GoRouter's client certificate settings are global—enabling strict mTLS for one domain affects all domains.
- **C2C networking**: Requires [`network.write` scope](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#grant-permissions), which is not granted to space developers by default—operators must set [`enable_space_developer_self_service: true`](https://github.com/cloudfoundry/cf-networking-release/blob/develop/jobs/policy-server/spec). Also lacks load balancing, observability, and identity forwarding.

This RFC addresses several use cases that require per-domain mTLS:

1. **CF app-to-app routing**: Applications need authenticated internal communication where only CF apps can connect (via instance identity), traffic stays internal, the platform enforces which apps can call which routes, and standard GoRouter features work (load balancing, retries, observability).

2. **External client certificates**: Some platforms need to validate client certificates from external systems (partner integrations, IoT devices) on specific domains without affecting other domains or requiring CF-specific identity handling.

3. **Cross-CF federation**: Applications on one CF installation need to securely communicate with applications on another CF installation, each with its own CA and GUID namespace.

**The gap**: GoRouter has no mechanism for requiring mTLS on specific domains while leaving others unaffected, and no way to enforce authorization rules at the route level based on caller identity.

For CF app-to-app routing specifically, authentication alone is insufficient. Without authorization enforcement, any authenticated app could access any route on the mTLS domain, defeating the purpose of platform-enforced security.


## Proposal

GoRouter gains the ability to require client certificates for specific domains, with configurable identity extraction and authorization enforcement. This is implemented in phases:

- **Phase 1a (mTLS Domain Infrastructure)**: GoRouter requires and validates client certificates for configured domains. The XFCC header is set with certificate details. This alone enables external client certificate validation.
- **Phase 1b (CF Identity & Authorization)**: Optional, opt-in behavior where GoRouter extracts CF identity from Diego instance certificates and enforces authorization rules. This enables CF app-to-app routing and cross-CF federation.
- **Phase 2 (Egress HTTP Proxy)**: Optional enhancement where the sidecar proxy automatically injects instance identity certificates, simplifying client adoption for CF app-to-app routing.

### Architecture Overview

The diagram below shows CF app-to-app routing (the most complex use case). For external client certificate validation, only GoRouter and the backend app are involved—external clients connect directly to GoRouter with their certificates.

```mermaid
flowchart LR
    subgraph "App A Container"
        AppA["App A"]
        ProxyA["Envoy<br/>(egress proxy)"]
    end
    
    subgraph "GoRouter"
        GR["1. Validate cert<br/>(Instance Identity CA)"]
        Auth["2. Check authorization"]
    end
    
    subgraph "App B Container"
        ProxyB["Envoy<br/>(validates GoRouter cert)"]
        AppB["App B"]
    end
    
    AppA -->|"HTTP"| ProxyA
    ProxyA -->|"mTLS<br/>(instance cert)"| GR
    GR --> Auth
    Auth -->|"authorized<br/>mTLS<br/>(GoRouter cert)"| ProxyB
    Auth -.->|"403 Forbidden"| ProxyA
    ProxyB -->|"HTTP + XFCC"| AppB
```

### Phase 1a: mTLS Domain Infrastructure

GoRouter gains the ability to require client certificates for specific domains while leaving other domains unaffected. This infrastructure is generic and can be used for multiple purposes beyond CF app-to-app routing.

**How it works:**
1. Operator configures a domain with mTLS requirements in the `mtls_domains` configuration
2. DNS (BOSH DNS or external) resolves the domain to GoRouter instances
3. Applications map routes to this domain like any shared domain
4. When a client connects, GoRouter:
   - Requires a client certificate
   - Validates it against the configured CA
   - Sets the XFCC header with certificate details (format configurable)
   - Optionally extracts identity and enforces authorization (Phase 1b)

**Configuration:**

```yaml
router:
  mtls_domains:
    # Domain pattern requiring mTLS. Wildcards supported.
    - domain: "*.apps.mtls.internal"
      
      # CA certificate(s) for validating client certs (PEM-encoded)
      ca_certs: ((diego_instance_identity_ca.certificate))
      
      # How to handle the X-Forwarded-Client-Cert header:
      #   sanitize_set (default, recommended) - Remove incoming XFCC, set from client cert
      #   forward - Pass through existing XFCC header
      #   always_forward - Always pass through, even if no client cert
      forwarded_client_cert: sanitize_set
      
      xfcc:
        # Format of the XFCC header:
        #   raw (default) - Full base64-encoded certificate (~1.5KB)
        #   envoy - Compact format (~300 bytes):
        #           Hash=<sha256>;Subject="CN=<instance-id>,OU=app:<guid>..."
        format: envoy
        
        # How to extract caller identity from the certificate:
        #   none (default) - No extraction; backend parses XFCC itself
        #   cf_ou - Extract app/space/org GUIDs from Diego instance identity
        #           certificate OU fields (app:<guid>, space:<guid>, organization:<guid>)
        identity_extractor: cf_ou
      
      authorization:
        # How to enforce access control:
        #   none (default) - Any valid certificate accepted
        #   cf_identity - Enforce rules using CF identity hierarchy
        #                 (requires identity_extractor: cf_ou)
        mode: cf_identity
        
        # Operator-level access policy (only for mode: cf_identity)
        # Use EITHER scope OR orgs/spaces (mutually exclusive)
        config:
          # Relative boundary - caller must be in same space/org as target:
          #   any (default) - No restriction at domain level
          #   org - Caller must be in same org as target app
          #   space - Caller must be in same space as target app
          scope: org
          
          # Absolute boundary - explicit list of allowed orgs/spaces:
          orgs: ["org-guid-1", "org-guid-2"]
          spaces: ["space-guid-1", "space-guid-2"]
```

**Validation rules:**
- `authorization.config.scope` is mutually exclusive with `authorization.config.orgs`/`authorization.config.spaces`
- If `authorization.config` is omitted, defaults to `authorization.config.scope: any`
- `authorization.mode: cf_identity` requires `xfcc.identity_extractor: cf_ou`
- Invalid combinations are rejected during BOSH deployment by the GoRouter job templates

### Phase 1b: CF Identity & Authorization

When `xfcc.identity_extractor: cf_ou` and `authorization.mode: cf_identity` are enabled, GoRouter enforces access control at the routing layer using a default-deny model, matching the design of container-to-container network policies.

Authorization is enforced at two layers:

1. **Domain level (operator)**: Configured via `authorization.config` in `mtls_domains`
2. **Route level (developer)**: Configured via `allowed_sources` in route options

**Layered authorization:**

```mermaid
flowchart LR
    A[Request on mTLS domain] --> B["1. Domain authorization (operator)"]
    B --> C["2. Route authorization (developer)"]
    C --> D[Request forwarded with XFCC header]
```

Developers can only **restrict further** within operator boundaries. They cannot expand access beyond operator-defined limits.

**Route options** (RFC-0027 compliant flat format):

```yaml
applications:
# Platform-enforced authorization with explicit allowlist
- name: backend-api
  routes:
  - route: backend.apps.mtls.internal
    options:
      # Comma-separated app GUIDs allowed to call this route
      mtls_allowed_apps: "frontend-app-guid,monitoring-app-guid"
      # Comma-separated space GUIDs whose apps can call this route
      mtls_allowed_spaces: "trusted-space-guid"
      # Comma-separated org GUIDs whose apps can call this route
      mtls_allowed_orgs: "partner-org-guid"

# App-delegated authorization: any authenticated app allowed within operator scope
# Useful when authorization depends on dynamic information (e.g., service bindings)
- name: autoscaler-api
  routes:
  - route: autoscaler.apps.mtls.internal
    options:
      # When true, any request passing operator-level authorization is allowed
      # The app receives XFCC header for additional authorization checks
      mtls_allow_any: true
```

**Validation rules:**
- `mtls_allow_any: true` is mutually exclusive with `mtls_allowed_apps`, `mtls_allowed_spaces`, and `mtls_allowed_orgs`
- All `mtls_allowed_*` values are comma-separated strings of GUIDs
- Cloud Controller validates GUID format (not existence, to support federation)

**Warning behavior:**

When a route specifies `mtls_allowed_*` options but the domain has `authorization.mode: none`, GoRouter logs a warning to the application's log stream:

```
[WARN] Route 'backend.partner.example.com' specifies mtls_allowed_apps but domain has authorization.mode=none; rules are not enforced.
```

This builds on the route options framework from [RFC-0027: Generic Per-Route Features](rfc-0027-generic-per-route-features.md). Phase 1b depends on RFC-0027 being implemented first.

### Phase 2: Egress HTTP Proxy (Optional)

To simplify client adoption, add an HTTP proxy to the application sidecar that automatically handles mTLS.

**How it works:**
1. Diego configures an egress proxy (Envoy) listening on `127.0.0.1:8888`
2. The proxy is configured to intercept requests to `*.apps.mtls.internal`
3. For matching requests, the proxy:
   - Upgrades the connection to TLS
   - Presents the application's instance identity certificate
   - Forwards the request to GoRouter

**Application usage:**
```bash
# Client app sets HTTP_PROXY for the internal domain
export HTTP_PROXY=http://127.0.0.1:8888
export NO_PROXY=external-api.example.com

# Plain HTTP request, proxy handles mTLS automatically
curl http://myservice.apps.mtls.internal/api
```

This eliminates the need for applications to load certificates and configure TLS clients.

### Extensibility

The `xfcc.identity_extractor` and `authorization.mode` fields are designed to support additional modes in the future without breaking the configuration schema:

| Identity Extractor | Authorization Mode | Use Case |
|-------------------|-------------------|----------|
| `none` | `none` | External client certs, app-level authorization |
| `cf_ou` | `cf_identity` | CF app-to-app with platform-enforced rules |
| `cf_ou` | `cf_identity` | Cross-CF federation (via per-installation domains) |
| `subject_cn` (future) | `cn_allowlist` (future) | Generic CN-based authorization |
| `spiffe` (future) | `spiffe_authz` (future) | SPIFFE identity federation |

Each `authorization.mode` can define its own `authorization.config` schema, allowing future modes to have different policy options without affecting existing configurations.

This allows operators to use `mtls_domains` for external client certificate validation without CF-specific coupling, while preserving the option to add new identity extraction and authorization modes as needs evolve.


## Release Criteria

**For CF app-to-app routing use case:**

Phase 1a and Phase 1b (with `xfcc.identity_extractor: cf_ou` and `authorization.mode: cf_identity`) are co-requisites and must be released together.

Deploying Phase 1a without enabling CF identity authorization would leave all mTLS routes accessible to any authenticated app, violating the default-deny security model. Operators enabling CF app-to-app routing must configure appropriate `authorization.config` settings.

Phase 1b depends on [RFC-0027: Generic Per-Route Features](rfc-0027-generic-per-route-features.md) being implemented first.

**For external client validation use case:**

Phase 1a alone (with `authorization.mode: none`) is sufficient. Backend applications handle authorization based on the XFCC header.


## Appendix

### Relationship to Container-to-Container Networking

This RFC complements Cloud Foundry's existing [container-to-container (C2C) networking](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html) rather than replacing it. The two mechanisms serve different purposes and operate at different layers.

**Why extend GoRouter instead of C2C networking?**

This RFC reuses existing GoRouter infrastructure—TLS termination, request routing, load balancing, access logging, and the route options framework from [RFC-0027](rfc-0027-generic-per-route-features.md). By enforcing authorization at the HTTP layer, applications gain access to caller identity via the XFCC header, enabling fine-grained authorization decisions. GoRouter already handles millions of requests; adding per-domain mTLS builds on proven infrastructure.

C2C networking operates at Layer 4 (TCP/UDP) using IPtables rules enforced on Diego Cells via [VXLAN policy agents](https://github.com/cloudfoundry/silk-release). This architecture has [scaling considerations for large deployments](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/09-large-deployments.md): policies are limited by VXLAN's 16-bit marks (~65,535 apps can participate in policies), and each policy requires IPtables rules on every Diego Cell. For HTTP traffic requiring caller identity, load balancing, and observability, GoRouter-based routing is a better fit.

**When to use which:**

- **C2C networking**: Non-HTTP protocols (databases, message queues, gRPC over TCP), low-latency direct connections, when traffic should bypass GoRouter entirely.
- **mTLS app routing (this RFC)**: HTTP APIs requiring caller identity in the request, platform-enforced authorization at the route level, when you need GoRouter features (load balancing, retries, observability, access logs).

The two mechanisms can coexist. An application might use C2C networking for database connections while exposing HTTP APIs via mTLS app routing.

### Configuration Examples

**CF app-to-app routing with different scope restrictions:**
```yaml
router:
  mtls_domains:
    - domain: "*.apps.mtls.internal"
      ca_certs: ((diego_instance_identity_ca.certificate))
      forwarded_client_cert: sanitize_set
      xfcc:
        format: envoy
        identity_extractor: cf_ou
      authorization:
        mode: cf_identity
        config:
          # Choose ONE of the following scope options:
          scope: org    # Apps can only call other apps in the same org
          # scope: space  # Apps can only call other apps in the same space
          # scope: any    # Any app can call, subject to route-level mtls_allowed_*
```

**External client certificate validation (app-level authorization):**
```yaml
router:
  mtls_domains:
    - domain: "*.partner.example.com"
      ca_certs: ((partner_ca.certificate))
      forwarded_client_cert: sanitize_set
      xfcc:
        format: envoy
        # identity_extractor: none (default)
      authorization:
        mode: none
        # No config needed for mode: none
```

In this configuration, GoRouter validates that the client certificate is signed by the partner CA, then forwards the XFCC header to the backend application. The application parses the XFCC header and performs its own authorization based on the certificate's Subject, SANs, or other fields.

**Cross-CF federation (apps calling across CF installations):**

When multiple CF installations need to communicate, configure a separate mTLS domain per remote CF installation. This scopes GUIDs to their originating installation and trusts only that installation's CA:

```yaml
router:
  mtls_domains:
    # Local CF app-to-app
    - domain: "*.apps.mtls.internal"
      ca_certs: ((diego_instance_identity_ca.certificate))
      forwarded_client_cert: sanitize_set
      xfcc:
        format: envoy
        identity_extractor: cf_ou
      authorization:
        mode: cf_identity
        config:
          scope: org

    # Trust apps from CF-East installation
    - domain: "*.apps.mtls.cf-east.internal"
      ca_certs: ((cf_east_diego_ca.certificate))
      forwarded_client_cert: sanitize_set
      xfcc:
        format: envoy
        identity_extractor: cf_ou
      authorization:
        mode: cf_identity
        config:
          orgs: ["trusted-east-org-guid"]  # Only this org from CF-East can call

    # Trust apps from CF-West installation
    - domain: "*.apps.mtls.cf-west.internal"
      ca_certs: ((cf_west_diego_ca.certificate))
      forwarded_client_cert: sanitize_set
      xfcc:
        format: envoy
        identity_extractor: cf_ou
      authorization:
        mode: cf_identity
        config:
          scope: any  # Any CF-West app can call (route-level mtls_allowed_* applies)
```

Route configuration specifies allowed apps per originating installation:

```yaml
applications:
- name: backend-api
  routes:
  # Local clients (must be same org due to domain scope)
  - route: backend.apps.mtls.internal
    options:
      mtls_allowed_apps: "local-frontend-guid"
  # Clients from CF-East (must be in trusted-east-org-guid due to domain config)
  - route: backend.apps.mtls.cf-east.internal
    options:
      mtls_allowed_apps: "east-frontend-guid"
```

The domain naming convention `*.apps.mtls.<cf-installation>.internal` ensures:
- No conflict with existing app routes (CF identifier is at the parent domain level)
- GUIDs are scoped to their originating installation
- Each installation's CA is trusted independently
- Standard `cf_ou` identity extraction and `cf_identity` authorization work unchanged

### References

| Component | Reference |
|-----------|-----------|
| GoRouter TLS config | [`routing-release/.../config.go`](https://github.com/cloudfoundry/routing-release/blob/develop/src/code.cloudfoundry.org/gorouter/config/config.go) |
| GoRouter BOSH spec | [`routing-release/jobs/gorouter/spec`](https://github.com/cloudfoundry/routing-release/blob/develop/jobs/gorouter/spec) |
| RFC-0027 route options | [`toc/rfc/rfc-0027-generic-per-route-features.md`](rfc-0027-generic-per-route-features.md) |
| Cloud Controller routes | [`cloud_controller_ng/.../route.rb`](https://github.com/cloudfoundry/cloud_controller_ng/blob/main/app/models/runtime/route.rb) |
| Container-to-Container Networking | [CF Docs](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html) |
| Diego Instance Identity | [`diego-release/docs/050-app-instance-identity.md`](https://github.com/cloudfoundry/diego-release/blob/develop/docs/050-app-instance-identity.md) |
