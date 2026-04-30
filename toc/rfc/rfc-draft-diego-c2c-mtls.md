# Meta
[meta]: #meta
- Name: Full mTLS for Diego Container-to-Container Traffic
- Start Date: 2026-02-13
- Author(s): @rkoster
- Status: Draft
- RFC Pull Request: [community#1437](https://github.com/cloudfoundry/community/pull/1437)


## Summary

This RFC proposes implementing full mutual TLS (mTLS) for container-to-container (C2C) traffic in Diego, enabling applications to both authenticate themselves and verify the identity of connecting applications.

The approach introduces a **new HTTP-based listener on port 62443** that runs alongside the existing TCP-based C2C port (61443), providing a dual opt-in model for both operators and application authors. This enables zero-trust networking where all app-to-app traffic can be authenticated and authorization decisions can be made based on app/space/org identity.


## Problem

Cloud Foundry's Diego runtime currently runs Envoy as a per-container sidecar for handling **inbound traffic only**. While this provides TLS termination and route integrity, several limitations prevent true zero-trust app-to-app communication:

### No Client-Side (Egress) Proxy

Envoy is not configured as an egress proxy. Applications cannot automatically inject their instance identity certificate when making outbound connections. The current workaround requires applications to manually use `CF_INSTANCE_CERT` and `CF_INSTANCE_KEY` environment variables to present their identity.

### No Identity Extraction on Server Side

Even when mTLS is enabled, the receiving application has no way to know who connected. Envoy does not forward client certificate information via headers (no XFCC header configuration).

### C2C Port (61443) is TCP-Based

The C2C listener (port 61443) is a TCP proxy, not an HTTP proxy. This means:
- No HTTP connection manager
- No XFCC header support
- No mTLS client certificate validation
- No HTTP/2 support

### Existing mTLS Only Affects Route Integrity

The existing BOSH property `containers.proxy.require_and_verify_client_certificates` only affects route integrity ports (Gorouter → App), not C2C traffic.

### Current Architecture

```mermaid
flowchart LR
    subgraph Container
        Envoy["Envoy<br/>(port 61001)"]
        App["App<br/>(port 8080)"]
        Envoy -->|plain TCP| App
    end
    Gorouter -->|TLS| Envoy
    
    Note["Envoy only handles INBOUND traffic<br/>(DownstreamTlsContext)"]
```

### Current Certificate Setup

Diego generates two separate certificates per container in the [credmanager](https://github.com/cloudfoundry/executor/blob/main/depot/containerstore/credmanager.go):

| Certificate | SAN Contents | Purpose | mTLS Support | HTTP/2 |
|------------|--------------|---------|--------------|--------|
| Instance Identity | Container IP address | Route integrity (Gorouter → App) | Yes (optional) | Yes |
| C2C Certificate | Internal route hostnames (e.g., `app.apps.internal`) | Container-to-container TLS | No | No |

Both certificates include app identity in the certificate's `Subject.OrganizationalUnit` field (separate from the SAN). These claims are set by Cloud Controller and passed through the [BBS CertificateProperties](https://github.com/cloudfoundry/bbs/blob/main/models/certificate_properties.pb.go) model:

- `app:<app-guid>`
- `space:<space-guid>`
- `organization:<org-guid>`


## Proposal

### Design Principles

1. **Backwards compatibility**: Keep port 61443 unchanged for existing applications
2. **Dual opt-in**: Both operator and application author must opt-in
3. **New port for new behavior**: Port 62443 for HTTP-based mTLS with XFCC header support

### Port Allocation

| Port | Type | Purpose | mTLS | XFCC | Status |
|------|------|---------|------|------|--------|
| 61001+ | HTTP | Route integrity | Optional | No | Existing |
| 61443 | TCP | C2C TLS (TCP-based) | No | No | Existing (unchanged) |
| **62443** | **HTTP** | **C2C mTLS with identity** | **Required** | **Yes** | **New** |
| 61445 | HTTP | Egress proxy (client-side) | N/A | N/A | New |

### Implementation Phases

The implementation is divided into three phases to allow gradual adoption and testing.

---

### Phase 1: Server-Side - New HTTP-based C2C mTLS Port (62443)

Add a new Envoy listener on port 62443 that provides HTTP-based C2C with mTLS and XFCC header forwarding.

```mermaid
flowchart TB
    subgraph ContainerB["Container B (Server)"]
        subgraph Listeners
            L61443["Port 61443<br/>(TCP)"]
            L62443["Port 62443<br/>(HTTP, new)"]
        end
        AppB["App B<br/>(port 8080)"]
        
        L61443 -->|"TLS termination only<br/>No client cert validation<br/>No XFCC header"| AppB
        L62443 -->|"mTLS required<br/>XFCC header forwarded"| AppB
    end
    
    ClientA["Container A<br/>(Client)"] -->|"Option 1: TLS (TCP proxy)"| L61443
    ClientA -->|"Option 2: mTLS with identity"| L62443
```

#### Changes Required

**New Port Constant**: Add `C2CMTLSPort = 62443` alongside the existing `C2CTLSPort = 61443`.

**New HTTP-based Listener**: Create a new Envoy listener with:
- HTTP connection manager (not TCP proxy)
- `DownstreamTlsContext` with `RequireClientCertificate: true`
- Validation context trusting the instance identity CA
- XFCC header set from the verified client certificate, with any existing headers removed to prevent spoofing
- Subject, URI, and DNS fields included in the XFCC header

**BOSH Properties**:

```yaml
containers.proxy.enable_c2c_mtls_listener:
  description: "Enable the HTTP-based C2C mTLS listener on port 62443. This listener 
    requires client certificates and forwards caller identity via the X-Forwarded-Client-Cert header."
  default: false
```

**Port Reservation**: Add validation to prevent applications from using port 62443, similar to the existing reservation for port 61443.

#### Result

When an operator enables `containers.proxy.enable_c2c_mtls_listener`:
- Port 62443 becomes available on all containers
- Clients connecting to 62443 MUST present a valid instance identity certificate
- The receiving app gets an `X-Forwarded-Client-Cert` header with caller identity:

```
X-Forwarded-Client-Cert: Hash=abc123;Subject="CN=instance-guid,OU=app:client-app-guid,OU=space:space-guid"
```

---

### Phase 2: Client-Side Egress Proxy (Port 61445)

Enable Envoy to act as an HTTP proxy for outbound connections, automatically injecting the instance identity certificate.

```mermaid
flowchart LR
    subgraph ContainerA["Container A"]
        AppA["App A"]
        EgressProxy["Envoy Egress<br/>(port 61445)"]
        AppA -->|HTTP| EgressProxy
    end
    
    subgraph ContainerB["Container B"]
        IngressProxy["Envoy Ingress<br/>(port 62443)"]
    end
    
    EgressProxy -->|"mTLS<br/>(auto cert injection)"| IngressProxy
    
    Note["Certificate contains:<br/>OU=app:client-app-guid<br/>OU=space:space-guid"]
```

#### Changes Required

**Egress Proxy Port**: Reserve port 61445 for the egress proxy.

**Egress Listener**: Create a new Envoy listener that acts as an HTTP CONNECT proxy, bound to `127.0.0.1:61445` (localhost only). The proxy accepts all outbound traffic but only injects the instance identity certificate for connections to C2C mTLS backends.

**UpstreamTlsContext**: Configure the egress proxy to attach the instance identity certificate only when connecting to C2C mTLS backends, identified by destination port (62443) and hostname pattern matching the configured `internal_domains`.

**Environment Variable**: Inject a CF-specific environment variable for applications to discover the egress proxy:

```
CF_INSTANCE_MTLS_PROXY=http://127.0.0.1:61445
```

**Enforcing Proxy Usage**: Operators can make the egress proxy mandatory for all applications by setting `HTTP_PROXY` and `HTTPS_PROXY` to `http://127.0.0.1:61445` using [running environment variable groups](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#evgroups). This ensures all HTTP/HTTPS traffic from applications is routed through the egress proxy, with instance identity certificates injected only for C2C mTLS backends.

**BOSH Properties**:

```yaml
containers.proxy.enable_egress_proxy:
  description: "Enable Envoy egress proxy for outbound mTLS on port 61445"
  default: false

containers.proxy.internal_domains:
  description: "Domains for C2C mTLS backends where the instance identity certificate should be injected."
  example: ["apps.internal.", "my.apps.internal."]
  default: []
```

This follows the same naming and format as the [`internal_domains` property in `bosh-dns-adapter`](https://github.com/cloudfoundry/cf-networking-release/blob/develop/jobs/bosh-dns-adapter/spec).

#### Considerations

- **SNI Handling**: Envoy needs to extract the target hostname for proper TLS handshake
- **NO_PROXY**: Applications should configure `NO_PROXY` for traffic that should not go through the proxy
- **Non-HTTP Traffic**: The HTTP CONNECT-based egress proxy only supports HTTP/HTTPS traffic. Support for TCP-based protocols could be addressed in a follow-up RFC.
- **Performance**: Additional hop adds latency
- **Memory**: Additional memory allocation may be needed for the egress proxy

---

### Phase 3: Full Integration

With both phases implemented, the complete mTLS flow enables zero-trust app-to-app communication:

```mermaid
sequenceDiagram
    participant AppA as App A
    participant EgressA as Envoy Egress<br/>(Container A:61445)
    participant IngressB as Envoy Ingress<br/>(Container B:62443)
    participant AppB as App B

    AppA->>EgressA: HTTP request
    Note over EgressA: Attaches instance cert<br/>OU=app:aaa-guid<br/>OU=space:xxx
    EgressA->>IngressB: mTLS connection
    Note over IngressB: Validates client cert<br/>against instance identity CA
    IngressB->>AppB: HTTP request +<br/>X-Forwarded-Client-Cert header
    Note over AppB: Reads XFCC header<br/>to authorize request
    AppB-->>IngressB: HTTP response
    IngressB-->>EgressA: Response
    EgressA-->>AppA: Response
```

#### Opt-in Model

| Actor | How to Opt-in |
|-------|---------------|
| **Operator** | Set `containers.proxy.enable_c2c_mtls_listener: true` and `containers.proxy.enable_egress_proxy: true` |
| **Server App** | Listen for connections and read `X-Forwarded-Client-Cert` header |
| **Client App** | Connect to port 62443 (directly or via egress proxy at 61445) |

#### App-Level Authorization

Applications can parse the XFCC header to make authorization decisions based on the caller's app GUID, space GUID, or organization GUID embedded in the certificate's OrganizationalUnit field.

---

### Benefits

- Backwards compatible: port 61443 stays as-is, existing apps keep working
- Opt-in for both operators (BOSH properties) and app authors (connect to 62443)
- Apps can migrate gradually, no big-bang required
- Server apps can verify who's calling and authorize based on app/space/org
- No more manual certificate handling for C2C calls

---

## Key Repositories

The following repositories require modifications to implement this proposal:

| Repository | Purpose |
|------------|---------|
| [cloudfoundry/executor](https://github.com/cloudfoundry/executor) | Envoy config generation, environment variable injection |
| [cloudfoundry/diego-release](https://github.com/cloudfoundry/diego-release) | BOSH property definitions |

## References

- [Envoy XFCC Header Documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_conn_man/headers#x-forwarded-client-cert)
- [Envoy Dynamic Forward Proxy](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/dynamic_forward_proxy_filter)
- [Diego Envoy Proxy Configuration](https://github.com/cloudfoundry/diego-release/blob/develop/docs/060-envoy-proxy-configuration.md)
