# RFC: Add Google Distributed Cloud air-gapped BOSH CPI and Stemcell Builder

## Summary
This RFC proposes adding support for **Google Distributed Cloud air-gapped** infrastructure to the Cloud Foundry ecosystem under the **Foundational Infrastructure (FI) Working Group**.

---

## Motivation
Google and SAP are collaborating on a joint production rollout of Cloud Foundry workloads (e.g., SAP BTP) on Google Distributed Cloud air-gapped environments.

While initial development, compilation, and testing were conducted within Google's internal repositories, cross-company collaboration requires an open, shared venue. Open-sourcing and releasing the BOSH CPI and stemcell builder under the `cloudfoundry` organization enables SAP—and future community partners—to actively collaborate on code, independently compile and build releases, and deploy/lifecycle-manage workloads natively on Google Distributed Cloud air-gapped hardware.

---

## Proposal & Scope

### 1. Proposed Repositories & Components
We propose adding support for **Google Distributed Cloud air-gapped** infrastructure via two new repositories under the `cloudfoundry` GitHub organization:
* **`cloudfoundry/bosh-gdc-cpi-release`**: Implements the BOSH CPI v2 API for Google Distributed Cloud air-gapped KubeVirt/VM APIs to manage VM lifecycle, network attachments, and persistent disk volume provisioning.
* **`cloudfoundry/bosh-gdc-stemcell-builder`**: Builds, hardens, and packages Ubuntu-based BOSH stemcells optimized for Google Distributed Cloud air-gapped virtualization environments.

### 2. Long-Term Maintenance Plan
Maintenance and ongoing development will follow a joint co-ownership model between Google and SAP:
* **Primary Maintainer:** Google
* **Co-Maintainer & Sponsor:** SAP (`@gowrisankar22`)

#### Designated Initial Approvers & Maintainers:
* `@ajlfleos` (Google)
* `@sanjay-nagarur` (Google)
* `@dilipkumar2k6` (Google)
* `@a-hassanin` (SAP)
* `@neddp` (SAP)
* `@gowrisankar22` (SAP)

Google will serve as the Primary Maintainer, dedicating ongoing engineering resources to lead daily operations, including issue triage, pull request reviews, and dependency updates. As Co-Maintainer, SAP will provide targeted support and validation to ensure compatibility releases align with upstream BOSH and Google Distributed Cloud air-gapped platform requirements.

### 3. CI/CD & Validation Infrastructure
* **Execution Environment:** Google Distributed Cloud air-gapped has an internet-connected deployment footprint that is currently used internally to run automated build, validation, and integration tests.
* **Continuous Integration:** We will continue using this dedicated infrastructure to run automated CI/CD pipelines (Concourse / GitHub Actions), executing CPI integration test suites and stemcell verification on all pull requests and releases.
* **No Foundation Infrastructure Overhead:** Google will fully host, maintain, and provide all infrastructure, compute, and hardware resources required for CI/CD and testing at zero cost to the Cloud Foundry Foundation.

