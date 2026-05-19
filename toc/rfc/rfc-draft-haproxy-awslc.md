# Meta
[meta]: #meta
- Name: AWS-LC as TLS Backend for HAProxy
- Start Date: 2026-05-06
- Author(s): @hoffmaen
- Status: Draft
- RFC Pull Request:
- Affected Component(s): haproxy-boshrelease

## Summary

This proposal applies to HAProxy as deployed by haproxy-boshrelease, which Cloud Foundry uses as the HTTPS ingress in front of the Gorouter. It is **not** about the TCP Router shipped with cf-deployment, which is a separate component with a different role.

Today, HAProxy is linked against the OpenSSL version provided by the BOSH stemcell. In practice that currently means OpenSSL 3.0.2 — significant TLS performance improvements have landed in OpenSSL 3.5, but adopting them requires a stemcell that ships OpenSSL 3.5, which is outside this release's control.

Extend HAProxy with [AWS-LC](https://github.com/aws/aws-lc) as an optional TLS backend in Cloud Foundry's haproxy-boshrelease. AWS-LC is an open-source (Apache 2.0) cryptographic library maintained by AWS, based on BoringSSL, with a [FIPS 140-3 validated module](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4816).

Load testing demonstrates that AWS-LC delivers **43% lower CPU usage** and **65% higher peak TLS connection rate** compared to OpenSSL 3.0 for TLS handshakes. HAProxy upstream explicitly recommends against OpenSSL in production ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)).

The change is non-breaking: OpenSSL remains the default, and AWS-LC is offered as an opt-in variant alongside existing releases.

## Problem

HAProxy terminates all inbound TLS connections for Cloud Foundry. The TLS handshake is the most CPU-intensive operation on the ingress data path. Under connection-heavy workloads — rolling deployments, autoscaling events, short-lived connections — OpenSSL 3.0 becomes the bottleneck.

### Measured Performance Gap

Load testing on representative CF infrastructure (HAProxy 3.2.16, TLS 1.3, `oha --disable-keepalive` isolating handshake performance):

| Metric | OpenSSL 3.0 | AWS-LC | Improvement |
|--------|-------------|--------|-------------|
| Peak new TLS connections/s (CPU saturated) | ~5,000 | ~8,100 | **+65%** |
| CPU at 5,000 conn/s (c=20) | 86% | 49% | **-43%** |
| CPU at 4,000 conn/s (c=40) | 62% | 44% | **-29%** |
| p95 latency at 5,000 conn/s | 5.1ms | 3.5ms | **-32%** |
| p95 latency at saturation (10k target) | 23.6ms | 11.2ms | **-53%** |

With keepalive (no handshake per request), throughput is identical (~45k req/s). The difference is entirely in the **TLS handshake path**.

### Production Impact

In real Cloud Foundry deployments the OpenSSL bottleneck appears at much lower connection rates than the synthetic numbers above suggest. The HAProxy maintainers attribute this to OpenSSL's poor performance under realistic ingress workloads — particularly when HAProxy also opens encrypted connections to backends, which doubles the TLS work per request ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)). With AWS-LC we expect HAProxy to handle load peaks substantially better than what the synthetic benchmarks alone would predict.

- **Connection storms**: During rolling deployments, all clients reconnect simultaneously.
- **Tail latency**: Under load, OpenSSL's p95 grows to 23.6ms while AWS-LC stays at 11.2ms.
- **Scaling costs**: The 43% CPU reduction at typical operating rates eliminates unnecessary horizontal scaling.

### Upstream Recommendation

HAProxy maintainers explicitly recommend against OpenSSL, citing performance issues and architectural incompatibilities with OpenSSL 3.x's provider dispatch model ([haproxy#3086](https://github.com/haproxy/haproxy/issues/3086)). HAProxy ships optimized code paths for AWS-LC via the `USE_OPENSSL_AWSLC` build flag.

## Proposal

### Release Variants

Produce the following BOSH release tarballs from haproxy-boshrelease:

The naming schema treats OpenSSL as the standard: the existing release keeps its current name with no `-openssl` suffix and continues to link against the system-provided OpenSSL from the stemcell. AWS-LC variants carry an explicit `awslc` (and `awslc-fips`) suffix, so existing deployments see no naming change.

| Variant | TLS Backend | Description |
|---------|-------------|-------------|
| `openssl` | System OpenSSL | Default, backward-compatible (no change for existing users) |
| `openssl-patched` | System OpenSSL | With custom HAProxy patches |
| `awslc` | AWS-LC | High-performance, non-FIPS |
| `awslc-patched` | AWS-LC | With custom HAProxy patches |
| `awslc-fips` | AWS-LC FIPS 3.3.0 | FIPS 140-3 validated |
| `awslc-fips-patched` | AWS-LC FIPS | FIPS with custom HAProxy patches |
| `multi` | All of the above | Runtime-switchable, for migration |

### Single-Variant Releases

Each single-variant release contains one monolithic `haproxy` package with only the blobs required for that specific TLS backend. The packaging script auto-detects which library to build based on the included blobs.

These releases are **slim and deploy quickly**: only the necessary dependencies are compiled, and the release tarball contains no unused components. A typical OpenSSL deployment compiles in ~15 minutes; AWS-LC in ~25 minutes (including cmake).

### Multi-Variant Release

The multi release bundles all six HAProxy binaries into a single deployment. A BOSH property selects the active variant at runtime:

```yaml
properties:
  ha_proxy:
    ssl_variant: awslc  # openssl | openssl-patched | awslc | awslc-patched | awslc-fips | awslc-fips-patched
```

The multi release is **useful for migration scenarios**. When adopting AWS-LC, operators can switch back to OpenSSL in ~2 minutes (property change + redeploy) without recompilation. This is critical because:

- AWS-LC has slightly different cipher/curve support (no DHE, no X448)
- Issues may only surface under production traffic patterns
- Recompilation from scratch takes ~25 minutes; a property switch takes ~2 minutes

Once migration is validated, operators can switch to the slim single-variant `awslc` release for production.

### Build Architecture

The multi release avoids redundant compilation through shared packages:

```
haproxy-deps       → Lua, PCRE2, socat, hatop (compiled once, shared by all 6 variants)
cmake              → CMake (compiled once, shared by aws-lc and aws-lc-fips)
aws-lc             → AWS-LC library (non-FIPS)
aws-lc-fips        → AWS-LC FIPS library (requires Go toolchain for delocate)
haproxy-openssl    → HAProxy binary linked to system OpenSSL
haproxy-awslc      → HAProxy binary linked to AWS-LC
haproxy-awslc-fips → HAProxy binary linked to AWS-LC FIPS
```

HAProxy is compiled with `USE_OPENSSL_AWSLC=1` for both FIPS and non-FIPS. FIPS is a library property — HAProxy itself does not need separate FIPS logic.

### Runtime Selection

The job wrapper resolves the binary path at startup:

1. If `/var/vcap/packages/haproxy-<ssl_variant>` exists → use variant binary (multi release)
2. Otherwise → fall back to `/var/vcap/packages/haproxy` (single-variant release)

This ensures backward compatibility: existing deployments that use the single-variant `openssl` release continue to work without manifest changes.

### Cipher and Curve Differences

AWS-LC (both FIPS and non-FIPS) differs from OpenSSL in TLS cipher availability:

- **No DHE key exchange in TLS**: AWS-LC's TLS implementation only offers ECDHE, not DHE_RSA/DHE_DSS. This is a BoringSSL design decision (not FIPS-specific). The DH primitive exists in the library but is not wired into the TLS handshake.
- **No X448 curve**: Only X25519, P-256, P-384, P-521 are supported for key exchange.
- **No FFDH groups**: `ffdhe2048`, `ffdhe3072`, etc. are not available as named groups in TLS.
- **All TLS 1.3 ciphersuites work**: AES-128-GCM, AES-256-GCM, CHACHA20-POLY1305.
- **ECDHE ciphers for TLS 1.2 work**: All `ECDHE_RSA_*` and `ECDHE_ECDSA_*` suites are available.

In practice this has no client impact: DHE is rarely required by modern clients, and ECDHE provides equivalent or better security with superior performance. Existing cipher configurations that include both DHE and ECDHE ciphers continue to work — HAProxy silently skips DHE entries that AWS-LC cannot fulfill, and clients negotiate ECDHE instead.

**Compatibility note**: A client would only break on AWS-LC if it supports **DHE but not ECDHE**. Such stacks predate ~2010 and also predate TLS 1.2. Under a TLS 1.2-minimum policy (already enforced in this deployment), they are filtered out at the protocol layer regardless of cipher selection — every client that can negotiate TLS 1.2 also supports ECDHE. Clients that currently happen to negotiate DHE will transparently fall back to ECDHE with no visible impact.

Recommended curve configuration for AWS-LC: `X25519:P-256:P-384:P-521`

### FIPS Verification

The AWS-LC FIPS module is built from a frozen, certified source tree using a fixed compiler toolchain. To produce a FIPS-compliant binary, AWS-LC's build process runs a `delocate`/`inject_hash` step that rewrites assembly and embeds an integrity hash of the module into the resulting library. This step is implemented in Go, so a Go toolchain (~200MB) must be available at compile time. Go is only a build-time dependency — it is cleaned up after the FIPS library is built and is not part of the runtime.

FIPS mode can be verified at runtime:

- `haproxy -vv` reports "AWS-LC FIPS 3.3.0"
- Stats socket: `SslFipsModeRuntime: 1`

### Version Management

All component versions (HAProxy, Lua, PCRE2, AWS-LC, CMake, Go) are defined in a single `src/haproxy-versions.sh` file, sourced by all packaging scripts. The existing autobump CI job updates this file for automated dependency bumps.

### Proposed, Low-Risk Migration Path

The path below is **fully optional**. The multi release exists as a **safety net** for operators who want fast rollback to OpenSSL during the transition. It is not a required step, and it is not the intended long-term home for AWS-LC deployments — once a deployment has settled on AWS-LC, the slim single-variant `awslc` (or `awslc-fips`) release is the recommended target. The slim release contains exactly one HAProxy binary, has a small tarball, deploys quickly, and **does not require the `ha_proxy.ssl_variant` property** at all (it falls back to `/var/vcap/packages/haproxy` directly).

Two equally valid adoption routes:

- **Direct route (recommended once confident)**: deploy the slim `awslc` release. No `ssl_variant` property, no multi-binary overhead, no compilation of unused variants.
- **Safety-net route (recommended for risk-averse migrations)**: deploy the multi release first, set `ssl_variant: awslc`, validate under production traffic, and once confident, switch to the slim `awslc` release. If problems surface during the multi-release phase, flipping `ssl_variant` back to `openssl` and redeploying takes ~2 minutes with no recompilation.

Phased rollout:

1. **Phase 1** (this RFC): ship AWS-LC variants alongside OpenSSL. No change for existing deployments.
2. **Phase 2** (optional): operators choose the safety-net route via the multi release, **or** jump directly to the slim single-variant `awslc` release.
3. **Phase 3**: switch the default release shipped by haproxy-boshrelease (the no-suffix slim release) from OpenSSL to AWS-LC. The multi release continues to exist for migrations but is not the long-term target — most production deployments end up on a slim single-variant release.

## Alternatives Considered

### WolfSSL

HAProxy supports WolfSSL, but it requires a commercial license for production use. AWS-LC is fully open source (Apache 2.0 + ISC).

### Tuning OpenSSL Configuration

OpenSSL 3.x's provider dispatch architecture introduces per-operation overhead that cannot be eliminated through configuration. The HAProxy maintainers have stated this architectural mismatch is fundamental.

### BoringSSL

AWS-LC is a maintained fork of BoringSSL with stable releases, FIPS validation, and dedicated support. BoringSSL itself has no stable release cadence or FIPS certification.

### Replacing HAProxy Entirely

Alternatives like Envoy or nginx exist but would require rewriting the entire BOSH release, job templates, and operator tooling. The TLS library swap achieves the performance goal with minimal disruption.

## References

- [HAProxy issue #3086: Recommend against OpenSSL](https://github.com/haproxy/haproxy/issues/3086)
- [AWS-LC GitHub](https://github.com/aws/aws-lc)
- [AWS-LC FIPS 140-3 certificate #4816](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4816)
- [oha load testing tool](https://github.com/hatoo/oha)
- [Implementation branch](https://github.com/cloudfoundry/haproxy-boshrelease/tree/aws-lc-multi)
