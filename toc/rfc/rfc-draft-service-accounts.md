# Meta
[meta]: #meta
- Name: Service Accounts for Cloud Foundry Workload Identity
- Start Date: 2026-10-06
- Author(s): @rkoster
- Status: Draft
- RFC Pull Request: [community#1645](https://github.com/cloudfoundry/community/pull/1645)
- Related RFCs: [RFC 0055: Identity-Aware Routing for GoRouter](rfc-0055-identity-aware-routing-for-gorouter.md)
- Affected Component(s): Cloud Controller, BBS, Diego, UAA, CF CLI, service brokers; later GoRouter

## Summary

Give applications a stable identity they can share, without distributing a shared
secret. Developers assign a **service account**. Cloud Foundry issues and rotates
each app instance's certificate, which the app uses to obtain short-lived JWTs
from UAA. External services can trust those JWTs directly or exchange them for
their own credentials.

The primary use case is **workload identity federation (WIF)** to off-platform
services, especially services managed by service brokers.

**One account, multiple apps, independent keys, explicit permissions.**

## Problem

A payments API stores uploaded invoices in a broker-managed cloud object store;
a background worker reads them for processing. Both need access to that external
service, without storing a long-lived access key in their service bindings.
The cloud provider supports WIF: exchange a JWT from a trusted issuer for
short-lived service credentials. The missing piece is a stable workload identity
that the provider can trust, without distributing another secret.

**Broker-managed services are a natural fit.** A broker already provisions the
service and its access. An identity-aware binding could configure trust and grants
for the app's service account, returning federation/connection metadata instead
of a long-lived password. Developers would retain the familiar service-binding UX.

Cloud Foundry already gives every instance its own certificate. However, instance
identities change on replacement, and app identities do not describe an intentional
group of apps. The team needs a durable **payments identity**, independent of which
instances or blue/green apps currently implement it.

**Next, coding agents running as CF apps** may need to push the applications they
generate. Explicit CAPI roles can give an agent that ability in a chosen space.
This is an emerging use case; off-platform federation is the primary motivation.

## Proposal

### 1. Create once, assign to apps

First, give the payments apps an identity that the object store's federation
provider can recognize across deployments. The account belongs to the targeted
space: each app can use one account, and multiple apps in that space can share
it. Cross-space assignment is excluded. Service access is granted in the next step.

```sh
cf target -o acme -s payments
cf push payments-api --no-start
cf push payments-jobs --no-start

cf create-service-account payments-worker
cf bind-service-account payments-api payments-worker
cf bind-service-account payments-jobs payments-worker

cf start payments-api
cf start payments-jobs
cf service-account payments-worker
```

```mermaid
flowchart LR
    CLI["Developer: create and bind"] --> CAPI["CAPI: account and assignments"]
    CAPI -->|"first bind: managed OAuth client"| UAA["UAA"]
    CAPI -->|"typed account identity"| Diego["BBS / Diego"]
    subgraph Space["Space: payments"]
        API["payments-api<br/>instance key A"]
        Jobs["payments-jobs<br/>instance key B"]
    end
    Diego -->|"issue certificate"| API
    Diego -->|"issue certificate"| Jobs
    API -.-> SAN["Shared DNS SAN:<br/>payments-worker.svc.identity"]
    Jobs -.-> SAN
```

First bind provisions one secretless UAA client and a roleless CAPI principal;
subsequent binds reuse them. The CLI waits for provisioning jobs, including retries.
No account certificate is issued before authorized provisioning is ready.

### 2. Bind a broker-managed service using federation

Binding an account answers **“Who am I?”**, not **“What may I do?”** For a service
whose broker supports identity federation, the proposed UX is:

```sh
# Proposed option; requires broker and client-library support
cf bind-service payments-api payments-store --authentication service-account
cf bind-service payments-jobs payments-store --authentication service-account
```

CAPI conveys the platform-owned account identity to the broker, which configures
the service's federation grants. Services may also be configured for federation
outside a broker.

#### OSBAPI impact

Propose a versioned service-plan capability, `service_account_binding`, and an
additive `bind_resource.service_account` object in the OSBAPI binding request.
These are **proposed extensions requiring OSBAPI agreement**, not existing fields.
An explicitly negotiated CF context extension can pilot the same semantics.

Illustrative request fragment supplied by CAPI, never by app binding parameters:

```json
{
  "bind_resource": {
    "app_guid": "<app-guid>",
    "service_account": {
      "version": "1.0",
      "id": "<account-guid>",
      "issuer": "https://uaa.example.org/oauth/token",
      "subject": "cf:service-account:payments-worker"
    }
  }
}
```

The broker accepts only configured issuer trust domains and returns non-secret
connection/federation metadata through the binding's `credentials` object:

```json
{
  "credentials": {
    "uri": "https://storage.example.org/payments",
    "authentication": {
      "type": "oauth2-bearer-jwt",
      "issuer": "https://uaa.example.org/oauth/token",
      "audience": "https://identity.example.org/federation/cf-payments"
    }
  }
}
```

CAPI approves and reconciles audience/scope targets before marking the binding
ready; libraries perform token acquisition and provider-specific exchange.
Unsupported brokers reject the requested mode; ordinary bindings stay unchanged.
Retries/async completion retain the binding's identity snapshot; failed setup or
cleanup remains visible and retryable. Grants and token targets are reference-counted
per binding so one unbind cannot remove another binding's access.

Account reassignment requires removing identity-based service bindings first.
All apps sharing an account share its grants. The OSBAPI originating-identity header
continues to identify the operation's caller, not the assigned workload account.

Creating accounts follows service-instance creation permissions: **Space Developer
or platform admin**, with readable/writable-space checks and operator controls.
Other lifecycle management initially requires space manager/admin; assignment
requires app-write permission. Ownership alone grants no account resource roles.

### 3. From app certificate to off-platform access

The app discovers its client ID and token endpoint through non-secret
`VCAP_SERVICE_ACCOUNT` metadata. Its library reads `CF_INSTANCE_CERT` and
`CF_INSTANCE_KEY`, reloading them when acquiring tokens after credential rotation.

```mermaid
sequenceDiagram
    participant App as payments-api
    participant UAA
    participant IdP as External federation provider
    participant Service as Broker-managed service
    App->>UAA: HTTPS POST /oauth/mtls/token + instance certificate
    Note over App,UAA: grant_type=client_credentials<br/>client_id=cf:service-account:payments-worker
    UAA->>UAA: Validate chain, key possession and exact account SAN
    UAA-->>App: Signed JWT for the approved federation audience
    App->>IdP: HTTPS token exchange with JWT
    IdP->>IdP: Verify issuer, signature, audience and subject grant
    IdP-->>App: Short-lived service credentials
    App->>Service: Request using exchanged credentials
    Service-->>App: Authorized data, or access denied
```

Illustrative **decoded UAA JWT** for an approved federation target (the provider's
required audience and exchange protocol must be configured and tested):

```json
{
  "iss": "https://uaa.example.org/oauth/token",
  "sub": "cf:service-account:payments-worker",
  "client_id": "cf:service-account:payments-worker",
  "aud": ["https://identity.example.org/federation/cf-payments"],
  "iat": 1791288000,
  "exp": 1791288300
}
```

Both apps have the same subject, but authenticate with different keys. The token
is limited to authorized audiences/scopes and expires within five minutes **and
no later than the certificate used to obtain it**. The external provider controls
the exchanged credentials' permissions and lifetime. Caller attribution should
also be retained in platform-controlled claims; claim names remain to be agreed.

There is deliberately **no `cnf`**: [RFC 8705][mtls] separates mTLS client
authentication from certificate-bound tokens. UAA must honor the client policy
`tls_client_certificate_bound_access_tokens: false`. The certificate is needed
to obtain the token, not to present it to the federation provider. Token issuance needs no live CAPI
assignment lookup; consumers validate issuer, signature, audience, expiry and
permissions independently.

### 4. Coding agents: the same identity, a CAPI target

An agent app can instead request a CAPI-targeted token. An authorized role manager
grants its account `SpaceDeveloper` in the space where generated apps may be pushed:

```sh
cf set-space-role cf:service-account:app-builder acme generated-apps SpaceDeveloper --client
```

```mermaid
sequenceDiagram
    participant Agent as Coding agent app
    participant UAA
    participant CAPI as Cloud Foundry API
    Agent->>UAA: mTLS token request for approved CAPI target
    UAA-->>Agent: JWT with aud cloud_controller and CAPI scopes
    Agent->>CAPI: Create and push generated app over HTTPS with bearer JWT
    CAPI->>CAPI: Validate token and explicit SpaceDeveloper role
    CAPI-->>Agent: Deployment result
```

This is a separate token target, not an all-purpose multi-audience token. CAPI
roles do not authorize external services, and federation grants confer no CAPI roles.

### 5. Authorize app-to-app routes with the same identity

Extend RFC 0055 route options with the source format
`cf:svc:<service-account-name>`, for example `cf:svc:payments-worker`.
The proposed CLI resolves the following to that route-option value:

```sh
cf add-route-policy apps.identity --hostname invoices --source-service-account payments-worker
```

```mermaid
flowchart LR
    API["payments-api"] -->|"mTLS certificate"| Router["GoRouter"]
    Jobs["payments-jobs"] -->|"mTLS certificate"| Router
    Policy["Allow: cf:svc:payments-worker"] -.-> Router
    Router -->|"verified account SAN + domain scope match"| Backend["invoices.apps.identity"]
    Other["Unbound app"] -->|"no account SAN: denied"| Router
```

Both payments apps can now call the invoices route. GoRouter verifies the caller's
certificate and checks for `payments-worker.svc.identity`; an app without that
identity does not qualify for this grant. No JWT or token exchange is needed.

Existing route policies keep working. An account grant does not bypass a domain's
org/space restriction: the **calling app** must still be in the allowed org or
space. Without a matching grant, access remains denied.

CAPI records which account the policy refers to and sends the rule to GoRouter.
The rule can be enabled only after all routers support it. If TLS terminates at a
proxy, the router must receive trustworthy certificate data including the account
SAN; a caller-provided identity header is not proof of identity.

**Disabling a service account stops new UAA tokens, not route access.** Route access
uses the certificate directly, so an already-issued certificate may still work
until expiry. Remove the route grant to withdraw that permission, and remove
account route grants before deleting the account.

### 6. Manage the account's lifecycle

| Intent | Command | Effect |
| --- | --- | --- |
| Inspect | `cf service-accounts` | List accounts in the targeted space |
| Remove assignment | `cf unbind-service-account payments-api` | Changes desired identity; restart the app to apply |
| Stop new tokens | `cf disable-service-account payments-worker` | Disables issuance for all apps sharing it |
| Resume | `cf enable-service-account payments-worker` | Re-enables issuance, retaining roles |
| Delete | `cf delete-service-account payments-worker` | Requires workload references removed; retains a name tombstone |
| Recover a deleted name | `cf create-service-account payments-worker --reuse-name` | Explicit, audited platform-admin override |

Running instances retain their launch identity—including renewal—until restart;
new tasks use the desired assignment. Staging never receives the account identity.
Unbind before assigning a different account. Zero-app accounts retain their client
and roles until explicitly disabled/deleted.

**Unbind, restart and disable do not revoke existing tokens or certificates.**
Copied credentials can remain usable until expiry while the client is enabled;
without restart, a running old assignment can keep renewing.

Names are immutable, foundation-unique lowercase DNS labels (3–63 characters).
The SAN suffix creates no DNS record or route; external identity is the trusted
`(issuer, subject)` pair. Admin `--reuse-name` creates a new UUID without restoring
bindings/roles, preserves audit history and cannot bypass live-name conflicts or
quotas. Its warning explains that external grants and valid old certificates may
still apply to the reused identity.

### 7. Extend space quotas

Add a maximum account count to space quotas, with this proposed V3 fragment:

```json
{
  "service_accounts": {
    "total_service_accounts": 10
  }
}
```

Count existing accounts, including disabled/unprovisioned ones, not bindings or
tombstones. Creation checks the limit atomically; deletion frees capacity. Lowering
the limit blocks further creation rather than deleting accounts. Default/unlimited
behavior follows existing space-quota conventions.

### Delivery

Start with CAPI account APIs/roles, native CLI, typed BBS/Diego identity and UAA
bearer issuance. Preserve existing instance fields, C2C route SANs and independent
keys. Protect the SAN namespace and managed client prefix from injection/takeover;
provision clients only in UAA's default zone. Unsupported identity features must
fail closed, with operator enablement only after compatible rollout.

Build on that foundation with curated external token targets, provider-specific
WIF tests and negotiated broker/driver integration: these deliver the primary
user-facing goal. CAPI access is the initial validation path, not proof of WIF
compatibility. Deliver account-aware route policies as a separate integration;
existing OSB bindings and route source types remain supported.

**Progress:** [CAPI][capi], [release wiring][release], [BBS][bbs], [Diego][diego] and
[CLI][cli] drafts demonstrate the two-app flow, explicit roles, disable/enable and
unbind/restart against CAPI; external federation, broker and account-route integration are not
yet demonstrated. Remaining work includes creation permissions, quotas/name reuse,
[UAA][uaa] bearer policy (the POC still emits `cnf`), leaf-expiry caps, namespace
protection, caller claims, module publication and rollout capability signaling.
Further renewal/staging/Windows/negative coverage is needed; lab CAPI HTTP access
must become HTTPS. Implementation details and test evidence live in those PRs.

[mtls]: https://www.rfc-editor.org/rfc/rfc8705.html#section-3.4
[capi]: https://github.com/cloudfoundry/cloud_controller_ng/pull/5520
[release]: https://github.com/cloudfoundry/capi-release/pull/702
[bbs]: https://github.com/cloudfoundry/bbs/pull/168
[diego]: https://github.com/cloudfoundry/diego-release/pull/1216
[cli]: https://github.com/cloudfoundry/cli/pull/3875
[uaa]: https://github.com/cloudfoundry/uaa/pull/4076
