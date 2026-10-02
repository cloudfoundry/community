# Meta
[meta]: #meta
- Name: Cloud Foundry Documentation Modernization
- Start Date: 2026-10-01
- Author(s): @johha @ZPascal @Dominik23
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1642
- Affected Component(s): CF Documentation, all Working Groups maintaining documentation


## Summary

This RFC proposes migrating the Cloud Foundry documentation (CF, UAA API) from its current Ruby/ERB-based HTML build system to a modern, Markdown-first documentation toolchain (Docusaurus or equivalent), hosted on GitHub Pages. The goal is to lower the barrier to contribution, re-enable full-text search, reduce hosting costs, and give the community full ownership and visibility into the documentation pipeline.

## Problem

The current CF documentation system has several issues that have accumulated over time:

- **Authoring friction:** Documentation is written and maintained using ERB/Ruby templates and a custom HTML pipeline. This is a significant barrier for contributors who are not familiar with the toolchain. Most modern open-source projects use plain Markdown, which is universally understood.
- **No feedback loop:** Contributors have no easy way to preview generated documentation locally without setting up a complex environment. Feedback on rendered output is slow and indirect.
- **Search is broken or disabled:** Full-text search across the docs is either absent or degraded, harming user experience and discoverability.
- **Poor SEO and AI-agent compatibility:** The current setup is not optimized for search engine indexing or consumption by AI-based developer tools (e.g., MCP servers, LLM context windows, Copilot).
- **Versioning is unclear:** There is no well-defined versioning model for documentation, making it difficult to track what applies to which CF release.
- **Hosting costs and access:** The current hosting solution involves infrastructure managed outside the community GitHub organization, leading to cost, access, and governance concerns.
- **Unclear contributor scope:** It is unclear which repositories contribute to the public-facing CF docs, and which teams are actively maintaining them.

## Proposal

### 1. Migrate to Markdown and a Modern Documentation Engine

The CF documentation SHOULD be rewritten in plain Markdown and managed via a modern static site generator. The recommended engine is Docusaurus (maintained by Meta, MIT-licensed, widely adopted in the CNCF ecosystem), though other frameworks such as Hugo or MkDocs MAY be evaluated and proposed as alternatives during the PoC phase.

Key capabilities the chosen framework MUST provide:

- Markdown-based authoring (no custom templating languages required)
- Built-in full-text search (e.g., via Algolia DocSearch or lunr.js)
- Versioned documentation support tied to CF release cycles
- Local development server (`npm start` or equivalent one-liner)
- A lightweight templating/component system that does not require Ruby or ERB
- SEO-friendly HTML output (structured metadata, canonical URLs, sitemap)
- AI-agent compatibility: clean, crawlable HTML and optionally an LLM-friendly `/llms.txt` index

The migration SHOULD use a phased approach (see [Phases](#phases)) and MUST NOT break the existing canonical `docs.cloudfoundry.org` URL during transition.

### 2. Deployment: GitHub Pages with Full Community Access

The documentation site MUST be deployed to GitHub Pages under the `cloudfoundry` GitHub organization. This achieves the following:

- **Zero hosting cost** for a static site within GitHub's free tier.
- **Full community visibility:** deployment is driven by a GitHub Actions workflow in a public repository that any approved contributor can inspect and trigger.
- **Access model mirrors existing patterns:** the repository access model SHOULD follow the same GitHub Teams / CODEOWNERS pattern established for Concourse and other CF org repositories (see RFC-0014), granting Working Group approvers the ability to merge documentation PRs without requiring CFF staff involvement.

#### Domain Handling

- The existing domain `docs.cloudfoundry.org` MUST remain functional during and after migration.
- During transition, a redirect or reverse-proxy MAY be used to serve the new site while the DNS record is updated.
- After the new site is stable, the DNS CNAME SHOULD be updated to point to the GitHub Pages endpoint (`cloudfoundry.github.io/docs` or equivalent).
- Old deep-link URLs MUST be handled via Docusaurus redirect configuration to avoid broken links in external content.

### 3. Contribution Workflow and PR Automation

To sustain documentation quality without overburdening maintainers, the following SHOULD be adopted:

- A `CODEOWNERS` file in the docs repository assigns each section to the responsible Working Group, mirroring the pattern used in the community repo.
- Pull requests for a given section automatically request review from the relevant Working Group approvers.
- A GitHub Actions CI pipeline validates Markdown linting, broken links, and (if applicable) spell-checking on every PR.
- Draft PRs are encouraged for early-stage work to enable async feedback before finalization.

### 4. Versioning Strategy

Documentation versioning is intended to be tied to CF Deployment release branches. In the initial implementation (PoC / Version 1), this mapping is not yet implemented; a versioning structure MAY already be present, but without an active connection to specific CF-Deployment releases.

The concrete approach — including how many versions are tracked, how prior versions are retained, and how breaking changes are published and their history tracked — is to be further defined in Version 2, following the migration, based on experience gathered from Version 1.

### 5. Extension and Customization

The chosen framework SHOULD support a plugin or extension mechanism so that Working Groups can add custom components (e.g., interactive CLI examples, version-specific callouts) without forking the core tooling. Docusaurus MDX support covers this use case. Custom extensions MUST be documented and reviewed to avoid introducing new maintenance burdens.

### Phases

#### Phase 1: Discovery and Stakeholder Alignment (Prerequisite)

Before any technical work begins, the following organizational questions MUST be answered:

- **Identify all doc repositories:** Produce a definitive list of all GitHub repositories that contribute content to the public-facing CF documentation. This SHOULD be led by the TOC with input from all Working Groups.
- **Survey existing consumers:** Working Group leads and known downstream consumers (e.g., SAP BTP, VMware Tanzu, anynines, …) SHOULD be asked whether they consume the CF docs as-is or maintain their own derivative documentation. This informs migration scope and backward-compatibility requirements.
- **Clarify ownership:** Each documentation section MUST have a named Working Group owner before migration begins.

#### Phase 2: Proof of Concept

A PoC SHOULD be established in a new repository (e.g., `cloudfoundry/docs-next`) to:

- Stand up Docusaurus (or the chosen alternative) with a representative subset of CF documentation migrated to Markdown.
- Validate local development experience, search, and versioning.
- Test GitHub Pages deployment via GitHub Actions.
- Validate the domain redirect strategy.
- Gather feedback from at least three active CF documentation contributors.

The results of the PoC SHOULD be presented in a TOC / Docs WG meeting.

#### Phase 3: Full Migration

Based on PoC findings, all documentation content SHOULD be migrated to Markdown. A migration script MAY be developed to automate conversion of the ERB/HTML source to Markdown, with a manual review pass per section. A full migration timeline MUST be published and agreed upon by all affected Working Groups before this phase begins.

#### Phase 4: Cutover and Decommission

- The new site goes live at `docs.cloudfoundry.org`.
- The old build system is archived (not deleted) for historical reference.
- Redirect rules ensure all old URLs resolve correctly.
- The old hosting infrastructure is decommissioned after a defined stabilization window (suggested: 90 days).

### Suggested Timeline

- **Phase 1 (Discovery):** October – November 2026 — stakeholder survey completed, repository inventory published
- **Phase 2 (PoC):** November – December 2026 — working Docusaurus site with representative content, deployed to GitHub Pages
- **Phase 3 (Full Migration):** Q1 2027 — all content migrated, CODEOWNERS in place, CI pipeline live
- **Phase 4 (Cutover):** Q2 2027 — `docs.cloudfoundry.org` DNS switched, old infrastructure decommissioned

## Impact and Consequences

### Positive

- **Lower contribution barrier:** Any developer familiar with Markdown and GitHub can contribute documentation without learning a proprietary toolchain.
- **Re-enabled search:** Full-text search improves discoverability for users and reduces support load.
- **Cost reduction:** GitHub Pages hosting eliminates ongoing infrastructure costs.
- **Community ownership:** The community can fully self-serve on documentation deployment without depending on CFF staff.
- **AI and SEO readiness:** Modern static site output is well-suited for search engine indexing and AI developer tools.
- **Versioning:** Documentation versions tied to releases reduce confusion about what applies to which CF version. This is planned for Version 2, scheduled after the migration.

### Negative / Risks

- **Migration effort:** Converting ERB/HTML to Markdown at scale requires significant up-front work from Working Groups. If stakeholder bandwidth is insufficient, the migration may stall.
- **Link rot:** If redirect handling is incomplete, existing documentation links in blog posts, books, and third-party sites will break.
- **JavaScript dependency:** Docusaurus requires Node.js. Contributors who currently work without a JavaScript toolchain will need to install it. A Docker-based development option SHOULD be provided as an alternative.
- **Review bottleneck:** Increased contributor access may increase PR volume. CODEOWNERS automation mitigates but does not eliminate this risk.

## Open Questions

- Which repositories currently feed into the public CF docs, and which Working Groups own them? (Must be answered in Phase 1.)
- Do downstream distributions (SAP, VMware Tanzu) consume the raw source or the rendered HTML? Would migrating to Markdown require changes on their end?
- Should versioned docs be maintained in the same repository as the main branch (Docusaurus model) or in separate release branches?
- Is Algolia DocSearch (free for open-source projects) the preferred search backend, or should a self-hosted option (e.g., Pagefind, lunr.js) be used?
- What is the target timeline for Phase 1 discovery, and what is the target timeline for each subsequent phase (see [Suggested Timeline](#suggested-timeline))?
- Who will own the Phase 1 stakeholder survey and drive the overall timeline?
- Should an `llms.txt` or similar AI-discovery file be published alongside the new docs site?
- Who will do the migration?
- Who will support the technical aspects of the new implementation?
- Who can we involve to vet this proposal for the UAA API docs and the CredHub API docs?
