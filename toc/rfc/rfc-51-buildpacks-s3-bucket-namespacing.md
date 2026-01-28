# Meta
[meta]: #meta
- Name: Buildpacks S3 Bucket Namespacing Strategy
- Start Date: 2026-01-09
- Author(s): @ramonskie
- Status: Accepted
- RFC Pull Request: [community#1403](https://github.com/cloudfoundry/community/pull/1403)


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

Implement proper namespacing for BOSH blobs in the buildpacks S3 bucket to improve organization, discoverability, and maintainability. The idea is to introduce folder-based namespacing per buildpack. This could be implemented using BOSH's built-in folder namespacing feature by adding a folder_name configuration to each buildpack BOSH release.
### App Runtime Interfaces
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

**Step 3: Move orphaned Blobs**

the orphaned blobs that are left would be moved to a folder named `orphaned`
we would set a retention for this for 3 months

if no one complains in the next 3 months
it would be safe to assume that we can delete these blobs

**Step 4: Update CI/CD Pipelines**

Update `buildpacks-ci` task scripts:
- Modify `tasks/cf-release/create-buildpack-dev-release/run` to use updated `config/final.yml`
- Ensure `bosh upload-blobs` respects new folder configuration
- Update any direct S3 access scripts to use new paths

**Step 5: Verification & Rollback**

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


#### Release Candidates Bucket

The `buildpack-release-candidates/` directory (1,099 files) should also be separated into its own dedicated bucket. This directory contains pre-release buildpack versions organized by buildpack type:

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

## Additional Information

- **S3 Bucket Investigation Document:** [`buildpacks-ci/S3_BUCKET_INVESTIGATION.md`](https://github.com/cloudfoundry/buildpacks-ci/blob/cf-release/S3_BUCKET_INVESTIGATION.md)
- **UUID Mapper Tool:** Located in `https://github.com/cloudfoundry/buildpacks-ci/tree/cf-release/tools/uuid-mapper` repository, maps orphaned UUIDs to BOSH release repositories
- **July 2024 Bucket Migration Context:** [buildpacks-ci commit](https://github.com/cloudfoundry/buildpacks-ci/commit/XXXXXXX) - "Switch to using buildpacks.cloudfoundry.org bucket" for CFF CDN takeover
- **BOSH `folder_name` Documentation:** [BOSH Blobstore Docs](https://bosh.io/docs/release-blobs/)
- **Related RFC:** [RFC-0011: Move Buildpack Dependencies Repository to CFF](rfc-0011-move-buildpacks-dependencies-to-cff.md)
