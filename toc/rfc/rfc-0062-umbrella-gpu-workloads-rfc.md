# Meta
[meta]: #meta
- Name: GPU Workloads in Cloud Foundry (Umbrella)
- Start Date: 2026-09-21
- Author(s): @johha, @ZPascal
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)
- Related RFCs: (the follow-up RFCs, once opened)
- Affected Component(s): BOSH/Stemcells, Diego (BBS, Auctioneer, Rep, Executor), Garden/garden-runc, Cloud Controller (CAPI), CF CLI, Buildpacks, cf-deployment

> **Note:** This is a working draft maintained in the `cf-gpuccino` proof-of-concept
> repository. It is not yet submitted to the Cloud Foundry community repo.

## Summary

GPUs have become a baseline requirement for AI/ML workloads. Bringing GPU support
to Cloud Foundry lets these workloads run on the platform teams already know. They are
pushed with `cf push`, scheduled by Diego, and managed with the same tooling, quotas,
and operational model as every other app, instead of being sent off to Kubernetes
or raw IaaS.

This RFC proposes adding first-class GPU support to Cloud Foundry: scheduling
GPU-capable cells, allocating GPU devices to app containers, and exposing GPU as a
requestable resource through the API and manifest. Device injection is built on the
**Container Device Interface (CDI)**, the vendor-neutral standard already supported
by runc.

Because GPU support reaches from the BOSH stemcell up to the CF API, it spans several
working groups and is too large for a single RFC. This umbrella RFC establishes the
**shared goal, approach, scope, and non-goals**, and names the follow-up RFCs, one
per owning working group, that carry the detailed designs. **The follow-up RFCs are
created once this umbrella is merged**, so the community agrees on direction before
design work fans out. A working proof-of-concept already demonstrates the full path
end-to-end on real hardware; it is the evidence base referenced throughout.

## Problem

Cloud Foundry has no concept of a GPU. The gap is not in one place. It runs through
every layer that touches a workload:

- **No device model in the scheduler.** Diego schedules on CPU, memory, and disk.
  The BBS `DesiredLRP`, the auctioneer's placement scoring, and the rep's
  cell-capacity reporting have no notion of a GPU as a requestable, finite resource.
  There is no way to say "this app needs a GPU," and no way for a cell to advertise
  that it has one.

- **No device injection at the container runtime.** Even on a host with a GPU and
  drivers present, Garden/garden-runc has no mechanism to expose `/dev/nvidia*`
  devices and the supporting libraries into an application container. The OCI runtime
  supports this via CDI, but Garden does not drive it.

- **No GPU in the API or the developer contract.** The Cloud Controller has no field
  for requesting a GPU, so it cannot appear in the app manifest, the `cf` CLI, quotas,
  or usage reporting. A developer has no supported way to ask for one.

- **No host enablement story.** GPU cells need a specific NVIDIA driver and the
  supporting toolkit present and matched to the kernel. Installing drivers at deploy
  time is slow (DKMS compilation, several minutes per VM) and adds an external
  dependency at the worst possible moment.

The consequence: a team using CF for everything else hits a cliff the moment a workload
needs a GPU, and has to move it to a separate platform.

## Proposal

Add GPU as a first-class, schedulable resource in Cloud Foundry, end to end: a
developer requests a GPU, Diego places the app on a GPU-capable cell, and the device
is injected into the app container, with the same push-and-go experience as any
other app.

### High-level goals

1. **A developer can request a GPU through the standard contract** (app manifest and
   `cf` CLI) without knowing anything about drivers, devices, or cell topology.
2. **Diego schedules GPU workloads correctly.** Only cells with an available GPU win
   the placement, and a GPU is treated as a finite, allocatable resource, not
   overcommitted.
3. **The device is exposed into the container** using the Container Device Interface
   (CDI), the vendor-neutral standard already supported by the OCI runtime (runc).
4. **Host enablement is operationally sane.** GPU cells boot ready, without slow
   per-VM driver installation at deploy time.
5. **Additive and opt-in.** GPU support introduces no change in behavior for
   foundations that don't use it. Non-GPU cells, apps, and manifests are unaffected.
6. **Apps can be staged for GPU use.** Buildpacks/staging make the GPU usable from
   application code (CUDA runtime libraries and the expected environment such as
   `CUDA_VISIBLE_DEVICES` and library paths), so a developer's code can talk to the
   device without manual setup.

### Approach: CDI as the injection standard

The proposal standardizes on the **Container Device Interface (CDI)** for getting GPU
devices into containers. CDI is a vendor-neutral specification (NVIDIA, AMD, and
others) that describes device nodes, mounts, and environment as a declarative spec the
OCI runtime layer consumes. Recent runc versions (1.1+) support CDI natively; the POC
injects CDI devices at the Garden/guardian layer via the upstream
`tags.cncf.io/container-device-interface` library, so either integration point is
viable and the follow-up RFC settles which one CF standardizes on.

Building on CDI rather than a GPU-vendor-specific integration means:

- Garden's job is reduced to resolving CDI device references and applying the CDI
  edits, rather than embedding NVIDIA-specific device logic.
- The same mechanism extends to other accelerators (e.g. AMD/ROCm) without
  re-architecting **the runtime path**. Each vendor still needs its own host
  enablement (driver in the stemcell, CDI-spec generator).
- CF tracks an external standard rather than owning driver-injection glue.

The proof-of-concept validated this full path. A GPU request travels from a
`DesiredLRP` through the auctioneer, rep, and executor, into a CDI-injected container
reaching `/dev/nvidia0` on real hardware, so the approach is demonstrated, not
theoretical.

### Deployment model: regular cells + GPU cells

GPUs are expensive and comparatively scarce, so the expected topology is a normal CF
foundation of regular Diego cells **plus a smaller pool of GPU cells**, not every cell
carrying a GPU. This is the same shape CF already uses for specialized cells: **Windows
cells** (their own stemcell) and **isolation-segment cells** (the standard Linux
stemcell, set apart by placement/isolation configuration) are each added as a separate
`instance_group` in cf-deployment, with their own rep/garden configuration, while the
rest of the foundation is untouched.

A GPU cell fits that pattern directly: a dedicated instance group added via an ops file
(e.g. `add-gpu-cell.yml`), running the **GPU stemcell** and advertising **GPU capacity**
through its rep, much as a Windows cell runs the Windows stemcell and advertises its
preloaded rootfs. Scheduling then routes GPU-requesting apps onto GPU cells the same way
it routes Windows apps onto Windows cells. Whether GPU cells are expressed as a
capability of a cell pool (Windows-stack style) or via placement/isolation-segment
tagging is a design detail for the follow-ups; both existing mechanisms are viable
starting points. This work is owned by **App Runtime Deployments** (cf-deployment).

### Area sketches

The technical work breaks into three areas, each owned by the working group that owns
those components. These map onto the two follow-up RFCs described under *Phasing* below:
Host and Diego (plus the deployment model) form RFC A; the API/contract/staging area is
RFC B. The sketches set direction and boundaries; the follow-ups carry the detailed
design.

#### 1. Host & BOSH enablement (*Foundational Infrastructure*)

Get GPU-capable hosts booting ready to run GPU containers.

- A **GPU stemcell** ships with the vendor driver present and matched to the kernel,
  so cells don't compile drivers at deploy time. The POC bakes the NVIDIA driver
  (595 / CUDA 12.9) into a custom Ubuntu Noble stemcell, validated end-to-end on real
  hardware.
- The **container toolkit** (e.g. `nvidia-container-toolkit`) is present on GPU cells
  and **generates the CDI spec** the runtime consumes.
- Host enablement is **vendor-specific by nature**: each GPU vendor needs its own
  driver and CDI-spec generator. This RFC delivers the NVIDIA path; other vendors are
  parallel efforts.

#### 2. Diego scheduling & runtime (*App Runtime Platform*)

Make a GPU a schedulable, allocatable resource across the Diego stack, and inject it
into the container.

- **BBS**: carry a GPU request on the `DesiredLRP`; treat GPU as a finite resource in
  cell state.
- **Auctioneer / Rep**: cells advertise GPU capacity; placement scoring only assigns
  GPU workloads to cells with an available GPU (a veto/gate so GPUs are not
  overcommitted).
- **Executor**: discover, allocate, and release GPU devices per container (a "GPU
  manager"), and build the container spec with the right CDI device reference.
- **Garden / garden-runc**: accept a CDI device reference on the container spec and
  apply the CDI edits (device nodes, mounts, environment) to the OCI bundle. In the POC
  this injection happens at the guardian layer via the CDI library; whether it stays
  there or moves to runc's native CDI support is a follow-up design detail. Garden holds
  no vendor-specific device logic either way.
- **Metrics**: per-container GPU utilization and memory emitted through the existing
  metrics path (Loggregator → Log Cache), so GPU usage is visible via `cf app` and
  dashboards like any other resource metric.
- Known gap surfaced by the POC: GPU-allocation rollback on a container-create failure
  must be handled so device indices don't leak.

#### 3. API, developer contract & staging (*App Runtime Interfaces*, with Buildpacks)

Let developers request and use a GPU through the standard contract, without knowing
about drivers or cells.

- **Cloud Controller (CAPI)**: a GPU request field on the app, surfaced through the v3
  API. The POC models it as an app **feature flag** (the `gpu` app feature, backed by a
  `gpu_enabled` column); the exact resource model is an open question (below).
- **App manifest & `cf` CLI**: expose the request so `cf push` with a manifest is all
  a developer needs.
- **Quotas, usage & metering**: GPU counts against org/space quotas, appears in usage
  reporting, and emits usage records (GPU-time) so foundations can govern and charge
  back GPU consumption like any other resource.
- **Buildpacks / staging**: a GPU buildpack provisions the runtime libraries and
  environment (CUDA/ROCm, `CUDA_VISIBLE_DEVICES`, library paths) so application code
  can use the device. Owned within this RFC in collaboration with the **Buildpacks**
  working group. *(Out of scope in the POC; brought in here.)*
- The developer-facing request is designed to be **vendor-neutral**; how far that can
  go is an open question (below).

### Open questions

These are deliberately unresolved. The umbrella names them so the community can weigh
in; each is settled in the follow-up RFC for its area, not here.

**1. The GPU resource model: how does a developer request a GPU?**
The POC uses a simple **feature flag** (the `gpu` app feature, on/off) rather than a count like
`gpu: 2`. A raw count sits awkwardly next to instance count (is it per-instance or
total?), and by analogy CF doesn't ask for CPU cores directly; they're derived from
requested memory. Options to weigh: boolean feature flag · explicit count (`gpu: N`) ·
derived from a plan or memory tier. *(Owned by the API RFC.)*

**2. How vendor-neutral can the developer contract be?**
The request itself (manifest/CLI) is designed to name no vendor. But an app's own
binaries are built against a specific runtime (CUDA vs ROCm), and a GPU buildpack
necessarily targets one, so full app-level portability across vendors is not free
(unlike x86↔ARM, CUDA and ROCm are different APIs, not just different instruction sets).

The likely **baseline** is that a foundation is **single-GPU-vendor by operator
choice**, the same way operators today run a foundation on one CPU architecture rather
than mixing x86 and ARM. Under that assumption the developer never picks a vendor
(there is only one in the foundation) and the neutrality problem largely dissolves: the
developer asks for "a GPU" and gets the one kind available.

What remains open:
- **Mixed-vendor foundations.** Must CF support GPU cells of different vendors in a
  single foundation, with scheduling matching each app to a compatible cell? This is the
  genuinely hard, advanced case; single-vendor-per-foundation is the simpler default.
- **How the vendor is expressed** when it does need to be. One candidate is a **stack
  variant** (e.g. `cflinuxfs5-nvidia` / `cflinuxfs5-amd`), reusing CF's existing
  stack-matching in scheduling. It is not a perfect fit (a stack is a rootfs, whereas
  the driver lives in the stemcell and the device is injected at runtime via CDI), so
  this is a candidate mechanism, not a decision.

*(Owned by the API RFC, with input from Host/FI and Diego.)*

**3. Multi-tenancy & isolation of GPU access.**
The POC allocates a whole GPU to one container and does not harden the isolation
boundary. Open: what isolation guarantees must CF provide between GPU workloads
(memory, compute, side channels)? Is whole-GPU-per-container the only supported model
initially, and what security review is required before GPUs are shared? *(Spans Diego
and Host/FI.)*

**4. Fractional GPU sharing (MIG / time-slicing).**
Can one physical GPU back multiple app instances, via NVIDIA MIG partitions,
time-slicing, or similar? This affects the resource model (question 1), scheduling
granularity, and isolation (question 3). The POC treats a GPU as an indivisible unit.
Open whether fractional sharing is in an early phase or explicitly deferred. *(Spans
API and Diego.)*

### Non-goals

The target is a **meaningful class of GPU workloads**: model inference,
GPU-accelerated data processing, and smaller fine-tuning or experimentation. Given
that, this RFC does **not** aim to:

- **Turn Cloud Foundry into a large-scale model-training platform.** The target is
  inference, GPU-accelerated data processing, and modest fine-tuning/experimentation.
  Multi-node distributed training and specialized training-cluster orchestration are
  the wrong fit and are out of scope.
- **Deliver every GPU vendor at once.** The initial path is NVIDIA (driver + CUDA +
  `nvidia-container-toolkit`). AMD/ROCm and others are enabled by the CDI-based design
  but are parallel, follow-on efforts, not part of the first delivery.
- **Design the detailed per-component changes.** Those live in the follow-up RFCs.
  This umbrella sets direction, scope, and ownership only.
- **Mandate a specific resource model, vendor-neutrality guarantee, isolation model, or
  fractional-sharing scheme** (see Open Questions). The umbrella names these; the
  follow-ups decide them.

### Phasing: the follow-up RFC family

This umbrella is **Phase 0: agree the direction.** Once it is merged, two cross-cutting
follow-up RFCs are opened, grouped by concern rather than by working group, so each one
deliberately spans the groups that must agree on the interfaces between them (which is
what makes it an RFC rather than a set of independent PRs):

| Follow-up RFC | Working Groups | Covers |
|---|---|---|
| **A: GPU-capable cells: host, scheduling & deployment** | Foundational Infrastructure + App Runtime Platform + App Runtime Deployments | GPU stemcell / driver + container toolkit + CDI-spec generation (Host); BBS GPU fields, auctioneer/rep scoring, executor GPU manager, Garden CDI pass-through, GPU metrics (Diego); GPU cell instance group + ops file in cf-deployment |
| **B: Requesting & consuming GPUs: API, CLI & staging** | App Runtime Interfaces + Buildpacks | Resource model, manifest + `cf` CLI, quotas/usage/metering, GPU buildpack |

RFC A is the "make the platform able to run a GPU workload" story, end to end. The three
infra groups co-design it because the seams between them (how a cell boots ready, how it
advertises capacity, how it's deployed, how CDI specs flow from host to runtime) are
exactly what needs agreeing. RFC B is the developer contract on top; it depends on A but
does not need to co-design it. The area sketches above map onto these two: Host + Diego +
the deployment model into A, the API/contract/staging sketch into B.

Both RFCs link back to this umbrella (and to each other) via the `Related RFCs` field.
RFC B's API contract depends on decisions in RFC A and will likely settle later. Each
follow-up may phase its own delivery internally (e.g. proof-of-concept → implementation →
rollout).

**Why an umbrella rather than one RFC:** GPU support spans several working groups, and
CF precedent for changes this broad is to split along working-group seams and link the
pieces (as the Cloud Native Buildpacks work did across RFC-0017 → 0028 → 0031). A single
cross-cutting RFC has precedent too (IPv6 dual-stack, RFC-0038), but splitting lets each
working group own and merge its part independently. The umbrella keeps the shared goal,
scope, and open questions in one place so the follow-ups don't re-litigate direction.

## Testing & validation

The proof-of-concept already exercises the full path, which de-risks the follow-up
RFCs:

- **Host & compute:** GPU compute validated on real hardware (Tesla T4) via a BOSH
  lifecycle errand running PyTorch and TensorFlow benchmarks. Container GPU access
  validated via the toolkit + CDI (`nvidia-smi` and a CUDA workload inside a container
  on a BOSH-managed VM).
- **Scheduling & runtime:** a GPU request demonstrated travelling from a `DesiredLRP`
  through auctioneer → rep → executor → Garden/guardian into a CDI-injected container
  reaching `/dev/nvidia0`.

Each follow-up RFC defines its own acceptance criteria. At the family level, the
end-to-end bar is: **a developer pushes a GPU app via manifest/CLI, Diego places it
only on a GPU-capable cell, the device is injected via CDI, and the app runs a GPU
workload.** Quota enforcement and GPU metrics visibility are part of the fuller target
but are owned by RFC B and validated there, not preconditions for the RFC A path. Cloud
Foundry Acceptance Tests (CATs) should gain GPU-conditional coverage that is skipped on
foundations without GPU cells, so the suite stays green everywhere else.

## Related RFCs & references

- **Follow-up RFCs:** RFC A (GPU-capable cells: host, scheduling & deployment; FI + ARP
  + ARD) and RFC B (requesting & consuming GPUs: API, CLI & staging; ARI + Buildpacks).
  Links added as each is opened.
- **Precedent:** RFC-0038 (IPv6 dual-stack, single cross-cutting RFC); RFC-0017 / 0028 /
  0031 (Cloud Native Buildpacks, linked RFC family).
- **Container Device Interface (CDI):** the vendor-neutral device-injection standard,
  consumed by the OCI runtime layer (runc 1.1+ natively, or a CDI library at the
  Garden/guardian layer as in the POC).
- **Proof-of-concept:** design spec, implementation plan, deploy/validation runbook, and
  per-repo [fork/branch reference](poc-forks.md), the evidence base for this proposal.
