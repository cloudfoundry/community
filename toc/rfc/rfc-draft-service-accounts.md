# Meta
[meta]: #meta
- Name: Service Accounts for Cloud Foundry Workload Identity
- Start Date: 2026-10-06
- Author(s): @rkoster
- Status: Draft
- RFC Pull Request: [community#1645](https://github.com/cloudfoundry/community/pull/1645)
- Related RFCs: [RFC 0055: Identity-Aware Routing for GoRouter](rfc-0055-identity-aware-routing-for-gorouter.md)
- Affected Component(s): Cloud Controller, BBS, Diego, UAA, CF CLI; subsequently GoRouter and service brokers

## Summary

Introduce space-owned service accounts: stable identities that selected apps share
without sharing a private key or distributing client secrets. Cloud Controller
manages the account and its OAuth client; Diego adds its identity to each app's
instance certificate. Apps authenticate to UAA with that certificate and obtain
short-lived bearer JWTs for explicitly authorized resources.

```sh
cf create-service-account payments-worker
cf bind-service-account payments-api payments-worker
cf bind-service-account payments-jobs payments-worker
```

Implementation drafts provide a tested starting point, not a prerequisite for
accepting their exact API or configuration details.

## Problem

Instance GUIDs and app GUIDs identify individual workloads, but are unsuitable as
a durable identity shared across an API, background workers, replacements and
blue/green deployments. Applications commonly compensate with stored client
secrets or externally managed credentials.

Cloud Foundry already issues per-instance certificates and authorizes OAuth client
principals. Connecting these mechanisms through an explicit account lifecycle
provides stable workload identity while preserving instance-level attribution.

## Proposal

### Identity and authorization boundary

- An account has an immutable UUID, name and owning space. Names are
  foundation-unique, lowercase DNS labels of 3–63 characters. Deletion retains a
  name tombstone; ordinary creation cannot reuse it. Only a platform admin may
  explicitly override that reservation as described below.
- Each app has zero or one account; multiple apps in the owning space may share
  it. Cross-space assignment is excluded, including within the same organization.
- Account creation follows service-instance creation permissions: Space Developers
  and platform admins may create accounts, subject to readable/writable-space
  checks and operator controls. Space Manager alone does not confer creation rights.
  Other account lifecycle operations initially require space managers/platform
  admins; assignment requires app-write permission in the writable owning space.
- Creating or binding an account grants no resource permissions. CAPI roles,
  route rules and broker privileges are explicit and shared by all apps using it.
  Anyone able to deploy code to those apps can exercise those permissions.

| Identity | Example |
| --- | --- |
| Name | `payments-worker` |
| OAuth client ID / JWT subject | `cf:service-account:payments-worker` |
| Certificate DNS SAN | `payments-worker.svc.identity` |
| External identity | Trusted `(issuer, subject)` pair |

The SAN suffix is identity-only: it creates no route or DNS record and is never
resolved to authenticate a caller. Separate foundations may reuse names; their
issuers and CA trust domains must remain distinct.

### Control plane and developer experience

Creation reserves the account. First authorized bind asynchronously provisions
one UAA client and roleless CAPI OAuth principal; further binds reuse them. Jobs
must survive retries/concurrency without adopting an unmanaged client-ID collision
or issuing credentials before provisioning is ready.

CAPI exposes `/v3/service_accounts`, account app listing, and the app's
`/relationships/service_account` relationship. Resource relationships use UUIDs;
names are human-facing lookup keys. The CLI provides create/list/show/delete,
bind/unbind and enable/disable commands, waits for jobs, and reports identity,
provisioning state and restart guidance. Existing `/v3/roles` semantics and org
membership prerequisites apply to the managed principal.

For recovery from accidental deletion, propose
`cf create-service-account NAME --reuse-name`. CAPI must authorize this explicit
tombstone override server-side for platform admins only and atomically prevent
conflicts with live accounts or concurrent creation. It creates a new account UUID
in the selected space, without restoring deleted bindings or CAPI roles; normal
creation checks and quotas still apply. Audit records retain the reservation's
history and identify the admin and replacement account.

The CLI must warn that reuse restores the same SAN and `(issuer, subject)`:
external grants may authorize the replacement, and still-valid old certificates
may authenticate once its client is provisioned. This is an intentional admin
escape hatch, not revocation or isolation from the former identity.

Accounts with no assigned apps retain their identity and roles until explicitly
disabled or deleted. Deletion requires removal of active workload references;
future route/broker references must also be resolved before teardown. Audit events
cover account creation, grants and assignment changes.

Extend space quotas with a **maximum number of service accounts** (proposed V3
field: `service_accounts.total_service_accounts`). Count every existing account
owned by the space, including disabled and unprovisioned accounts; app bindings
do not consume additional quota. Enforce the limit atomically during creation so
concurrent requests cannot exceed it. Deletion frees quota capacity, but its name
tombstone remains and does not count toward this resource limit. Lowering a quota
below current usage blocks further creation without deleting existing accounts.
Defaults and unlimited behavior should follow existing space-quota conventions.

### Credentials and token profile

CAPI supplies a platform-owned account name through typed BBS certificate
properties. Diego derives exactly one account SAN in instance and C2C credentials,
preserving existing GUID/CN/IP, app/space/org OUs, route SANs and certificate renewal.
Every instance keeps its own key. Runtime tasks inherit their launch assignment;
staging receives no account identity. Other SAN-producing inputs cannot inject the
reserved suffix; malformed or ambiguous account identities fail closed.

UAA uses [RFC 8705 PKI client authentication][mtls] with a validated chain and
exactly one registered DNS SAN binding. Managed clients are secretless,
`client_credentials`-only, provisioned in the default UAA zone. Operators must
protect `cf:service-account:` across client-management paths and zones; ordinary
client administrators cannot create, alter or take over managed registrations.

Mutual-TLS client authentication is independent of certificate-bound access
tokens. Set [`tls_client_certificate_bound_access_tokens: false`][binding] on the
managed client: tokens are bearer JWTs **without `cnf`**, usable without presenting
the instance certificate to CAPI. Require trusted issuer, stable account subject,
authorized audience/scopes and expiry no later than five minutes or the issuing
leaf certificate's expiry. Platform-controlled caller claims should retain
app/space/org/instance attribution and must not be overridden by app templates.

Non-secret `VCAP_SERVICE_ACCOUNT` metadata supplies the client ID and token
endpoint. Libraries reread rotated instance credential files when acquiring
tokens. UAA authenticates against its managed registration without a live CAPI
assignment lookup. Resource servers independently validate tokens and permissions.
The first delivery uses a fixed CAPI audience; additional targets require explicit
audience/scope policy rather than universal multi-audience tokens.

### Lifecycle and rollout

Bind/unbind changes desired configuration; running containers retain their
launch-time identity, including renewal, until replaced. **Restart is required**;
restaging solely for identity changes is unnecessary. New tasks use the desired
assignment. Unbind must precede assigning a different account.

Restart does not revoke copied credentials. While the shared client is enabled,
an old certificate/key can obtain tokens until certificate expiry; each token is
also capped by that expiry. Without restart, an old running assignment can keep
renewing. Account disable stops new tokens when effective, not existing JWTs or
certificate-only access. Immediate per-app cryptographic revocation is out of scope.

Features are operator-enabled only after compatible CAPI, BBS, cells and UAA are
deployed. Unsupported identity features must fail closed; silently dropping SANs
is not acceptable. Capability discovery and rollback must account for all cells
and consumers before enabling new assignments.

### Delivery and remaining decisions

1. Deliver the account lifecycle, native CLI, Diego identity, UAA bearer profile
   and explicit CAPI roles.
2. Add curated token targets/external federation and account sources for RFC 0055
   route policies. Route matching requires verified SAN-bearing certificate data
   and preserves caller org/space domain restrictions and default-deny behavior.
3. Negotiate broker/driver support for identity-based service bindings separately;
   this RFC does not standardize new OSB fields or change legacy bindings.

Maintainers should confirm ownership/permission defaults, name retention and
quotas, namespace protection, token/caller claim policy, API naming and mixed-version
capability signaling before finalizing the contract.

### Implementation evidence

Drafts: [CAPI][capi], [capi-release][release], [BBS contract][bbs], [Diego][diego],
[CLI][cli]. They preserve committed RED/GREEN tests and include verification notes.
The lab demonstrated two apps sharing a SAN with distinct keys, runtime-task
inheritance, roleless tokens seeing zero apps, explicit roles enabling access,
disable/enable, and unbind/restart/rebind through the native CLI.

**Remaining acceptance requirements:** the prototype's manager-only creation check
must align with service-instance permissions. Current [UAA mTLS work][uaa] emits `cnf`;
bearer-policy handling, leaf-expiry caps, managed-namespace enforcement and caller
claims require completion. BBS module publication and automatic rollout capability
signaling remain open. Timed live renewal, staging certificate inspection, Windows
execution and the full negative/rotation matrix need further evidence. Lab CAPI
calls used internal HTTP; production bearer use requires TLS. The POC therefore
does not yet meet the complete proposed profile.

[mtls]: https://www.rfc-editor.org/rfc/rfc8705.html#section-2.1
[binding]: https://www.rfc-editor.org/rfc/rfc8705.html#section-3.4
[capi]: https://github.com/cloudfoundry/cloud_controller_ng/pull/5520
[release]: https://github.com/cloudfoundry/capi-release/pull/702
[bbs]: https://github.com/cloudfoundry/bbs/pull/168
[diego]: https://github.com/cloudfoundry/diego-release/pull/1216
[cli]: https://github.com/cloudfoundry/cli/pull/3875
[uaa]: https://github.com/cloudfoundry/uaa/pull/4076
