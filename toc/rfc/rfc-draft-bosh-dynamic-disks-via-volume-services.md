# Meta
[meta]: #meta
- Name: BOSH-Provided Dynamic Disks via Volume Services
- Start Date: 2026-03-13
- Author(s): @rkoster
- Status: Draft
- RFC Pull Request: [community#](https://github.com/cloudfoundry/community/pull/)


## Summary

Enable Diego containers to use IaaS-managed persistent disks through the existing volume services architecture:

- **BOSH Director** gains a `permissions` model controlling which instance groups may create, attach, detach, and delete disks
- **BOSH Agent** gains subcommands that relay disk requests to the Director over NATS
- **Volume driver** implements Docker Volume Plugin v1.12, translating volume operations into Agent disk commands

Diego's volman discovers this driver automatically — **zero changes to Diego, CAPI, or the CF CLI**.

This is a **foundation technology** enabling Cloud Foundry to run stateful single-container workloads — agentic coding sessions, cloud-based developer environments, and long-running AI agent processes — by giving Diego containers access to dedicated IaaS block storage managed by BOSH.


## Problem

A new class of workload is emerging: **single-container processes that need dedicated persistent storage as part of their own execution environment**.

- **Agentic coding sessions** — an AI agent operates within a workspace containing source code, build artifacts, and tool state
- **Cloud-based developer environments** — persistent scratch space tied to a single container
- **Batch jobs** — checkpoint intermediate state across restarts

These workloads need storage that survives container restarts but is tied to a single container — not a shared service.

Diego's volume services already attach persistent storage via drivers (`nfsv3driver`, `smbdriver`). What's missing is a driver backed by **dedicated IaaS block storage managed by BOSH**.


## Proposal

### Overview

The proposal has three layers:

1. **BOSH Director** — `permissions` model on instance groups controlling disk lifecycle operations, enforced at runtime
2. **BOSH Agent** — subcommands that relay disk requests to the Director over NATS (Agent is a relay, not an enforcement point)
3. **Volume driver for Diego** — Docker Volume Plugin v1.12 job on Diego cells; disk CIDs flow through CC service bindings (same as NFS/SMB)


### Layer 1: BOSH Director — Dynamic Disk Management

#### Permissions

Instance groups gain an optional `permissions` list controlling which disk operations they may request:

| Permission | Scope |
|---|---|
| `disk.create` | Create disks in own deployment |
| `disk.delete` | Delete disks in own deployment |
| `disk.list` | List disks in own deployment (by CID prefix) |
| `disk.self.attach` | Attach disks to the requesting VM only |
| `disk.self.detach` | Detach disks from the requesting VM only |
| `disk.attach` | Attach disks to any VM in own deployment (implies `disk.self.attach`) |
| `disk.detach` | Detach disks from any VM in own deployment (implies `disk.self.detach`) |
| `disk.<deployment>.create` | Create disks in named deployment (cross-deployment) |
| `disk.*.create` | Create disks in any deployment |

No deployment qualifier = scoped to own deployment. Broader permissions imply narrower ones (`disk.attach` implies `disk.self.attach`). The `permissions` list is extensible — future RFCs may add permissions for other resource types.

#### Deployment manifest

```yaml
name: cf

instance_groups:
  # Diego cells: attach/detach to self only (tightest scope)
  - name: diego-cell
    permissions:
      - disk.self.attach   # attach disks to THIS cell only
      - disk.self.detach   # detach disks from THIS cell only
    jobs:
      - name: bosh-volume-driver   # Docker Volume Plugin v1.12
        release: bosh-volume-services
      - name: rep
        release: diego
      # ...

  # Broker: create/delete only
  - name: volume-services-broker
    permissions:
      - disk.create       # provision IaaS disks
      - disk.delete       # deprovision IaaS disks
    jobs:
      - name: bosh-volume-broker   # Open Service Broker API
        release: bosh-volume-services
      # ...
```

Cross-deployment example — broker in a separate deployment managing disks for `cf`:

```yaml
name: volume-services

instance_groups:
  - name: broker
    permissions:
      - disk.cf.create    # create disks in the "cf" deployment
      - disk.cf.delete    # delete disks in the "cf" deployment
    jobs:
      - name: bosh-volume-broker
        release: bosh-volume-services
```

#### How it works

1. **Deploy time**: Director validates all `permissions` entries. Unknown permissions cause deploy errors.
2. **Runtime**: When a disk operation arrives over NATS, the Director identifies the Agent by its client certificate, resolves the instance group and deployment, and checks the `permissions` list. Unauthorized requests are rejected.
3. **Tracking**: Dynamic disks are marked `dynamic` in the Director DB, associated with a target deployment (which may differ from the creating deployment in cross-deployment cases). `bosh disks` surfaces them.
4. **Lifecycle**: When a deployment is deleted, associated dynamic disks are orphaned and follow existing orphan disk cleanup.

#### VM-level locking

Dynamic disk operations do **not** acquire deployment locks. Instead, the Director uses a fine-grained **VM lock** (`lock:vm:<vm_cid>`) around CPI `attach_disk` and `detach_disk` calls:

- Dynamic disk attach/detach and deploy-time attach/detach both acquire the VM lock
- Operations on **different VMs** proceed in parallel — no blocking
- Operations on the **same VM** are serialized — only one CPI attach/detach at a time
- Short lock timeout (60s) — dynamic disk ops fail fast if the VM is busy

This allows dynamic disk operations to proceed while a `bosh deploy` is running, as long as they target different VMs. If a deploy and a dynamic disk op target the same VM simultaneously, the VM lock serializes the CPI calls.


### Layer 2: BOSH Agent — Disk Primitives

The Agent is extended with subcommands that relay disk requests to the Director over NATS. The Agent does not enforce permissions — the Director is the sole enforcement point (see Layer 1). Each subcommand reads the Agent's existing NATS credentials and client certificate, sends a request, and outputs the result as JSON to stdout or exits non-zero with an error on stderr.

| Subcommand | Arguments | Description |
|---|---|---|
| `create-disk` | `--size <MiB>` `--disk-type <name>` | Create a disk via the CPI. Returns disk CID. |
| `delete-disk` | `--disk-cid <CID>` | Delete a disk via the CPI. |
| `attach-disk` | `--disk-cid <CID>` `[--agent-id <UUID>]` | Attach a disk. Without `--agent-id`: attach to self (requires `disk.self.attach`). With `--agent-id`: attach to target VM (requires `disk.attach`). Returns device path. |
| `detach-disk` | `--disk-cid <CID>` `[--agent-id <UUID>]` | Detach a disk. Without `--agent-id`: detach from self (requires `disk.self.detach`). With `--agent-id`: detach from target VM (requires `disk.detach`). |
| `list-disks` | `--prefix <string>` | List dynamic disks matching the CID prefix. Returns array of `{cid, size, created_at}`. For disk set support (see Future Work). |

The `--disk-type` argument references a disk type defined in the cloud config (e.g., `default`, `fast`, `large`). The Director resolves this to cloud properties at runtime, ensuring consistency with operator-defined disk configurations.

The `--agent-id` argument specifies the target VM by its Agent UUID (from the Agent's client certificate). Agent IDs are globally unique across all deployments. When omitted, the operation targets the calling Agent's own VM.

Collocated BOSH jobs invoke the Agent at a well-known path:

```bash
/var/vcap/bosh/bin/bosh-agent create-disk --size 10240 --disk-type default
```


### Layer 3: BOSH Volume Driver for Diego

A BOSH job (`bosh-volume-driver`) implements the [Docker Volume Plugin v1.12](https://docs.docker.com/engine/extend/plugins_volume/) protocol — the same protocol used by `nfsv3driver` and `smbdriver`. It is collocated on Diego cells and listens on a Unix socket.

| Endpoint | Behavior |
|---|---|
| `/VolumeDriver.Create` | Stores pre-created disk CID (from service binding opts) in local state |
| `/VolumeDriver.Mount` | Calls `bosh-agent attach-disk`, mounts filesystem, returns mountpoint |
| `/VolumeDriver.Unmount` | Unmounts filesystem, calls `bosh-agent detach-disk` |
| `/VolumeDriver.Remove` | Removes disk CID from local state (broker handles deletion) |
| `/VolumeDriver.Get/List/Path` | Returns volume info from local state |
| `/VolumeDriver.Capabilities` | Returns `{"Capabilities": {"Scope": "local"}}` |
| `/Plugin.Activate` | Returns `{"Implements": ["VolumeDriver"]}` |

#### Plugin discovery

Volman discovers drivers through spec files in `/var/vcap/data/voldrivers` (default). The job places a spec file at startup:

```json
{
  "Name": "bosh-volume-driver",
  "Addr": "unix:///var/vcap/data/bosh-volume-driver/driver.sock",
  "TLSConfig": null,
  "UniqueVolumeIds": true
}
```

Volman syncs every 30 seconds and calls `/Plugin.Activate` to verify the driver. No changes to Diego, volman, the Rep, or Garden.

#### Disk CID flow through Cloud Foundry

Disk CIDs flow from the broker to the volume driver through **Cloud Controller service bindings** — the same mechanism used by NFS and SMB volume services:

```mermaid
flowchart LR
    subgraph "Provisioning (broker)"
        B["Broker"] -->|"bosh-agent<br/>create-disk"| A1["Agent"] -->|"NATS"| D["Director<br/>→ CPI"]
    end

    subgraph "Binding (CC)"
        B -->|"bind response:<br/>driver + disk CID"| CC["Cloud<br/>Controller"]
    end

    subgraph "Runtime (diego-cell)"
        CC -->|"DesiredLRP<br/>volume_mounts"| Rep
        Rep -->|"Mount(disk-CID)"| VD["Volume<br/>Driver"]
        VD -->|"bosh-agent<br/>attach-disk"| A2["Agent"] -->|"NATS"| D2["Director<br/>→ CPI"]
    end
```

**How it works:**
1. User runs `cf create-service bosh-disk default my-workspace`. Broker calls `bosh-agent create-disk --disk-type default`, records the disk CID.
2. User runs `cf bind-service my-app my-workspace`. Broker returns volume mount config (driver name + disk CID) in the bind response.
3. Diego places the container. Rep passes volume mount to volman → `VolumeDriver.Mount` → `bosh-agent attach-disk` → mount filesystem into container.
4. Container stops. Rep calls `VolumeDriver.Unmount` → unmount → `bosh-agent detach-disk`.
5. User deletes service instance. Broker calls `bosh-agent delete-disk`.

This is identical to NFS/SMB volume services. The only difference is the backing storage: IaaS block devices instead of network filesystem shares.


### Security Model

- **No Director credentials in workloads.** Jobs call the local Agent binary; the Agent uses existing NATS mTLS credentials.
- **Director-enforced permissions.** The Director identifies callers by client certificate, resolves to instance group, and checks `permissions` before executing. Analogous to UAA scope checking.
- **No new network access.** The Agent already has NATS connectivity.
- **Disk isolation.** IaaS block devices can only be attached to one VM at a time (enforced by the IaaS).


### Scope and Deliverables

This RFC specifies **interface contracts and deployment model** only. Implied deliverables:

1. **BOSH Director** — `permissions` manifest property, deploy-time validation, runtime enforcement, NATS handlers for dynamic disk ops, dynamic disk tracking, orphan management
2. **BOSH Agent** — `create-disk`, `delete-disk`, `attach-disk`, `detach-disk` subcommands
3. **Volume driver job** — Docker Volume Plugin v1.12, collocated on Diego cells (`bosh-volume-services` release)
4. **Volume broker job** — Open Service Broker API for disk lifecycle, same release


## Future Work

### Kubernetes / CSI integration

The Agent disk primitives (Layer 2) are not Diego-specific. The same interface could back a [CSI driver](https://kubernetes-csi.github.io/docs/) for Kubernetes-based CF deployments.

CSI separates storage operations into two components:

- **Controller Plugin** (centralized) — handles `ControllerPublishVolume` (attach to a target node) and `ControllerUnpublishVolume`. Would use `disk.attach` and `disk.detach` permissions with `--agent-id` to target specific nodes.
- **Node Plugin** (per-node DaemonSet) — handles `NodeStageVolume` / `NodePublishVolume` (mount). Would use `disk.self.attach` and `disk.self.detach` permissions (or no attach permissions if the controller handles all attach/detach).

This RFC's permission model supports both patterns — Diego's local-only model (`disk.self.attach`) and K8s's centralized controller model (`disk.attach` + `--agent-id`). CSI driver implementation is out of scope for this RFC.

### Disk sets — per-instance persistent storage

This RFC specifies single-disk primitives. A natural extension is **disk sets** — a service instance that manages a collection of disks, one per app instance, analogous to Kubernetes StatefulSet `volumeClaimTemplates`.

#### Problem

Diego's `DesiredLRP` defines `volume_mounts` once for all instances — every instance receives identical mount configuration. This works for shared filesystems (NFS, SMB) but not for IaaS block devices, which can only attach to one VM at a time. To run multiple app instances with per-instance persistent storage, each instance needs its own disk with stable identity (instance 0 always gets disk 0, even after restart).

#### Concept

A **disk set** is a broker-managed collection of disks:

1. **Provision**: `cf create-service bosh-disk-set default my-workspace` — broker creates a disk set record (no disks yet)
2. **Bind**: `cf bind-service my-app my-workspace` — broker returns `volume_id = <disk-set-id>` (a namespace, not a single CID)
3. **Mount (per instance)**: Diego places instance N, volman calls the driver with an encoded volume ID containing the instance index. Driver resolves: "disk set X, index N → disk CID" (creates on first use). Driver calls `bosh-agent attach-disk`.
4. **Scale up**: New instances trigger new disk creation
5. **Scale down**: Disks are detached but **retained** (like K8s StatefulSet)
6. **Deprovision**: Broker deletes all disks in the set

#### Leveraging Diego's `UniqueVolumeIds` mechanism

Diego's volman already supports per-container volume differentiation via the `UniqueVolumeIds` driver spec flag. When a driver declares this flag, volman encodes `<volume-id>_<suffix>` before passing to the driver. The driver decodes prefix and suffix to handle per-container state.

Today, the suffix is the **container GUID** (a UUID that changes on every restart). For disk sets, the suffix must be the **instance index** (0, 1, 2 — stable across restarts). This requires a small Diego change:

**Proposed: `InstanceIndexedVolumes` driver spec flag**

```json
{
  "Name": "bosh-volume-driver",
  "Addr": "unix:///var/vcap/data/bosh-volume-driver/driver.sock",
  "UniqueVolumeIds": true,
  "InstanceIndexedVolumes": true
}
```

When `InstanceIndexedVolumes` is true, volman passes the instance index (from `ActualLRPKey.Index`) as the suffix instead of the container GUID. The Rep already has this value available in `NewRunRequestFromDesiredLRP` — the change is small and isolated.

With this flag, the driver receives:
- Create: `<disk-set-id>_0`, `<disk-set-id>_1`, etc.
- Mount: `<disk-set-id>_0` for instance 0, `<disk-set-id>_1` for instance 1

The driver decodes the suffix, uses it as the instance key, and resolves to the correct disk CID from the broker's disk set.

#### BOSH-side support

A `list-disks` Agent subcommand enables the broker and driver to discover existing disks in a set:

| Subcommand | Arguments | Description |
|---|---|---|
| `list-disks` | `--prefix <string>` | List disk CIDs matching the prefix. Returns array of `{cid, size, created_at}`. |

This allows the broker to enumerate disks in a set without maintaining a separate database, and supports garbage collection of orphaned disks.

#### Scope

Disk sets require the `InstanceIndexedVolumes` Diego change. This RFC establishes the foundation (single-disk primitives); disk sets are a follow-up RFC that builds on this foundation and proposes the Diego enhancement.


## Appendix: Alternative Architectures

This appendix explores an alternative approach — exposing disk operations via a Director HTTP API — and analyzes what would be required to integrate it with Diego volume services. This analysis informed the design choices in this RFC.

### A. Director HTTP API approach

An alternative architecture adds REST endpoints directly to the BOSH Director:

```
POST   /dynamic_disks/provide      # create + attach disk to instance
POST   /dynamic_disks/:name/detach # detach disk from instance  
DELETE /dynamic_disks/:name        # delete disk
```

Clients authenticate via UAA OAuth tokens with scopes like `bosh.dynamic_disks.update` and `bosh.dynamic_disks.delete`.

This approach has been prototyped in [community PR #1401](https://github.com/cloudfoundry/community/pull/1401) and [bosh PR #2652](https://github.com/cloudfoundry/bosh/pull/2652).

### B. Credential provisioning for Director API access

To call the Director HTTP API, clients need UAA credentials with the appropriate scopes. Two provisioning paths exist:

**Option 1: Define UAA clients in Director deployment manifest**

```yaml
# director.yml (bosh create-env)
uaa:
  clients:
    dynamic-disk-client:
      secret: ((dynamic_disk_client_secret))
      authorities: bosh.dynamic_disks.update,bosh.dynamic_disks.delete
      authorized-grant-types: client_credentials
```

The operator must then extract the generated secret and distribute it to components that need Director API access.

**Option 2: Create UAA clients out-of-band with `uaac`**

```bash
uaac target https://DIRECTOR_IP:8443 --ca-cert /path/to/ca.pem
uaac token client get uaa_admin -s UAA_ADMIN_SECRET
uaac client add dynamic-disk-client \
  --authorities bosh.dynamic_disks.update,bosh.dynamic_disks.delete \
  --authorized_grant_types client_credentials \
  --secret GENERATED_SECRET
```

Either approach requires manual credential management outside the standard BOSH deployment workflow.

### C. Diego volume services integration challenges

To integrate the Director HTTP API with Diego volume services, two components need Director API access:

| Component | Location | Credential distribution |
|---|---|---|
| Service broker | Broker VM(s) | Inject via BOSH job properties. One or few instances. Manageable. |
| Volume driver | Every Diego cell | Inject via BOSH job properties. N instances (potentially hundreds). Each cell becomes an attack surface. |

The volume driver runs on every Diego cell because Diego's volman expects drivers to be local processes listening on Unix sockets. When a container is placed on a cell, the Rep calls the local volume driver to mount the volume.

**Per-cell credential distribution creates operational and security concerns:**

1. **Credential sprawl** — UAA client credentials stored on every Diego cell
2. **Network exposure** — Every cell needs HTTPS access to the Director (typically cells only have outbound access to blob stores and NATS)
3. **Attack surface** — Compromising any cell yields Director API credentials capable of attaching/detaching disks across the deployment

### D. Centralized alternatives

Could the volume driver be centralized to avoid per-cell credentials?

**Option 1: Centralized volume driver proxy**

A single process holds Director credentials and proxies volume operations for all cells.

Problems:
- Volman discovers drivers via local Unix socket spec files — there's no built-in remote driver protocol
- Would require building a custom network protocol and modifying volman's discovery mechanism
- Single point of failure for all volume operations

**Option 2: Controller watching Diego BBS**

A controller watches Diego's BBS for DesiredLRP volume mount requests and calls the Director API centrally.

Problems:
- Must track which cell each container lands on (BBS ActualLRP state)
- Race conditions between container placement and disk attachment
- Must coordinate with Rep's mount lifecycle (Rep expects volume driver to return mountpoint synchronously)
- Deep integration with Diego internals rather than using the standard volume plugin interface

Both alternatives require significant custom integration work, whereas the standard volume driver model integrates cleanly with Diego's existing architecture.

### E. Comparison summary

| Aspect | Agent subcommands (this RFC) | Director HTTP API |
|---|---|---|
| **Credential model** | No new credentials. Agent uses existing NATS mTLS. | UAA OAuth credentials required. |
| **Cell requirements** | No changes. Agent already present. | Director API credentials + network access on every cell. |
| **Permission granularity** | Per-instance-group, declared in manifest. | Per-UAA-client. All clients with scope have equal access. |
| **Diego integration** | Standard volume driver plugin. Zero Diego changes. | Custom integration required. |
| **Broker integration** | Calls local Agent binary. | Calls Director HTTP API (straightforward). |

Both approaches share the same Director dependency for disk operations and the same failure mode: mounted disks survive Director downtime, but new operations require the Director to be available.

### F. End-to-end sequence diagram

The following diagram illustrates the complete lifecycle in a cross-deployment scenario, where the broker runs in a separate deployment (`volume-services`) with `disk.cf.create` and `disk.cf.delete` permissions, and the Diego cells run in the `cf` deployment with `disk.self.attach` and `disk.self.detach` permissions:

```mermaid
sequenceDiagram
    participant User as CF User
    participant CC as Cloud Controller
    participant Broker as Broker<br/>(volume-services deployment)
    participant Director as BOSH Director
    participant Agent_B as Agent<br/>(broker VM)
    participant Agent_C as Agent<br/>(diego-cell VM)
    participant Driver as Volume Driver<br/>(diego-cell)
    participant Rep as Diego Rep

    Note over User,Rep: 1. Service Instance Creation (disk provisioning)
    User->>CC: cf create-service bosh-disk default my-workspace
    CC->>Broker: PUT /v2/service_instances/:id
    Broker->>Agent_B: bosh-agent create-disk --size 10240 --disk-type default
    Agent_B->>Director: NATS: create-disk
    Director->>Director: Check permissions: disk.cf.create ✓
    Director->>Director: CPI create_disk
    Director-->>Agent_B: disk CID
    Agent_B-->>Broker: disk CID
    Broker-->>CC: 201 Created

    Note over User,Rep: 2. Service Binding (disk CID handoff via CC)
    User->>CC: cf bind-service my-app my-workspace
    CC->>Broker: PUT /v2/service_bindings/:id
    Broker-->>CC: volume_mounts: [{driver: "bosh-volume-driver",<br/>volume_id: "disk-CID"}]

    Note over User,Rep: 3. App Start (disk attachment + container mount)
    CC->>Rep: DesiredLRP with volume mount
    Rep->>Driver: VolumeDriver.Mount(volume_id=disk-CID)
    Driver->>Agent_C: bosh-agent attach-disk --disk-cid disk-CID
    Agent_C->>Director: NATS: attach-disk
    Director->>Director: Check permissions: disk.self.attach ✓
    Director->>Director: CPI attach_disk
    Director-->>Agent_C: device path
    Agent_C-->>Driver: device path
    Driver->>Driver: mount filesystem
    Driver-->>Rep: mountpoint path
    Rep->>Rep: bind mount into container

    Note over User,Rep: 4. App Stop (disk detachment)
    Rep->>Driver: VolumeDriver.Unmount(volume_id=disk-CID)
    Driver->>Driver: unmount filesystem
    Driver->>Agent_C: bosh-agent detach-disk --disk-cid disk-CID
    Agent_C->>Director: NATS: detach-disk
    Director->>Director: Check permissions: disk.self.detach ✓
    Director->>Director: CPI detach_disk
    Director-->>Agent_C: OK
    Agent_C-->>Driver: OK
    Driver-->>Rep: OK

    Note over User,Rep: 5. Service Instance Deletion (disk destruction)
    User->>CC: cf delete-service my-workspace
    CC->>Broker: DELETE /v2/service_instances/:id
    Broker->>Agent_B: bosh-agent delete-disk --disk-cid disk-CID
    Agent_B->>Director: NATS: delete-disk
    Director->>Director: Check permissions: disk.cf.delete ✓
    Director->>Director: CPI delete_disk
    Director-->>Agent_B: OK
    Agent_B-->>Broker: OK
    Broker-->>CC: 200 OK
```
