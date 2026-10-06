# RFC: Add Google Distributed Cloud air-gapped (GDC) BOSH CPI and Stemcell Support

## Summary
This RFC proposes adding support for **Google Distributed Cloud air-gapped (GDC)** infrastructure to the Cloud Foundry ecosystem under the **Foundational Infrastructure (FI) Working Group**.

---

## Motivation
Google and SAP are collaborating on a joint production rollout of Cloud Foundry workloads (e.g., SAP BTP) on GDC environments.

While initial development, compilation, and testing were conducted within Google's internal repositories, cross-company collaboration requires an open, shared venue. Open-sourcing the CFBOSH CPI and CI/CD orchestration, and contributing GDC stemcell support under the `cloudfoundry` organization enables SAP and other community partners to actively collaborate on code, independently compile and build releases, and deploy/lifecycle-manage workloads natively on GDC hardware.

---

## Proposal & Scope

### 1. Proposed Repositories & Components
We propose adding support for **GDC** infrastructure under the `cloudfoundry` GitHub organization through:
* **`cloudfoundry/bosh-gdc-cpi-release` (New Repository)**: Implements the BOSH CPI v2 API for GDC APIs to manage VM lifecycle, subnet and LoadBalancer attachments, multizone persistent disk provisioning/resizing, and stemcell OS image imports.
* **`cloudfoundry/bosh-linux-stemcell-builder` (Upstream Contribution)**: Rather than creating a separate stemcell repository, we will contribute GDC stemcell definitions, OS image stages, and packaging scripts directly into the existing [`cloudfoundry/bosh-linux-stemcell-builder`](https://github.com/cloudfoundry/bosh-linux-stemcell-builder) repository. This keeps GDC Linux stemcells aligned and in sync with all other Cloud Foundry infrastructure stemcells.
* **`cloudfoundry/bosh-gdc-ci` (New Repository — GDC-Specific CFBOSH CI/CD Orchestration)**: Open-sources our CFBOSH CI/CD orchestration and end-to-end test suites so that both presubmit and release pipelines can be run and co-maintained natively on GitHub Actions.

### 2. Long-Term Maintenance Plan
Maintenance and ongoing development for `cloudfoundry/bosh-gdc-cpi-release`, the GDC stemcell components in `cloudfoundry/bosh-linux-stemcell-builder`, and `cloudfoundry/bosh-gdc-ci` will follow a Google-led maintenance and ownership model, with SAP providing supporting collaboration and validation.
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

Google will serve as the Primary Maintainer, dedicating ongoing engineering resources to lead daily operations, including issue triage, pull request reviews, dependency updates, and operating, debugging, and fixing any issues in the underlying GDC Staging and GCP test infrastructure. As Co-Maintainer, SAP will collaborate on code reviews, trigger and monitor workflows via GitHub Actions, and provide validation to ensure compatibility releases align with upstream BOSH and GDC platform requirements.

### 3. CI/CD, Testing & Release Pipeline Infrastructure
Our CI/CD strategy runs natively on **GitHub Actions** across two testing levels—**Presubmit Testing** and the **Release Pipeline**—backed by Google-managed test infrastructure:

* **Presubmit Testing (Run on Every Pull Request):**
  * **Stage 1 — Static & Unit Checks:** Linting, formatting, license checks, compilation, manifest validation, and unit tests with mocks run automatically on every PR using standard GitHub Actions Linux runners in under 5 minutes without requiring external infrastructure or secrets.
  * **Stage 2 — Maintainer-Gated Component Integration Tests on GDC Staging:** To catch real GDC API and provisioning issues without deploying a full stack on every PR, presubmit tests validate changed BOSH CPI components (creating VMs, resizing multizone disks, and importing stemcell OS images) against live APIs in dedicated test namespaces on **Google's internal GDC Staging cluster**.
  * **Security & Automated Cleanup:** Scoped GDC test credentials are stored in **GitHub Actions Secrets** (with secret masking in logs). PRs opened by Google or SAP maintainers trigger integration tests automatically, while PRs from external contributors require maintainer review and approval before accessing secrets. All test VMs, disks, images, and networks are automatically deleted at the end of each test run.

* **Release Pipeline & Full E2E Qualification (Scheduled / On-Demand):**
  * **Artifact Build & Stemcell Vulnerability Scanning:** Triggered on a fixed schedule or on demand (rather than on every merge), GitHub Actions workflows build candidate CPI releases, Linux stemcells (including running a Go vulnerability scan on the stemcells), and CFBOSH deployment bundles.
  * **Full End-to-End (E2E) Qualification:** A Google-managed **Concourse cluster hosted on GKE** deploys the full CFBOSH environment targeting the **GDC Staging** environment, executes end-to-end test suites, and automatically tears down all test deployments upon completion.
  * **Artifact Publishing, Release Notes & Shared Release Pipeline Dashboard:** Once qualified, verified CPI releases, Linux stemcells, and deployment bundles are published via **GitHub Releases** to the shared public **Cloud Foundry registry**. Google and SAP will also maintain a restricted read-only CI/CD release pipeline dashboard so maintainers from both companies can monitor release status, history, and logs *(Note: We will assess the technical feasibility of a GitHub Actions-based dashboard and may select a mutually agreed alternative based on that evaluation)*.

* **Infrastructure Access & Debugging Ownership:**
  * SAP maintainers (and external contributors) will have **zero direct access** to **GDC Staging infrastructure** or to the **GCP resources** used by the presubmit integration and release pipelines.
  * SAP's visibility into test and release execution is limited to the logs surfaced in **GitHub Actions** (and the restricted read-only release pipeline dashboard).
  * In the event of any GDC Staging or GCP infrastructure errors during presubmit integration or release pipeline runs, the **Google team** will take full responsibility for debugging and fixing the issue.

* **Minimal Cloud Foundry Foundation (CFF) Infrastructure Overhead:**
  * Presubmit and build orchestration workflows use GitHub's standard Linux runners for public repositories (currently provided at no cost by GitHub; if this changes, Google will assess the impact and determine the appropriate approach).
  * Google continues to fully host, manage, and fund the **GDC Staging environment** and **production GCP infrastructure** (used for the Concourse runtime cluster hosted on GKE), so **no dedicated GDC hardware or test runtime infrastructure is required from the Cloud Foundry Foundation**.
  * Aside from standard GitHub repository/runner usage and the nominal storage cost of publishing verified artifacts to the shared public Cloud Foundry registry, this proposal introduces minimal incremental cost to the Cloud Foundry Foundation.


