# Meta

- **Name:** ARM64 (aarch64) Architecture Support for Cloud Foundry
- **Start Date:** 2026-06-24
- **Author(s):** Sachin Vighe
- **Status:** Draft
- **Related RFCs:** [rfc-0026-noble-os](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0026-noble-os.md)
- **Affected Component(s):** bosh-linux-stemcell-builder, Diego, Garden-runC, Gorouter, Loggregator, Cloud Controller, UAA, cf-deployment, buildpacks

# Summary

This RFC proposes adding ARM64 (aarch64) architecture support to the Cloud Foundry ecosystem, enabling CF deployments on AWS Graviton and other ARM64 processors. This work is designed to offer potential cost-to-performance savings for CF operators while maintaining full compatibility with existing x86_64 deployments. A proof-of-concept has demonstrated that all major CF components compile and execute on ARM64 with zero source code changes. This RFC proposes a phased approach to deliver ARM64 stemcells, validate platform components, and produce ARM64-compatible buildpacks and stacks.

# Problem

Cloud Foundry currently supports only the x86_64 architecture. ARM64 processors are the fastest-growing architecture in cloud infrastructure, with all major cloud providers offering ARM64 instances. ARM64 instances offer 20–40% better price/performance compared to equivalent x86_64 instances, along with up to 60% better energy efficiency (sustainability benefits). CF operators cannot leverage these savings today because:

1. No ARM64 BOSH stemcells are published
2. CF component BOSH releases do not produce ARM64 artifacts
3. The `cflinuxfs4` root filesystem and buildpacks only ship x86_64 binaries
4. No ARM64 testing or CI/CD infrastructure exists

### Previous Work

In 2018, the Cloud Foundry community [demonstrated CF running on a Raspberry Pi](https://www.cloudfoundry.org/blog/baking-clouds-experiment-raspberry-pi-bosh-cloud-foundry/), identifying seccomp policy issues and syscall differences between ARM and x86_64 as key challenges. Since then, the ARM64 ecosystem has matured significantly — Go has had excellent ARM64 support since Go 1.5 (2015), the OCI runc project fully supports ARM64 with proper seccomp, and all major language runtimes ship ARM64 builds.

### Existing ARM64 Support

Some CF ecosystem tools already have ARM64 builds:
- **BOSH CLI** — already publishes ARM64 binaries
- **CF CLI** — already publishes ARM64 binaries
- **ARM64 JDKs** — production-ready ARM64 JDKs are available
- **Paketo Cloud Native Buildpacks** — already ARM64 compatible (see [ARM64 Paketo Buildpacks](https://www.cloudfoundry.org/blog/arm64-paketo-buildpacks/))

### Developer Workflow Benefit

ARM64 Linux support also benefits CF core developers on Apple Silicon MacBooks (M1/M2/M3/M4). All Go-based CF components can be cross-compiled locally using `GOOS=linux GOARCH=arm64`, enabling faster development and unit test iteration without needing remote infrastructure. Additionally, an ARM64 stemcell would enable running BOSH with the Docker CPI natively on Apple Silicon (see [bosh-deployment#497](https://github.com/cloudfoundry/bosh-deployment/issues/497)), giving developers a fully local CF environment without Rosetta emulation issues. Validating this local BOSH-lite workflow on Apple Silicon is included in the testing scope.

# Proposal

Enable ARM64 as a supported architecture through a phased approach, delivering the work across multiple working groups.

## Goals

1. **Enable ARM64 deployments** of Cloud Foundry across cloud providers
2. **Maintain x86_64 compatibility** — no breaking changes to existing deployments
3. **Support multi-architecture builds** in CI/CD pipelines
4. **Upstream all changes** to CF Foundation repositories (no provider-specific forks)
5. **Provide production-ready** ARM64 support (not experimental/preview)

## Success Criteria

- BOSH Acceptance Tests (BATS) pass on ARM64 stemcells
- CF Acceptance Tests (CATs) pass on ARM64 deployment
- Applications can be deployed via standard buildpacks on ARM64 cells
- Performance ≥ 100% of x86_64 baseline for equivalent instance classes
- Zero impact on existing x86_64 deployments

## Non-Goals

1. **Not breaking x86_64 support** — existing deployments continue unchanged
2. **Not requiring CF operators to migrate** — ARM64 is optional, operators opt in
3. **Not supporting 32-bit ARM** — only 64-bit ARM (aarch64)
4. **Not requiring homogeneous deployments** — mixed-architecture deployments (ARM64 Diego cells alongside x86_64 control plane) are in scope following the existing Windows cell model with architecture-aware placement
5. **Not creating provider-specific forks** — all work contributed upstream

## Phases

### Phase 1: ARM64 Stemcell

Publish an ARM64 BOSH stemcell based on the current CF Linux operating system (Ubuntu Noble, and subsequently Resolute Raccoon as it becomes available). The stemcell MUST include:

- ARM64 kernel and userspace
- BOSH agent compiled for ARM64
- EFI boot support for cloud environments
- Identical package set to the x86_64 stemcell

### Phase 2: Platform Component Validation

All BOSH releases in `cf-deployment` MUST produce ARM64 binaries alongside x86_64. Go-based components SHOULD cross-compile via CI with `GOARCH=arm64`. Components with C dependencies (e.g., Garden-runC, runC) MUST be validated with native ARM64 compilation. Components shipping pre-compiled binary blobs (e.g., JDK in uaa-release) MUST include ARM64 variants of those blobs, with packaging scripts selecting the correct variant based on stemcell architecture (`uname -m`).

### Phase 3: ARM64 Stack and Buildpacks

An ARM64 variant of the `cflinuxfs5` (Noble) root filesystem and ARM64-compiled buildpack dependencies MUST be produced to enable `cf push` application staging on ARM64 cells.

Key considerations for buildpack ARM64 support (informed by Paketo's experience):
- **Binary storage:** Architecture-specific blobs stored and accessed separately, selected at staging time based on cell architecture
- **Update monitoring:** Dependency update processes must be architecture-aware, checking for both x86_64 and ARM64 releases
- **Buildpack size:** Architecture-specific buildpack variants (separate downloads per arch) are preferred over bundling both architectures into a single buildpack to avoid doubling download size
- **Release pipelines:** Existing pipeline assumptions around single-architecture artifacts will need to be extended

### Phase 4: Multi-Architecture Deployment Support

`cf-deployment` SHOULD provide ops-files or native support for ARM64 deployments, allowing operators to deploy CF on ARM64 infrastructure.

# Proof of Concept Results

A proof-of-concept was conducted to validate ARM64 feasibility before proposing this RFC. The POC compiled and validated 30 ARM64 binaries from 7 major CF releases on real ARM64 hardware (4 vCPU, 16 GB RAM).

## Components Validated

| Component Group | Binaries | Result |
|---|---|---|
| **Diego** | rep, auctioneer, bbs, locket | ✅ Cross-compiles and executes |
| **Garden-runC** | gdn, grootfs, dadoo, dontpanic, thresholder, socket2me, execas, maximus, newuidmap, newgidmap | ✅ Cross-compiles and executes |
| **runC** | OCI container runtime | ✅ Builds natively with seccomp support |
| **Gorouter** | gorouter, routing-api, cf-tcp-router, route-registrar | ✅ Cross-compiles and executes |
| **Loggregator-agent** | loggregator-agent, forwarder-agent, syslog-agent, syslog-binding-cache, prom-scraper, udp-forwarder | ✅ Cross-compiles and executes |
| **Cloud Controller** | cc-uploader, tps-watcher (Go); 229 Ruby gems | ✅ Go cross-compiles; Ruby gems build natively |
| **UAA** | cloudfoundry-identity-server WAR | ✅ Architecture-independent (Java) |
| **BOSH** | bosh-agent, bosh-cli, bosh-agent-pipe; 134 Ruby gems | ✅ Go cross-compiles; Ruby gems build natively |

## Key Findings

1. **Zero source code changes required.** All Go components cross-compile cleanly with `GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build`. No patches or architecture-specific workarounds were needed.

2. **runC builds natively with full seccomp support.** The container runtime — the highest-risk component due to C code and architecture-specific syscall tables — compiles and functions correctly on ARM64. This resolves the key concern identified in the 2018 Raspberry Pi experiment.

3. **Ruby native extensions work.** All C-extension gems required by Cloud Controller (229 gems including nokogiri, puma, mysql2, oj, pg) and BOSH Director (134 gems) compile successfully on `aarch64-linux`.

4. **ARM64 stemcell boots successfully.** A prototype ARM64 stemcell (Ubuntu Jammy + BOSH agent, 784 MB) was built using `debootstrap --arch=arm64` with EFI boot support and validated on ARM64 hardware.

## POC Test Details

The integration test suite validates binary correctness on real ARM64 hardware rather than running existing component-level integration tests (e.g., Diego's inigo tests or Gorouter's integration suite). The tests verify:

- All 30 compiled binaries are valid ARM64 ELF executables (`file` command confirms `ELF 64-bit LSB executable, ARM aarch64`)
- Binaries execute correctly and respond to CLI flags (e.g., `--help`, `--version`)
- Ruby native extensions load correctly on `aarch64-linux` (require/load without errors)
- runC creates and runs containers on ARM64 with seccomp filtering
- A multi-container deployment simulation (router + apps + Diego components + BOSH agent + Garden) functions end-to-end

Component-specific integration test suites (e.g., CATs, BATS, Diego BBS tests) running on ARM64 would be part of the validation work in the proposed workstreams below.

## Performance

The POC validated that ARM64 delivers comparable or better performance than x86_64 for CF workloads, including Go compilation, application startup, and memory usage. Detailed benchmarking on production-representative infrastructure should be part of later validation phases within the workstreams.

# Workstreams

The implementation requires work across multiple CF working groups. The dependency chain is:

```
Stemcells (bosh-linux-stemcell-builder)
    ↓
BOSH Agent (bosh-agent)
    ↓
BOSH Director (bosh)
    ↓
Diego (diego-release) + Garden (garden-runc-release) ← critical path
    ↓
Cloud Controller (capi-release) + Routing + Logging
    ↓
cflinuxfs4 + Buildpacks
    ↓
Applications
```

## Foundational Infrastructure WG

The Foundational Infrastructure Working Group owns `bosh-linux-stemcell-builder` and the BOSH agent. Work includes:

- Extend `bosh-linux-stemcell-builder` to produce ARM64 stemcells (Ubuntu Noble initially, Noble/Resolute Raccoon when applicable)
- Validate the BOSH agent on ARM64 (POC has demonstrated this works)
- Set up CI pipelines producing ARM64 stemcell builds (ARM64 CI workers will be provided)
- Validate the BOSH Director (Ruby) operates correctly on ARM64 (POC validated 134 gems)
- Run BOSH Acceptance Tests (BATS) on ARM64 stemcells
- Publish 0.x beta ARM64 stemcells on bosh.io for community validation
- After successful community validation, publish 1.x GA ARM64 stemcells

## App Runtime Platform WG

The App Runtime Platform Working Group owns Diego, Garden-runC, Gorouter, Loggregator, and other runtime components. Work includes:

- Add ARM64 cross-compilation targets to CI pipelines for all Go-based components
- Validate Garden-runC (including runC with seccomp) on ARM64 Diego cells — **this is the critical path**
- Run component-level integration tests on ARM64 (Diego inigo tests, Gorouter integration tests)
- Validate the Loggregator pipeline on ARM64
- Validate container networking (Silk CNI, cf-networking) on ARM64
- Validate NATS and BPM on ARM64

## App Runtime Interfaces WG

The App Runtime Interfaces Working Group owns Cloud Controller (CAPI) and UAA. Work includes:

- Validate Cloud Controller Ruby application runs on ARM64 stemcells (POC validated gem compilation)
- Validate UAA Java WAR deploys and runs on ARM64 JVM (Eclipse Temurin, SAP Machine, or equivalent ARM64 JDK)
- Ensure the Go helper binaries (cc-uploader, tps-watcher) are built for ARM64 in CI
- Run Cloud Controller acceptance tests (CATS) on ARM64

## App Runtime Deployments WG

The App Runtime Deployments Working Group owns `cf-deployment`. Work includes:

- Set up cf-deployment validation against the ARM64 stemcell (similar to existing Jammy/Noble validation)
- Distribute issues discovered during validation to the responsible component Working Groups
- Provide an ops-file enabling operators to deploy CF on ARM64
- Validate the full CF deployment lifecycle (deploy, upgrade, scale) on ARM64

## App Runtime Interfaces WG (Classical Buildpacks)

The ARI Working Group owns the classical buildpacks which have higher adoption in CF today. Note: ARM64 support for Cloud Native Buildpacks (CNBs) is already being addressed by the Paketo WG separately (see [ARM64 Paketo Buildpacks](https://www.cloudfoundry.org/blog/arm64-paketo-buildpacks/)). Work for classical buildpacks includes:

- Produce ARM64 variants of classical buildpack dependencies (JDK, Node.js, Python, Ruby, Go, .NET, PHP, nginx runtimes)
- Produce an ARM64 variant of the `cflinuxfs4` root filesystem
- Validate classical buildpack `detect` and `compile` phases on ARM64 cells
- Update classical buildpack CI to produce and test ARM64 artifacts

## All CF Release Authors

- Add `GOARCH=arm64` cross-compilation to release CI pipelines
- Validate that BOSH release packaging scripts work on ARM64 stemcells
- Address any architecture-specific assumptions in job scripts or compilation scripts

## CI/CD Infrastructure

ARM64 build workers will be provided for Concourse pipelines to enable native ARM64 compilation and testing. The initial CI infrastructure will be contributed alongside the implementation work. Long-term CI/CD ownership should be discussed as part of this RFC.

# Open Questions

1. **Stemcell naming convention:** How should ARM64 stemcells be identified? Proposed: `ubuntu-jammy-arm64` alongside existing `ubuntu-jammy` (implicitly x86_64). Open to community input on naming and metadata approach.

2. **CI/CD long-term ownership:** ARM64 CI workers will be provided initially to unblock development. Should long-term ownership transfer to the CF Foundation, or remain as a community-contributed resource?

3. **Stemcell release cadence:** Should ARM64 stemcells follow the same release cadence as x86_64 from day one, or start with a separate beta cadence until stability is proven?

4. **Buildpack priority order:** Which buildpacks should be prioritized for ARM64 support? Proposed: Java → Go → Node.js → Python → Ruby → others. Open to community input based on operator demand.

# Affected Repositories

The full scope covers 60+ repositories across the CF ecosystem. The critical path (P0) repositories are:

**BOSH Infrastructure (5):**
- `bosh` — Core orchestration (Go, Ruby)
- `bosh-agent` — VM agent (Go)
- `bosh-linux-stemcell-builder` — Stemcell creation (Shell, Ruby)
- Cloud Provider Interfaces (CPIs) for target platforms (e.g., `bosh-aws-cpi-release`, `bosh-google-cpi-release`, `bosh-vsphere-cpi-release`) and corresponding light stemcell builders

**Container Runtime (4):**
- `diego-release` — Container orchestration (Go)
- `garden-runc-release` — Container runtime (Go + C) **[highest risk]**
- `grootfs` — Container filesystem (Go)
- `guardian` — Garden backend (Go)

**Core Services (5):**
- `capi-release` — Cloud Controller API (Ruby)
- `uaa-release` — Authentication (Java)
- `routing-release` — HTTP routing (Go)
- `loggregator-release` — Logging (Go)
- `nats-release` — Messaging (Go)

**Application Layer (2):**
- `cflinuxfs4-release` — Root filesystem (Shell)
- `java-buildpack` — Java applications (priority buildpack)

**Testing (1):**
- `cf-acceptance-tests` — Full platform validation (Go)

Remaining repositories (P1/P2) are primarily Go-based and are expected to cross-compile with minimal effort. A detailed repository inventory will be shared alongside this RFC.
