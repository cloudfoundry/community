# Meta
[meta]: #meta
- Name: Buildpacks S3 Bucket Namespacing Strategy
- Start Date: 2026-01-09
- Author(s): @ramonskie
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

Address the pollution and lack of proper namespacing in the `buildpacks.cloudfoundry.org` S3 bucket by implementing a structured namespacing strategy for BOSH release blobs. This RFC proposes two options: (1) implement proper namespacing within the existing shared bucket using BOSH's `folder_name` configuration, or (2) migrate to dedicated per-buildpack S3 buckets.

## Problem

The `buildpacks.cloudfoundry.org` S3 bucket currently suffers from significant organizational issues that impact maintainability, auditing, and operational efficiency:

### Current State

- **Total Files:** 34,543 files, 2.32 TB
- **UUID Files in Root:** 4,351 files (12.6% of total) with UUID naming (e.g., `29a57fe6-b667-4261-6725-124846b7bb47`)
- **No Human-Readable Names:** Blob files are stored with UUID-only names in the S3 bucket root
- **Poor Discoverability:** Impossible to identify file contents without cross-referencing BOSH release `config/blobs.yml` files
- **Orphaned Blobs:** 770 identified orphaned blobs (~91% from July 2024 CDN migration) that are not tracked in any current git repository

### Root Cause

BOSH CLI's blob storage mechanism uses content-addressable storage with UUIDs as S3 object keys:

```yaml
# config/final.yml in buildpack BOSH releases
blobstore:
  provider: s3
  options:
    bucket_name: buildpacks.cloudfoundry.org
```

When `bosh upload-blobs` runs, BOSH:
1. Generates a UUID for each blob as the S3 object key
2. Uploads the blob to S3 using only the UUID as the filename
3. Tracks the UUID-to-filename mapping in `config/blobs.yml`:

```yaml
# config/blobs.yml
java-buildpack/java-buildpack-v4.77.0.zip:
  size: 253254
  object_id: 29a57fe6-b667-4261-6725-124846b7bb47
  sha: abc123...
```

**Result:** Human-readable names exist only in git repositories; S3 contains only UUIDs.

### Impact

1. **Operational Difficulty:** Bucket browsing requires downloading and inspecting files or cross-referencing multiple git repositories
2. **Orphan Detection:** No automated way to identify unused blobs when `blobs.yml` diverges from S3
3. **Audit Challenges:** Cannot identify file types, owners, or purposes without external mappings
4. **Cost Inefficiency:** Potentially storing obsolete blobs (estimated 30-40% orphan rate in some analyses)
5. **Multi-Team Collision:** Multiple buildpack teams share the same flat namespace, increasing collision risk and confusion

### Examples of Affected Repositories

The investigation identified that UUID blobs are created by buildpack BOSH release repositories:

**Buildpack BOSH Releases (13 repositories):**
- ruby-buildpack-release
- java-buildpack-release  
- python-buildpack-release
- nodejs-buildpack-release
- go-buildpack-release
- php-buildpack-release
- dotnet-core-buildpack-release
- staticfile-buildpack-release
- binary-buildpack-release
- nginx-buildpack-release
- r-buildpack-release
- hwc-buildpack-release
- java-offline-buildpack-release

**Note:** This RFC focuses on buildpack BOSH releases only. Infrastructure BOSH releases (diego, capi, routing, garden-runc) that may also use this bucket are out of scope for this proposal.

## Proposal

Implement proper namespacing for BOSH blobs in the buildpacks S3 bucket to improve organization, discoverability, and maintainability. Two options are proposed:

### Option 1: Folder-Based Namespacing

Implement BOSH's built-in folder namespacing feature by adding `folder_name` configuration to each buildpack BOSH release.

#### Implementation

**Step 1: Update BOSH Release Configuration**

Modify `config/final.yml` in each buildpack BOSH release:

```yaml
# config/final.yml
---
blobstore:
  provider: s3
  options:
    bucket_name: buildpacks.cloudfoundry.org
    folder_name: ruby-buildpack  # Add this line with buildpack-specific name
```

**Naming Convention for `folder_name`:**
- Use the BOSH release repository name without `-release` suffix
- Examples: `ruby-buildpack`, `java-buildpack`, `nodejs-buildpack`

**Step 2: Migrate Existing Blobs**

For each buildpack BOSH release:

1. Clone the release repository and extract current blob UUIDs from `config/blobs.yml`
2. Copy each blob to its new namespaced location:
   ```bash
   # Example for ruby-buildpack
   aws s3 cp \
     s3://buildpacks.cloudfoundry.org/29a57fe6-b667-4261-6725-124846b7bb47 \
     s3://buildpacks.cloudfoundry.org/ruby-buildpack/29a57fe6-b667-4261-6725-124846b7bb47
   ```
3. Keep original files in root temporarily for rollback capability
4. After successful verification (30-day grace period), archive or delete root-level blobs

**Step 3: Update CI/CD Pipelines**

Update `buildpacks-ci` task scripts:
- Modify `tasks/cf-release/create-buildpack-dev-release/run` to use updated `config/final.yml`
- Ensure `bosh upload-blobs` respects new folder configuration
- Update any direct S3 access scripts to use new paths

**Step 4: Verification & Rollback**

- Test blob access with updated configuration in staging/dev environments
- Monitor BOSH release builds for 30 days
- Keep original root-level blobs for rollback during grace period
- After successful verification, move root-level blobs to archive or delete

#### Pros

- ✅ **Native BOSH Support:** Uses built-in BOSH functionality, no custom tooling required
- ✅ **Minimal Infrastructure Change:** Same bucket, same permissions, same CDN
- ✅ **Clear Ownership:** Each folder represents one buildpack team's blobs
- ✅ **Backward Compatible:** Existing root-level blobs remain accessible during migration
- ✅ **Cost Effective:** No new infrastructure costs
- ✅ **Preserves BOSH Design:** Maintains content-addressable storage benefits (deduplication, immutability)
- ✅ **Easy Browsing:** S3 console shows organized folder structure
- ✅ **Orphan Detection:** Easier to identify unused blobs per buildpack

#### Cons

- ❌ **Shared Bucket Limitations:** Still requires coordination between teams for bucket policies
- ❌ **Breaking Change Potential:** May impact consumers if not carefully coordinated
- ❌ **Migration Effort:** Requires updating 13+ buildpack releases
- ❌ **Blob Duplication:** Existing blobs must be copied (not moved) during grace period, temporarily doubling storage
- ❌ **Multi-Repo Coordination:** Changes must be synchronized across multiple repositories
- ❌ **No Per-Team Access Control:** Cannot implement IAM policies for individual buildpack teams within shared bucket

### Option 2: Dedicated S3 Buckets Per Buildpack

Create separate S3 buckets for each buildpack BOSH release.

#### Implementation

**Step 1: Create S3 Buckets**

Create one bucket per buildpack with naming convention:
```
buildpacks-{buildpack-name}.cloudfoundry.org
```

Examples:
- `buildpacks-ruby.cloudfoundry.org`
- `buildpacks-java.cloudfoundry.org`
- `buildpacks-nodejs.cloudfoundry.org`

**Step 2: Update BOSH Release Configuration**

```yaml
# config/final.yml for ruby-buildpack-release
---
blobstore:
  provider: s3
  options:
    bucket_name: buildpacks-ruby.cloudfoundry.org
```

**Step 3: Migrate Blobs**

For each buildpack:
1. Identify all blobs from `config/blobs.yml`
2. Copy blobs to new dedicated bucket
3. Update `config/final.yml` with new bucket name
4. Test release builds
5. Keep old bucket accessible for rollback period

**Step 4: Update DNS**

- Configure DNS for new subdomains
- Point buildpack consumers to new bucket URLs (if any direct access exists)
- Update documentation

#### Pros

- ✅ **Complete Team Isolation:** Each buildpack team has full control over their bucket
- ✅ **Granular IAM Policies:** Per-team access control via AWS IAM
- ✅ **Independent Lifecycle Management:** Teams can set their own retention policies
- ✅ **Reduced Blast Radius:** Issues with one bucket don't affect others
- ✅ **Clear Cost Attribution:** Track S3 costs per buildpack
- ✅ **No Namespace Collisions:** Impossible for teams to interfere with each other

#### Cons

- ❌ **High Infrastructure Overhead:** 13+ new S3 buckets to manage
- ❌ **Increased DNS Complexity:** Requires multiple DNS entries
- ❌ **Operational Burden:** More resources to monitor, maintain, and secure
- ❌ **Higher AWS Costs:** Multiple S3 buckets incur additional request and monitoring overhead (~$20/month additional)
- ❌ **Breaking Change Potential:** May impact consumers if not carefully coordinated
- ❌ **Significant Migration Effort:** Larger coordination effort across teams and AWS resources

#### Additional Consideration: Release Candidates Bucket

The `buildpack-release-candidates/` directory (1,099 files) could also be separated into its own dedicated bucket under Option 2. This directory contains pre-release buildpack versions organized by buildpack type:

```
buildpack-release-candidates/
├── apt/
├── binary/
├── dotnet-core/
├── go/
├── java/
├── nodejs/
├── php/
├── python/
├── ruby/
└── staticfile/
```

**Creating a separate bucket for release candidates would provide:**
- ✅ **Clear Lifecycle Separation:** Development artifacts isolated from production blobs
- ✅ **Independent Retention Policies:** Apply aggressive cleanup rules (e.g., 180-day expiration) without affecting production
- ✅ **Reduced Production Bucket Clutter:** Keep production bucket focused on finalized BOSH blobs
- ✅ **Simplified Access Control:** CI/CD systems can have different permissions for release candidates vs. production blobs

**Example bucket structure:**
```
buildpacks.cloudfoundry.org            # Production BOSH blobs only
buildpacks-candidates.cloudfoundry.org # Pre-release buildpack packages
```

**Note:** This separation is **compatible with both Option 1 and Option 2**:
- **With Option 1:** Release candidates bucket + shared production bucket with folder namespacing
- **With Option 2:** Release candidates bucket + per-buildpack production buckets

The release candidates bucket would **not** require BOSH configuration changes, as these files are uploaded directly by CI/CD pipelines (`buildpacks-ci`), not via `bosh upload-blobs`.

## Comparison

| Aspect | Option 1: Folder Namespacing | Option 2: Dedicated Buckets |
|--------|------------------------------|----------------------------|
| **Infrastructure Changes** | Minimal (config only) | Major (13 buckets + DNS) |
| **Migration Complexity** | Medium | High |
| **Operational Overhead** | Low | High |
| **Team Isolation** | Logical (folders) | Physical (buckets) |
| **Access Control Granularity** | Bucket-level | Bucket-level per team |
| **Cost Impact** | ~$5-10/month temporary (migration grace period) | +~$20/month ongoing (request & monitoring overhead) |
| **Rollback Ease** | Easy (keep old files) | Difficult (multiple resources) |
| **BOSH Native Support** | ✅ Yes (`folder_name`) | ✅ Yes (`bucket_name`) |
| **Orphan Detection** | Easier (per folder) | Easiest (per bucket) |
| **Breaking Changes Risk** | Low | Medium-High |

## Cost Analysis

### Current State (Shared Bucket)
- **Storage:** ~2.32 TB = ~$53/month (at $0.023/GB S3 Standard)
- **Data Transfer OUT:** ~500 GB/month = ~$45/month (at $0.09/GB)
- **S3 Requests:** ~$0.50/month
- **Total:** ~$98.50/month

### Option 1: Folder Namespacing

**Migration Period (30 days):**
- Temporary blob duplication during grace period
- Additional storage: ~$5-10/month for 30 days
- **Migration cost:** ~$5-10 (one-time)

**Steady State:**
- Same storage structure (folders within 1 bucket)
- Same request costs
- Cleanup of orphaned blobs: **-$6/month savings**
- **Total: ~$92/month** (6% reduction)

### Option 2: Dedicated Buckets Per Buildpack

**Infrastructure:**
- 13 buildpack buckets
- 1 optional release candidates bucket
- **Total: 14 S3 buckets**

**Monthly Costs:**
- **Storage:** ~$53/month (same, just distributed)
- **Data Transfer OUT:** ~$45/month (same)
- **Additional S3 Request Overhead:** 14 buckets × $0.50 = **+$7/month**
- **CloudWatch Monitoring:** 14 buckets × $0.30 = **+$4.20/month**
- **Additional DNS/Certificate Management:** ~$1/month
- **Total: ~$110/month** (~12% increase)

**Cost Comparison:**
- **Option 1:** $92/month (after cleanup)
- **Option 2:** $110/month
- **Difference:** +$18/month (~+$216/year) for Option 2

**Note:** This analysis assumes **no CDN** (CloudFront) is used. If CloudFront distributions were added per bucket, costs would increase by an additional $50-100/month for Option 2.

## Recommendation

**Option 1 (Folder-Based Namespacing) is recommended** for the following reasons:

1. **Lower Risk:** Minimal infrastructure changes reduce deployment and rollback complexity
2. **Cost Effective:** Avoids recurring per-bucket overhead costs (+$18/month savings vs Option 2)
3. **Native Support:** Uses existing BOSH functionality without custom tooling
4. **Faster Implementation:** Can be rolled out incrementally per buildpack over ~16 weeks
5. **Preserves Existing Architecture:** Maintains current DNS and access patterns
6. **Sufficient for Buildpacks:** Logical separation via folders meets organizational needs for buildpack teams

Option 2 should be considered only if:
- Per-team IAM access control is a hard requirement
- Budget allows for increased AWS costs (+$216/year)
- Physical bucket isolation is mandated by security/compliance requirements

## Implementation Plan

Assuming **Option 1** is adopted:

### Phase 1: Preparation (Week 1-2)
- [ ] Finalize `folder_name` naming convention
- [ ] Create migration scripts for blob copying
- [ ] Document rollback procedures
- [ ] Identify all buildpack BOSH releases using the shared bucket (13 buildpacks)
- [ ] **Decision:** Determine whether to create separate `buildpacks-candidates.cloudfoundry.org` bucket for release candidates

### Phase 2: Pilot Migration (Week 3-4)
- [ ] Select 1-2 pilot buildpacks (e.g., `staticfile-buildpack-release`, `binary-buildpack-release` - lower risk)
- [ ] Update `config/final.yml` with `folder_name`
- [ ] Copy pilot buildpack blobs to new folder structure
- [ ] Test BOSH release builds in CI
- [ ] Monitor for 2 weeks

### Phase 3: Rollout (Week 5-10)
- [ ] Roll out to remaining buildpack BOSH releases (3-4 buildpacks per week)
- [ ] Update CI/CD pipelines to use new configuration
- [ ] Verify each buildpack's release process post-migration
- [ ] Document per-buildpack migration status

### Phase 4: Cleanup (Week 11-13)
- [ ] Generate final orphan blob report
- [ ] Archive July 2024 migration artifacts (702 blobs, ~250 GB) to S3 Glacier Deep Archive
- [ ] After 30-day grace period, remove root-level blobs that are successfully migrated
- [ ] Document final bucket organization in buildpacks-ci repository

### Phase 5: Automation (Week 14-16)
- [ ] Implement automated orphan detection (monthly scan)
- [ ] Add S3 lifecycle policies for temporary CI artifacts
- [ ] Set up CloudWatch alarms for bucket size anomalies
- [ ] Create runbook for future blob management

## Estimated Impact

### Storage Cost Savings (Post-Migration)
- **Orphaned Blob Cleanup:** Remove/archive 770 orphaned blobs (~270 GB)
  - Move July 2024 migration artifacts (250 GB) to Deep Archive: $0.25/month (from $5.75/month)
  - Delete truly orphaned blobs (20 GB): $0.46/month savings
- **Total Monthly Savings:** ~$5.50/month
- **Annual Savings:** ~$66/year

### Operational Benefits
- **Improved Discoverability:** Engineers can browse blobs by buildpack in S3 console
- **Faster Audits:** Clear ownership boundaries speed up security/compliance reviews
- **Easier Debugging:** Quickly identify which buildpack owns a blob
- **Reduced Onboarding Time:** New team members understand bucket organization intuitively
- **Better Orphan Detection:** Automated scripts can detect unused blobs per buildpack folder

## Additional Information

- **S3 Bucket Investigation Document:** [`buildpacks-ci/S3_BUCKET_INVESTIGATION.md`](https://github.com/cloudfoundry/buildpacks-ci/blob/cf-release/S3_BUCKET_INVESTIGATION.md)
- **UUID Mapper Tool:** Located in `https://github.com/cloudfoundry/buildpacks-ci/tree/cf-release/tools/uuid-mapper` repository, maps orphaned UUIDs to BOSH release repositories
- **July 2024 Bucket Migration Context:** [buildpacks-ci commit](https://github.com/cloudfoundry/buildpacks-ci/commit/XXXXXXX) - "Switch to using buildpacks.cloudfoundry.org bucket" for CFF CDN takeover
- **BOSH `folder_name` Documentation:** [BOSH Blobstore Docs](https://bosh.io/docs/release-blobs/)
- **Related RFC:** [RFC-0011: Move Buildpack Dependencies Repository to CFF](rfc-0011-move-buildpacks-dependencies-to-cff.md)

## Open Questions

1. **Who owns migration execution?** Should this be Application Runtime Interfaces WG or joint ownership with other teams?
2. **Budget approval:** Does the CFF budget accommodate temporary storage cost increase during migration grace period (~$5-10/month for 30 days)?
3. **Access control requirements:** Are there any per-team IAM access control requirements that would necessitate Option 2?
4. **Release candidates bucket separation:** Should the `buildpack-release-candidates/` directory (1,099 files) be moved to a dedicated `buildpacks-candidates.cloudfoundry.org` bucket to enable independent lifecycle management and cleanup policies?
