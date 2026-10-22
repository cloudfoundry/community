# Meta
[meta]: #meta
- Name: AWS-LC as TLS Backend for HAProxy
- Start Date: 2026-05-06
- Author(s): @hoffmaen
- Status: Accepted
- RFC Pull Request: [community#1501](https://github.com/cloudfoundry/community/pull/1501)
- Related RFCs: [RFC#23: CF components support FIPS certified stemcells](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0023-add-cf-supports-for-fips-stemcell.md)
- Affected Component(s): haproxy-boshrelease

## Summary

**Note:** This proposal applies to HAProxy as deployed by haproxy-boshrelease, which Cloud Foundry uses as the HTTPS ingress in front of the Gorouter. It is **not** about the TCP Router shipped with cf-deployment, which is a separate component with a different role.

Today, HAProxy is linked against the OpenSSL version provided by the BOSH stemcell. In practice that currently means OpenSSL 3.0.2 — significant TLS performance improvements have landed in OpenSSL 3.5, but adopting them requires a stemcell that ships OpenSSL 3.5, which is outside this release's control.

Extend HAProxy with [AWS-LC](https://github.com/aws/aws-lc) as an optional TLS backend in Cloud Foundry's haproxy-boshrelease. AWS-LC is an open-source (Apache 2.0) cryptographic library maintained by AWS, based on BoringSSL, with a [FIPS 140-3 validated module](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4816).

Load testing demonstrates that AWS-LC delivers **43% lower CPU usage** and **65% higher peak TLS connection rate** compared to OpenSSL 3.0 for TLS handshakes. Under FIPS, the gap widens further to **45% lower CPU** and **125% higher peak rate** (OpenSSL FIPS vs AWS-LC FIPS). HAProxy upstream explicitly recommends against OpenSSL in production ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)).

In addition to the performance gap, AWS-LC ships native **post-quantum-safe TLS key exchange** (ML-KEM / Kyber), which OpenSSL 3.0 does not support. Adopting AWS-LC therefore unlocks a forward-looking security capability that the current stemcell-provided OpenSSL cannot offer, ahead of the upcoming OpenSSL 3.5 stemcell adoption.

The change is non-breaking: a single release bundles every variant, OpenSSL remains the default, and AWS-LC is selected opt-in at deploy time via a BOSH property — existing deployments are unaffected.

## Problem

HAProxy terminates all inbound TLS connections for Cloud Foundry. The TLS handshake is the most CPU-intensive operation on the ingress data path. Under connection-heavy workloads — rolling deployments, autoscaling events, short-lived connections — OpenSSL 3.0 becomes the bottleneck.

### Production Impact

In real Cloud Foundry deployments the OpenSSL bottleneck appears at lower connection rates than synthetic benchmarks alone would suggest. The HAProxy maintainers attribute this to OpenSSL's poor performance under realistic ingress workloads — particularly when HAProxy also opens encrypted connections to backends, which doubles the TLS work per request ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)). With AWS-LC we expect HAProxy to handle load peaks substantially better than what the synthetic benchmarks alone would predict.

- **Connection storms**: During rolling deployments and client reconnection waves, large numbers of new TLS handshakes arrive simultaneously and saturate the ingress.
- **Tail latency**: Under load, OpenSSL's p95 handshake latency grows steeply while AWS-LC remains stable.
- **Scaling costs**: The CPU reduction at typical operating rates eliminates unnecessary horizontal scaling and frees headroom for traffic spikes.

### HAProxy Upstream Recommendation

HAProxy maintainers explicitly recommend against OpenSSL, citing performance issues and architectural incompatibilities with OpenSSL 3.x's provider dispatch model ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)). HAProxy ships optimized code paths for AWS-LC via the `USE_OPENSSL_AWSLC=1` build flag, and HAProxy Technologies publishes a [State of SSL Stacks](https://www.haproxy.com/blog/state-of-ssl-stacks) review that recommends AWS-LC and ships [official Community Performance Packages compiled with AWS-LC](https://www.haproxy.com/company/news/haproxy-technologies-announces-availability-of-haproxy-community-performance-packages-compiled-with-aws-lc).

Other TLS libraries supported by HAProxy were considered and rejected: WolfSSL requires a commercial production license, while upstream BoringSSL has no stable release cadence and no FIPS certification. AWS-LC is the only option that combines an open-source license, stable releases, FIPS 140-3 validation, and an HAProxy-optimized integration path.

### No Post-Quantum TLS Support in OpenSSL 3.0

A growing class of security-sensitive workloads — financial integrations, long-lived B2B confidential data, government / healthcare connectors — has multi-decade confidentiality requirements that the **"harvest now, decrypt later"** threat model puts at risk. An adversary recording encrypted traffic today could decrypt it once a cryptographically relevant quantum computer exists. Mitigating this requires post-quantum-safe key exchange in TLS today, not at some future migration point.

OpenSSL 3.0 — the version currently shipped by the stemcell — has **no native post-quantum key exchange or signature support.** Native ML-KEM (FIPS 203, "Kyber") and ML-DSA (FIPS 204, "Dilithium") only landed upstream in OpenSSL 3.5 (2025). PQ on OpenSSL 3.0 is only available via the third-party `oqs-provider` from the Open Quantum Safe project, which is a separate install and not part of any supported stemcell.

AWS-LC, by contrast, ships native post-quantum support today:

- **ML-KEM (Kyber, FIPS 203)** — TLS 1.3 hybrid named groups such as `X25519MLKEM768` that combine classical X25519 with ML-KEM-768. Used in production by AWS, Google, and Cloudflare.
- **ML-DSA (Dilithium, FIPS 204)** — post-quantum signature scheme; deployable today on internal mTLS where both sides are controlled, and a forward path for public certificate signing once the CA ecosystem catches up.
- **Hybrid groups** are TLS 1.3 named groups, configured via the existing `ssl-default-bind-curves` knob — no HAProxy code changes required to enable them.
- AWS-LC's PQ algorithms are **FIPS 140-3 validated** as part of AWS-LC FIPS 3.3.0, so the FIPS variant retains PQ capability.

For details on the algorithms and their integration in AWS-LC, see the upstream [PQREADME](https://github.com/aws/aws-lc/blob/main/crypto/fipsmodule/PQREADME.md).

Adopting AWS-LC therefore closes a forward-looking security gap that cannot be closed within the current OpenSSL 3.0 stemcell. The capability is opt-in (operators must add a PQ named group to the curves list) and additive: clients without PQ support continue to negotiate classical curves with no behavioural change.

## Proposal

Ship a **single haproxy-boshrelease** that bundles every HAProxy build — the three SSL backends (system OpenSSL, AWS-LC, AWS-LC FIPS), each compiled both with and without the custom HAProxy patches — and let operators select which binary runs at deploy time via two BOSH properties. OpenSSL remains the default, so existing deployments are unaffected and no new release tarballs or naming schemes are introduced.

> **Design note:** an earlier revision of this RFC proposed a matrix of slim single-variant release tarballs plus a separate `multi` release. During implementation we consolidated to a *single* release containing all variants, because compiling the complete release takes only ~5–6 minutes — so the slim per-variant tarballs saved little deploy-time compile while multiplying the release/pipeline surface to maintain. The sections below describe the consolidated design.

### Selectable Builds

The single release bundles all six HAProxy binaries. Two orthogonal BOSH properties select which one runs at deploy time:

- `ha_proxy.ssl_variant` — the TLS backend: `openssl` (default), `awslc`, or `awslc-fips`.
- `ha_proxy.include_haproxy_patches` — whether to run the build carrying the custom HAProxy patches: `false` (default) or `true`.

OpenSSL remains the standard: both properties default to the OpenSSL/unpatched build, which continues to link against the system-provided OpenSSL from the stemcell, so existing deployments see no change. The resulting combinations:

| `ssl_variant` | `include_haproxy_patches` | Binary | Notes |
|---|---|---|---|
| `openssl` (default) | `false` (default) | system OpenSSL | backward-compatible default — no change for existing users |
| `openssl` | `true` | system OpenSSL + patches | |
| `awslc` | `false` | AWS-LC | high-performance, non-FIPS |
| `awslc` | `true` | AWS-LC + patches | |
| `awslc-fips` | `false` | AWS-LC FIPS 3.3.0 | FIPS 140-3 validated |
| `awslc-fips` | `true` | AWS-LC FIPS + patches | FIPS with custom HAProxy patches |

#### Custom HAProxy Patches (`include_haproxy_patches`)

The patched builds apply a single patch that relaxes HAProxy's enforcement of [RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455) (the WebSocket protocol). Stock HAProxy rejects a WebSocket upgrade request whose `Sec-WebSocket-Key` header is missing or malformed; the patch removes that validation in the HTTP/1 multiplexer so such requests are accepted and forwarded to the backend.

- **Why it is needed:** some scenarios require WebSocket support for legacy clients that open long-lived WebSocket connections without sending a spec-compliant `Sec-WebSocket-Key`. These clients predate strict RFC 6455 enforcement and cannot be changed; without the patch their connections are rejected at the ingress. This requirement has been carried across HAProxy releases (it is not new to any particular HAProxy major version).
- **Why it cannot be the default:** the patch makes HAProxy intentionally non-compliant with RFC 6455 (it accepts malformed WebSocket handshakes). Shipping it by default would weaken protocol conformance for every operator, so it is offered only as an explicit opt-in.
- **Why it is a precompiled build selected by a property, not a compile-time toggle:** BOSH properties are evaluated at deploy time, and BOSH does not recompile a package when a property changes — so the patch cannot be applied conditionally at compile time from a property. Instead the release ships both the patched and the unpatched binary for every SSL backend (each content-addressable), and `ha_proxy.include_haproxy_patches` selects between the already-compiled binaries at deploy time.

Operators who do not have this legacy-WebSocket requirement leave `include_haproxy_patches` at its default (`false`).

#### One Release, Selected at Deploy Time

There is a single release tarball. It bundles all six HAProxy binaries plus the shared dependencies, and the two properties above pick the active binary at runtime:

```yaml
properties:
  ha_proxy:
    ssl_variant: awslc              # openssl (default) | awslc | awslc-fips
    include_haproxy_patches: false  # default; set true for the patched build
```

Switching TLS backend (or toggling the patches) is a **property change plus redeploy (~2 minutes), with no recompilation** — the target binary is already compiled and installed. Adoption and rollback are therefore cheap and fully reversible: if an AWS-LC issue surfaces under production traffic, flipping `ssl_variant` back to `openssl` and redeploying restores the previous behaviour in minutes. This matters because:

- AWS-LC has slightly different cipher/curve support (no DHE, no X448)
- Issues may only surface under production traffic patterns

Compiling the **complete** release on the deploy target takes only **~5–6 minutes** for all variants combined, because the expensive dependencies (`haproxy-deps`, `aws-lc-src`, `cmake`) are compiled once and shared (see Build Architecture). Because the full build is this cheap, there is no benefit to maintaining separate slim per-variant releases: a single release keeps the build matrix, the CI pipeline, and the operator-facing choices simple, while costing only a few minutes of one-time deploy compilation.

### Build Architecture

The release avoids redundant compilation through shared packages, so building all variants together is far cheaper than six independent builds:

```
haproxy-deps                 → Lua, PCRE2, socat, hatop (compiled once, shared by all binaries)
aws-lc-src                   → AWS-LC source, unpacked once (shared by aws-lc and aws-lc-fips)
cmake                        → CMake (shared by aws-lc and aws-lc-fips)
aws-lc / aws-lc-fips         → AWS-LC libraries (FIPS adds -DFIPS=1 + a Go toolchain for delocate)
haproxy-openssl[-patched]    → HAProxy linked to system OpenSSL  (± patches)
haproxy-awslc[-patched]      → HAProxy linked to AWS-LC          (± patches)
haproxy-awslc-fips[-patched] → HAProxy linked to AWS-LC FIPS     (± patches)
```

HAProxy is compiled with `USE_OPENSSL_AWSLC=1` for both FIPS and non-FIPS. FIPS is a library property — HAProxy itself does not need separate FIPS logic. With the shared packages, compiling the entire release — all six HAProxy binaries plus both AWS-LC libraries — on the deploy target takes about **5–6 minutes**.

### Costs and CI Impact

Consolidating to a single release keeps both the pipeline and operator deploys simple.

**Operator deploy-time compilation is a one-time ~5–6 minutes.** A BOSH release tarball ships source and blobs; the compilation happens on the target VM at deploy time. Because every binary is bundled, a deploy compiles all of them — but thanks to the shared `haproxy-deps`, `aws-lc-src`, and `cmake` packages this is only ~5–6 minutes total, and it happens once. Subsequent redeploys reuse the compiled packages, so switching `ssl_variant` / `include_haproxy_patches` is a ~2-minute property change with no recompilation.

**The release pipeline produces exactly one tarball.** There is no per-variant fan-out: `bosh create-release` runs once, so pipeline wall-clock and artifact storage are those of a single release rather than seven. This is the main reason the design consolidated to one release — the slim per-variant tarballs saved only a couple of minutes of deploy-time compile (out of 5–6) while multiplying the number of artifacts, tarball-naming schemes, and release-pipeline steps to maintain.

**CI acceptance tests** exercise each TLS backend by deploying the single release and selecting the backend via `ha_proxy.ssl_variant` (`openssl`, `awslc`, `awslc-fips`), rather than building a separate release per backend.

### Runtime Selection

The job wrapper composes the binary package from the two properties at startup — `haproxy-<ssl_variant>`, with a `-patched` suffix appended when `include_haproxy_patches` is `true` — and runs it:

- `ssl_variant` unset / `openssl` **and** `include_haproxy_patches` unset / `false` → `haproxy-openssl`, the backward-compatible default; existing deployments need no manifest change.
- e.g. `ssl_variant: awslc-fips` + `include_haproxy_patches: true` → `haproxy-awslc-fips-patched`.

`ssl_variant` accepts only `openssl`, `awslc`, or `awslc-fips`. Any other value — including an old-style combined name such as `awslc-patched` — is a configuration error, and the job **fails fast with a clear message** rather than silently falling back to a different binary.

### Measured Performance Gap

The tables below quantify the production scenarios described in the Problem section. Load testing on representative CF infrastructure (HAProxy 3.2.16, TLS 1.3, `oha --disable-keepalive` isolating handshake performance):

| Metric | OpenSSL 3.0 | AWS-LC | Improvement |
|--------|-------------|--------|-------------|
| Peak new TLS connections/s (CPU saturated) | ~5,000 | ~8,100 | **+65%** |
| CPU at 5,000 conn/s (c=20) | 86% | 49% | **-43%** |
| CPU at 4,000 conn/s (c=40) | 62% | 44% | **-29%** |
| p95 latency at 5,000 conn/s | 5.1ms | 3.5ms | **-32%** |
| p95 latency at saturation (10k target) | 23.6ms | 11.2ms | **-53%** |

With keepalive (no handshake per request), throughput is identical (~45k req/s). The difference is entirely in the **TLS handshake path**.

### FIPS Performance Gap

The same benchmark was repeated with FIPS-validated builds (OpenSSL 3.0.2 with the FIPS provider vs AWS-LC FIPS 3.3.0). Under FIPS, the gap is roughly twice as large as in the non-FIPS case:

| Metric | OpenSSL FIPS | AWS-LC FIPS | Improvement |
|--------|--------------|-------------|-------------|
| Peak new TLS connections/s (CPU saturated, c=60) | 3,363 | 7,559 | **+125%** |
| CPU at 2,000 conn/s | 49% | 30% | **-39%** |
| p95 latency at 5,000 conn/s (c=20) | 11.5ms | 3.0ms | **-73%** |

OpenSSL FIPS saturates at less than half the connection rate of AWS-LC FIPS. This is consistent with OpenSSL 3.0's provider dispatch model: every cryptographic operation pays an indirection cost that the FIPS provider compounds with additional self-test bookkeeping. AWS-LC's FIPS module is integrated directly into its TLS implementation without that overhead, so customers requiring FIPS compliance pay the *largest* performance penalty under OpenSSL — and gain the most from migrating to AWS-LC.

### Cipher and Curve Differences

AWS-LC (both FIPS and non-FIPS) differs from OpenSSL in TLS cipher availability:

- **No DHE key exchange in TLS**: AWS-LC's TLS implementation only offers ECDHE, not DHE_RSA/DHE_DSS. This is a BoringSSL design decision (not FIPS-specific). The DH primitive exists in the library but is not wired into the TLS handshake.
- **No X448 curve**: Only X25519, P-256, P-384, P-521 are supported for key exchange.
- **No FFDH groups**: `ffdhe2048`, `ffdhe3072`, etc. are not available as named groups in TLS.
- **All TLS 1.3 ciphersuites work**: AES-128-GCM, AES-256-GCM, CHACHA20-POLY1305.
- **ECDHE ciphers for TLS 1.2 work**: All `ECDHE_RSA_*` and `ECDHE_ECDSA_*` suites are available.

The practical impact is small but **not zero**. Clients that already support ECDHE are unaffected: with haproxy-boshrelease's default `ssl_ciphers` ordering (defined in `jobs/haproxy/spec`), which lists every ECDHE suite ahead of any DHE suite, any client capable of ECDHE is already negotiating it today and sees no change on AWS-LC. The affected population is the set of clients that negotiate **DHE and cannot do ECDHE** — for these, there is no fallback, and the handshake fails on AWS-LC.

Crucially, a DHE-only client does **not** transparently fall back to ECDHE: under the default cipher ordering, if it were capable of ECDHE it would already have negotiated ECDHE. This is because HAProxy enables server cipher preference by default (`SSL_OP_CIPHER_SERVER_PREFERENCE`, which also governs curve/group selection), so HAProxy picks the first entry in its own ordered list that the client supports — and every ECDHE suite sits ahead of any DHE suite in the default list. So the clients currently negotiating DHE are, by definition, the ones for which DHE was the only mutually-supported key exchange. This preference ordering is operator-configurable — it can be inverted with `prefer-client-ciphers` (which haproxy-boshrelease does not set by default), and an operator could place DHE ahead of ECDHE in the list, though there is no practical reason to — so it is a property of the shipped default rather than a guarantee.

That said, genuinely **TLS 1.2-capable but DHE-only** clients are rare in absolute terms, and the affected volume is quantifiable in advance from the access logs: before DHE is disabled these handshakes still succeed (so they produce no `ssl_fc_err`), but they can be counted by the negotiated-cipher fetch, i.e. requests where a `DHE-*` suite was selected. This lets the impact be measured and the affected clients identified *before* the switch, rather than discovered afterwards. The migration path further de-risks it via the reversible, property-based rollback (flip `ssl_variant` back to `openssl` and redeploy).

Recommended curve configuration for AWS-LC: `X25519:P-256:P-384:P-521`

### Testing

haproxy-boshrelease already has a substantial test suite that this proposal reuses rather than reinvents:

- **Go/Ginkgo acceptance suite** (`acceptance-tests/…`) — deploys the release to a real BOSH director and drives live traffic. It already exercises the TLS data path end to end: HTTPS over **TLS 1.2 and 1.3**, HTTP/1.1 and HTTP/2 with **ALPN** negotiation (`https_frontend_test.go`), **mTLS** client-cert verification (`mtls_frontend_test.go`), **strict SNI** (`strict_sni_test.go`), **WebSocket** proxying (`websocket_test.go`), domain-fronting protection, external cert lists, client-cert forwarding, plus ~20 further feature tests.
- **rspec template specs** (`spec/haproxy/templates/…`) — render the job templates under given properties and assert on the rendered config, without deploying.

**Primary regression strategy: run the existing acceptance suite against the AWS-LC variant.** The suite already asserts that TLS termination, mTLS, SNI, ALPN, and WebSocket proxying all work. Running it unchanged against an AWS-LC-linked binary is the strongest guarantee that swapping the TLS library preserves behaviour — if AWS-LC broke any part of the TLS data path, these existing tests fail. The acceptance pipeline therefore gains an AWS-LC (non-FIPS) run of the suite.

**New test added by this proposal: an rspec spec for the variant selector.** The `ha_proxy.ssl_variant` → binary-resolution logic in the job wrapper is new and template-level, so it is covered by an rspec template spec: the correct package path is selected for each variant, and an absent/misconfigured variant is handled per the Runtime Selection behaviour rather than silently falling back.

**Deliberately not added:**

- **A separate FIPS acceptance run.** Each acceptance run compiles the release on the deploy target (~20–30 min for an AWS-LC variant); adding a second full suite run for `awslc-fips` roughly doubles that cost for little additional signal, since FIPS is a property of the linked library, not of HAProxy's behaviour. FIPS activation is verified out-of-band during release validation (`haproxy -vv` / stats-socket `SslFipsModeRuntime`) rather than on every acceptance run.
- **Synthetic per-cipher / per-curve negotiation tests.** The repo's testing style is functional (drive a real client, assert the request succeeds), not primitive-level. Asserting the exact negotiated cipher or forcing a DHE-only client adds brittle tests that do not match how this suite is written; the cipher/curve differences are documented above and bounded by the recommended configuration.

### Version Management

Component versions are defined in two files sourced by the packaging scripts: `src/haproxy-versions.sh` (HAProxy, Lua, PCRE2, socat, hatop) and `src/aws-lc-versions.sh` (AWS-LC, CMake, Go). They are kept separate so a HAProxy bump does not change the AWS-LC packages' fingerprints and force an unnecessary AWS-LC recompile. The existing autobump CI job updates both for automated dependency bumps.

### Proposed, Low-Risk Migration Path

Because everything lives in one release and switching is a property change, adoption and rollback are both cheap and fully reversible — there is no separate release to move between, and the reversibility *is* the safety net.

1. **Phase 1** (this RFC): ship the release with AWS-LC bundled. No change for existing deployments — `ssl_variant` defaults to `openssl`.
2. **Phase 2** (optional): operators set `ssl_variant: awslc` (or `awslc-fips`) and redeploy, then validate under production traffic. If an issue surfaces, flipping `ssl_variant` back to `openssl` and redeploying restores the prior behaviour in ~2 minutes with no recompilation.
3. **Phase 3**: change the shipped default `ssl_variant` from `openssl` to `awslc` once the ecosystem has validated it, so new deployments get AWS-LC by default while OpenSSL remains selectable via the property.

### cf-deployment Integration

cf-deployment integration is **out of scope** for this RFC. haproxy-boshrelease is not part of the cf-deployment base manifest; it is opt-in via `operations/use-haproxy.yml`, which adds the `haproxy` release at a version that is bumped automatically, plus an `haproxy` instance group. Operators who adopt AWS-LC manage their own release pinning outside the cf-deployment auto-bump flow (as this release is already consumed in practice), so no change to cf-deployment is required for this proposal.

First-class cf-deployment support could be added later, for example a variant selector in `use-haproxy.yml` that picks the `-awslc` / `-awslc-fips` release while still tracking automatic version bumps. That is a cf-deployment-side change and is explicitly **out of scope** for this RFC.

## Alternatives Considered

OpenSSL configuration tuning was evaluated but cannot eliminate OpenSSL 3.x's per-operation provider dispatch overhead, which is architectural. Replacing HAProxy entirely with Envoy or nginx would solve the TLS performance problem but require rewriting the entire BOSH release, job templates, and operator tooling — disproportionate scope for a TLS-library swap.

## References

- [HAProxy issue #3086: Recommend against OpenSSL](https://github.com/haproxy/haproxy/issues/3086)
- [HAProxy Technologies — State of SSL Stacks](https://www.haproxy.com/blog/state-of-ssl-stacks)
- [HAProxy Technologies — Community Performance Packages compiled with AWS-LC](https://www.haproxy.com/company/news/haproxy-technologies-announces-availability-of-haproxy-community-performance-packages-compiled-with-aws-lc)
- [AWS-LC GitHub](https://github.com/aws/aws-lc)
- [AWS-LC FIPS 140-3 certificate #4816](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4816)
- [oha load testing tool](https://github.com/hatoo/oha)
- [Implementation draft PR](https://github.com/cloudfoundry/haproxy-boshrelease/pull/925)
