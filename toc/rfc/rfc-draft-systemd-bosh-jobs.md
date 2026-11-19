# Meta
[meta]: #meta
- Name: Support BOSH Jobs Managed by systemd Without Monit
- Start Date: 2026-11-13
- Author(s): @mkocher
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1706
- Related RFCs: (none)
- Affected Component(s): bosh-agent, bosh (director), bosh-cli, bpm-release, bosh-linux-stemcell-builder


## Summary

Add a first-class way for BOSH jobs to be supervised by systemd instead of monit. Release authors opt a job in by versioning its job spec and declaring BPM as its supervisor; process definitions stay in the job's existing `bpm.yml`. The BOSH agent generates the systemd configuration, and BPM continues to provide process isolation. Monit-managed and systemd-managed jobs coexist on the same VM, so releases can migrate one job at a time. Monit is deprecated when this reaches GA and removed in a later major stemcell line.

## Problem

Monit is the process supervisor for every BOSH-deployed job. It has several problems:

**1. Monit is frozen on an old version due to a license change.**
BOSH stemcells ship monit **5.2.5**, released in March 2011. The current monit version is **5.35.2**. After 5.2.5, monit relicensed to AGPL-3+, which is incompatible with the Apache 2.0 license used by BOSH. The community cannot upgrade without a license exception. [This has been a known blocker since at least 2018.](https://github.com/cloudfoundry/bosh/issues/1295) We are permanently stuck on a 14-year-old process supervisor.

**1. We have already adopted systemd elsewhere in the BOSH stack.**
The BOSH agent itself moved to systemd (replacing runit) when the Noble stemcell was introduced. systemd is the standard process supervisor on every Linux distribution BOSH targets. Continuing to run a separate, frozen process supervisor alongside systemd creates unnecessary complexity.

**1. For jobs that already use BPM, the monit file is pure boilerplate.**
The vast majority of CF BOSH jobs use BPM for process isolation. Their monit files are identical copies of the same template:
```
check process <name>
  with pidfile /var/vcap/sys/run/bpm/<name>/<name>.pid
  start program "/var/vcap/jobs/bpm/bin/bpm start <name>"
  stop program "/var/vcap/jobs/bpm/bin/bpm stop <name>"
  group vcap
```

## Proposal

Release authors opt a job into systemd supervision in its job spec. The job keeps its existing `bpm.yml`; no new process-definition file is introduced. Jobs that don't opt in continue to use monit unchanged.

BPM is required for the systemd path. Release authors don't need to learn anything about systemd.

### Versioned Job Spec

The job `spec` gains two fields:

```yaml
# jobs/cloud_controller_ng/spec
name: cloud_controller_ng
spec_version: "2.0"
supervisor: bpm        # the default for spec_version >= 2; may be omitted
templates:
  bpm.yml.erb: config/bpm.yml
  cloud_controller_ng.yml.erb: config/cloud_controller_ng.yml
```

**`spec_version`** declares which job spec format the job uses. A spec without it is version 1, today's format, and behaves exactly as today. Future minor versions can add features; BOSH components reject a job whose spec version is newer than they understand, rather than silently ignoring what they don't support.

**`supervisor`** declares how the job's processes are run:

| Value | Meaning |
| --- | --- |
| `monit` | Today's behavior, and the default for version 1 specs. |
| `bpm` | The processes in `bpm.yml` are supervised by BOSH through BPM, without monit. The default for version 2 specs. |
| `none` | The job has nothing to supervise, such as errands and utility jobs. |

systemd is an implementation detail and is not part of the job spec.

The supervisor is chosen per job by the release author; there is no deployment-level toggle. Problems such as a `supervisor: bpm` job with no `bpm.yml` are caught when the release is uploaded.

### How Jobs Run

For `supervisor: bpm` jobs, the agent generates a systemd service for each process in `bpm.yml`. Each service runs the process through BPM, and systemd restarts it if it exits, matching monit's behavior. The services are created fresh on every boot, so nothing starts before the agent has prepared the VM, and restarting the agent does not restart healthy workloads.

BPM is updated so that its foreground mode (`bpm run`) is suitable for use under systemd. A BPM version deployed with the job continues to take precedence over the one on the stemcell; if that BPM is too old to support this mode, the job fails with a clear error rather than falling back to monit.

### Coexistence and Compatibility

Monit and systemd jobs can run side by side on the same VM, and a single process is never supervised by both.

- Jobs with a version 1 spec, or `supervisor: monit`, keep using monit everywhere.
- Older Directors, agents and stemcells don't understand the new fields. Releases that need to stay deployable on them can keep their monit files alongside `supervisor: bpm`; older platforms use monit, and newer ones use systemd and ignore the monit file.
- A job with no monit file requires a new enough Director, agent and stemcell. On a platform that can't run it, the deploy fails with a clear error.

### Health Checks

Monit supports restarting a service when a health check fails. Rather than building health-check logic into the supervisor, jobs bring their own health checks as ordinary processes. Any process in `bpm.yml` can declare that when it exits, other processes in the same job should be restarted:

```yaml
# config/bpm.yml
processes:
- name: cloud_controller_ng
  executable: /var/vcap/packages/cloud_controller_ng/bin/cloud_controller_ng
- name: cc_healthchecker
  executable: /var/vcap/packages/cc_healthchecker/bin/healthchecker
  restarts_on_exit:
  - cloud_controller_ng
```

When `cc_healthchecker` exits, `cloud_controller_ng` is restarted. This design:

- Lets release authors write whatever health check logic they need in their process binary.
- Allows health check processes to be packaged and shared across jobs (the same pattern as healthchecker-release).
- Does not require any changes to the process being monitored — the main process is unaware of the health check.

Restarts triggered this way don't happen while BOSH is intentionally stopping the job, and are rate-limited so a failing health check can't restart the main process in a tight loop.

### Lifecycle Hooks on VM Reboot

Today, `pre-start` and `post-start` only run during Director-orchestrated deployments. When a VM reboots without Director involvement, monit immediately starts all jobs, and neither hook runs. This is a long-standing gap in BOSH semantics.

For jobs with a version 2 spec, the agent runs both hooks when the VM reboots, with the same ordering guarantees as a deploy:

1. All `pre-start` scripts finish before any job starts.
2. All jobs are running before any `post-start` script begins.

As in a deploy, if a `pre-start` fails, the jobs are not started, and the failure is reported through the Health Monitor. Hooks are not rerun when only the agent restarts, and jobs that were deliberately stopped stay stopped.

Hooks already run on every deploy, so they are expected to be idempotent; this RFC makes that expectation explicit for reboots too. Jobs with a version 1 spec keep today's reboot behavior.

### What Is Not In Scope

**Raw systemd unit templates**: This RFC does not let release authors write systemd units directly. Jobs always run through BPM, which leads to more secure BOSH releases and avoids exposing the entire supervisor surface to release authors. A future spec version could add this if a real need arises.

**Older stemcell lines**: The systemd path targets the Resolute stemcell first. Supporting older stemcell lines is optional later work.

**Windows**: Windows stemcells are unaffected.

### Monit Deprecation and Removal

Monit is deprecated when the systemd path reaches GA and removed in a later major stemcell line. The timeline will be announced at GA so release authors have time to migrate. Until removal, monit continues to work for every job that uses it today.

## Migration Path for Release Authors

For an existing BPM-managed job:

1. Add `spec_version: "2.0"` and `supervisor: bpm` to the job spec. Mark errands and utility jobs `supervisor: none`.
2. Make sure `pre-start` and `post-start` scripts are safe to run on reboot.
3. Replace monit-based health checks with health-check processes using `restarts_on_exit`.
4. Cut a new release.

Keep the monit file while the release must support older platforms, and remove it once it doesn't.

## Workstreams

- **bosh-agent**: generate and manage systemd services alongside monit, run lifecycle hooks on reboot, and support `restarts_on_exit`.
- **bpm-release**: make `bpm run` suitable for supervision by systemd.
- **bosh (Director)**: understand the new job spec fields, accept jobs without monit files, and pass the supervisor choice to the agent.
- **bosh-cli**: the same job spec support for `create-release` and `create-env`.
- **bosh-linux-stemcell-builder**: ship what the systemd path needs in the Resolute stemcell.
- **Release authors**: migrate jobs as described above, when ready.

## Hat Tip

This RFC borrows heavily from @jpalermo's [original proposal](https://github.com/cloudfoundry/bosh-linux-stemcell-builder/discussions/338).
