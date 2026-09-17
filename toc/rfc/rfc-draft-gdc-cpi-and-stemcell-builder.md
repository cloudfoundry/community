# RFC: Add Google Distributed Cloud air-gapped BOSH CPI and Stemcell Support

## Summary
This RFC proposes adding support for **Google Distributed Cloud air-gapped** infrastructure to the Cloud Foundry ecosystem under the **Foundational Infrastructure (FI) Working Group**.

---

## Motivation
Google and SAP are collaborating on a joint production rollout of Cloud Foundry workloads (e.g., SAP BTP) on Google Distributed Cloud air-gapped environments.

While initial development, compilation, and testing were conducted within Google's internal repositories, cross-company collaboration requires an open, shared venue. Open-sourcing the BOSH CPI and contributing Google Distributed Cloud air-gapped stemcell support under the `cloudfoundry` organization enables SAP—and future community partners—to actively collaborate on code, independently compile and build releases, and deploy/lifecycle-manage workloads natively on Google Distributed Cloud air-gapped hardware.

---

## Proposal & Scope

### 1. Proposed Repositories & Components
We propose adding support for **Google Distributed Cloud air-gapped** infrastructure under the `cloudfoundry` GitHub organization through:
* **`cloudfoundry/bosh-gdc-cpi-release` (New Repository)**: Implements the BOSH CPI v2 API for Google Distributed Cloud air-gapped KubeVirt/VM APIs to manage VM lifecycle, network attachments, and persistent disk volume provisioning.
* **`cloudfoundry/bosh-linux-stemcell-builder` (Upstream Contribution)**: Rather than creating a separate stemcell repository, we will contribute Google Distributed Cloud air-gapped stemcell definitions, OS image stages, and packaging scripts directly into the existing [`cloudfoundry/bosh-linux-stemcell-builder`](https://github.com/cloudfoundry/bosh-linux-stemcell-builder) repository. This keeps Google Distributed Cloud Linux stemcells aligned and in sync with all other Cloud Foundry infrastructure stemcells.

### 2. Long-Term Maintenance Plan
Maintenance and ongoing development for `cloudfoundry/bosh-gdc-cpi-release` and the GDC stemcell components in `cloudfoundry/bosh-linux-stemcell-builder` will follow a joint co-ownership model between Google and SAP:
* **Primary Maintainer:** Google
* **Co-Maintainer & Sponsor:** SAP (`@gowrisankar22`)

#### Designated Initial Approvers & Maintainers:
* `@ajlfleos` (Google)
* `@sanjay-nagarur` (Google)
* `@dilipkumar2k6` (Google)
* `@a-hassanin` (SAP)
* `@neddp` (SAP)
* `@gowrisankar22` (SAP)
* `@Ivaylogi98` (SAP)

Google will serve as the Primary Maintainer, dedicating ongoing engineering resources to lead daily operations, including issue triage, pull request reviews, and dependency updates. As Co-Maintainer, SAP will provide targeted support and validation to ensure compatibility releases align with upstream BOSH and Google Distributed Cloud air-gapped platform requirements.

### 3. CI/CD & Testing Infrastructure
* **Test Scope:** `cloudfoundry/bosh-gdc-cpi-release` and the GDC stemcell additions will contain unit tests, static analysis, and packaging validation (using mocked interfaces). They do not include live integration test suites requiring access to Google Distributed Cloud environments.
* **Continuous Integration:** Automated CI pipelines (e.g., GitHub Actions) will run unit tests, linting, and release builds on standard CI runners for all pull requests and releases.
* **No Foundation Infrastructure Overhead:** Because testing is limited to unit tests running on standard runners, no dedicated Google Distributed Cloud hardware or infrastructure is required, incurring zero infrastructure or compute cost for both Google and the Cloud Foundry Foundation.

