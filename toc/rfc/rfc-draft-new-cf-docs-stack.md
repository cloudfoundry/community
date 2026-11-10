# Meta
[meta]: #meta
- Name: Cloud Foundry Documentation Modernization
- Start Date: 2026-10-01
- Author(s): @johha @ZPascal @Dominik23
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1642
- Affected Component(s): CF Documentation, all Working Groups maintaining documentation


## Summary

This RFC proposes migrating the Cloud Foundry documentation (CF, UAA API) from the current Ruby/ERB HTML build system to a Markdown-first toolchain hosted on GitHub Pages. The goals are to lower the contribution barrier, re-enable full-text search, cut hosting costs, and give the community full ownership of the documentation pipeline. Two independent proofs of concept already demonstrate the approach (see [Proof of Concept](#proof-of-concept)).

## Problem

The current CF documentation system has accumulated several issues:

- **Authoring friction:** Docs are written in ERB/Ruby templates and a custom HTML pipeline — a significant barrier for contributors unfamiliar with the toolchain. Most modern projects use plain Markdown.
- **No feedback loop:** There is no easy way to preview rendered docs locally without a complex environment.
- **Search is broken or disabled:** Full-text search is absent or degraded, harming discoverability.
- **Poor SEO and AI-agent compatibility:** The output is not optimized for search-engine indexing or consumption by AI developer tools.
- **Versioning is unclear:** There is no defined model for tracking what applies to which CF release.
- **Hosting costs and access:** Publishing depends on infrastructure outside the community GitHub organization, raising cost, access, and governance concerns.
- **Unclear contributor scope:** It is unclear which repositories feed the public docs and which teams maintain them.
- **Working Groups not informed of doc changes:** Cross-WG contributors already commit to the docs repos today, but there is no mechanism to notify the relevant WG when their area changes.

## Proposal

### 1. Migrate to Markdown and Docusaurus

The CF documentation SHOULD be rewritten in plain Markdown and managed by **Docusaurus** (current major version, v3 or newer — maintained by Meta, MIT-licensed, widely adopted in the CNCF ecosystem). Docusaurus is the recommended engine for this migration; the PoC confirms the choice and MAY propose an alternative only if a hard requirement cannot be met (see [Phase 2](#phase-2-proof-of-concept)). Docusaurus uses MDX for templating and reusable components, replacing the ERB templating. A working proof of concept already demonstrates the approach end to end (see [Proof of Concept](#proof-of-concept)).

Docusaurus provides the capabilities the new stack requires:

- Markdown/MDX authoring with no custom templating language
- Built-in full-text search (e.g., Algolia DocSearch or a self-hosted option such as Pagefind or lunr.js)
- Versioned documentation support tied to CF release cycles
- A one-command local development server (`npm start`)
- A lightweight component system (admonitions, tabs, reusable MDX partials/snippets) that does not require Ruby or ERB
- SEO-friendly output (structured metadata, canonical URLs, sitemap) and AI-agent-friendly crawlable HTML, optionally an `/llms.txt` index
- Handling of HTML tables, including column-width specification
- Variables for values that repeat across pages, in a way that is transparent to contributors
- Code snippets of various types (shell, console, json, yaml) displayed by language with a copy button

The migration SHOULD use a phased approach (see [Phases](#phases)) and MUST NOT break the existing canonical `docs.cloudfoundry.org` URL during transition.

### 2. Deployment: GitHub Pages with Full Community Access

The documentation site MUST be deployed to GitHub Pages under the `cloudfoundry` GitHub organization:

- **Zero hosting cost** for a static site within GitHub's free tier.
- **Full community visibility:** deployment is driven by a GitHub Actions workflow in a public repository.
- **Access model mirrors existing patterns:** repository access SHOULD follow the GitHub Teams pattern established for Concourse and other CF org repos (see RFC-0014), removing any dependency on CFF staff. Merging and publishing remain with the Docs WG — "community self-serve" means transparency and no external dependencies, not that anyone can publish.

#### Domain Handling

- `docs.cloudfoundry.org` MUST remain functional during and after migration.
- During transition, a redirect or reverse-proxy MAY serve the new site while DNS is updated.
- Once stable, the DNS CNAME SHOULD point to the GitHub Pages endpoint.
- Old deep-link URLs MUST be handled via redirect configuration to avoid broken links.

### 3. Contribution Workflow and PR Automation

To sustain documentation quality without overburdening maintainers, the following SHOULD be adopted:

#### Repository Structure

The new CF documentation lives in **one single repository**: all content is authored, reviewed, built, and published from it, and Working Groups maintain their areas directly within it. This is a deliberate choice. It removes the "which repo do I edit?" problem — the URL path of a page maps directly to its file path, and the edit link on every page points straight to the right file with no lookup. It also keeps navigation and the pages it references in the same PR, instead of today's split between content repos and the separate book repo.

Docs-related content in other repositories is migrated into this repository during Phase 3 (see [Phases](#phases)).

#### Ownership and Notifications

Documentation is already a cross-Working-Group effort today, and the new repository MUST preserve that while making ownership clearer. Two properties MUST hold:

- **The Docs WG approves every merge.** Approval authority for merging into the docs repository rests with the Docs WG, regardless of which area a change touches.
- **The owning Working Group is notified for its area.** When a change touches a given area, the responsible WG is automatically informed and MAY review, but this is awareness and optional review — never a merge gate.

The exact mechanism is an implementation detail to be settled by the Docs WG, as long as it satisfies the two properties above. Area-to-WG ownership and the corresponding GitHub teams are defined in Phase 1 and SHOULD track WG membership in the community repo.

#### Review Process

1. A contributor opens a PR against the docs repository.
2. The owning WG is notified for awareness and optional review — not a merge requirement.
3. The Docs WG reviews and approves every PR before merge (content, style, consistency with the style guide).
4. Merging into the main branch triggers build and deployment to GitHub Pages.

#### Automation

- A GitHub Actions CI pipeline validates Markdown linting and broken links on every PR. Spell-checking is added in Version 2 (see [Versioning Strategy](#4-versioning-strategy)).
- Draft PRs are encouraged for early-stage work to enable async feedback.

### 4. Versioning Strategy

Documentation versioning is intended to be tied to CF Deployment release branches. In Version 1 (PoC) this mapping is not yet implemented: the docs start with a single `v1.0` version. The concrete approach — how many versions are tracked, how prior versions are retained, and how breaking changes are published — is defined in Version 2 after the migration, based on Version 1 experience.

Version 2 also adds **docs spellcheck**: an automated spell-check (e.g., `cspell` or a unified.js tool such as `retext`, selected in Version 2) runs in CI on every PR, with a configurable shared dictionary for CF and technical terms, maintained by the Docs WG.

### 5. Extension and Customization

Working Groups MUST NOT need custom extensions, plugins, or JavaScript to author documentation. Customization (CLI examples, version-specific callouts, tables, layouts) is handled by Docusaurus's built-in MDX features — admonitions, tabs, and reusable partials/snippets — keeping the contribution barrier low.

Parts of the existing documentation rely on HTML tables and CSS layouts that plain Markdown handles poorly. The PoC MUST validate that the most complex existing pages can be represented with MDX and Docusaurus components alone, and any gap MUST be reported as a PoC finding.

### Phases

#### Phase 1: Discovery and Stakeholder Alignment (Prerequisite)

Before technical work begins:

- **Identify all doc sources:** Produce a definitive list of all repositories feeding the public CF docs and the WG responsible for each. This defines the migration scope and the per-area ownership mapping. Led by the TOC with input from all WGs.
- **Survey consumers:** Ask WG leads and known downstream consumers (e.g., SAP BTP, anynines; VMware Tanzu works from its own branches and is not affected) whether they consume the docs as-is or maintain derivatives.
- **Clarify ownership:** Each section MUST have a named WG owner before migration.
- **Onboard maintainers:** Plan a familiarization period with the new toolchain for current docs maintainers before cutover.

#### Phase 2: Proof of Concept

A PoC SHOULD stand up Docusaurus with a representative subset of CF docs to validate local dev, search, versioning, GitHub Pages deployment, and the domain redirect strategy, and to gather feedback from at least three active contributors. A working PoC already exists (see [Proof of Concept](#proof-of-concept)); its results SHOULD be presented in a TOC / Docs WG meeting.

Docusaurus is the recommended engine. If the PoC surfaces a requirement Docusaurus cannot meet, the PoC team MAY evaluate and propose an alternative, documenting the reason as a PoC finding for the TOC / Docs WG to decide.

#### Phase 3: Full Migration

Based on PoC findings, all content SHOULD be migrated to Markdown by **one central migration team** for consistency. A migration script MAY be developed and AI tooling MAY be used for bulk conversion, as long as cross-repository links are preserved. Every section receives a manual review pass by the owning WG. A full migration timeline MUST be published and agreed by all affected WGs before this phase begins.

#### Phase 3a: Parallel Operation and Commit-Tracked Sync

After initial migration, the new docs repository and the existing source repositories run in parallel until cutover:

- The new repository tracks upstream sources via a manifest (e.g., `.docs-sources.json`) recording the last-synced commit SHA per source.
- A scheduled CI job converts changed content, opens a PR against the new repository, and updates the manifest on merge — so contributors need not change their existing workflow before cutover.
- The manifest and sync tooling are owned by the Docs WG.

This phase ends when all WGs confirm their content is fully migrated and the cutover date is set.

#### Phase 4: Cutover and Decommission

- The new site goes live at `docs.cloudfoundry.org`.
- The old build system is archived (not deleted) for historical reference.
- Redirect rules ensure all old URLs resolve correctly.
- The old hosting infrastructure is decommissioned after a defined stabilization window (suggested: 90 days).

### Suggested Timeline

- **Phase 1 (Discovery):** October – November 2026 — stakeholder survey completed, repository inventory published
- **Phase 2 (PoC):** November – December 2026 — working Docusaurus site with representative content, deployed to GitHub Pages
- **Phase 3 (Full Migration):** Q1 2027 — all content migrated, ownership mapping in place, CI pipeline live
- **Phase 3a (Parallel Operation):** Q1–Q2 2027 — commit-tracked sync running, WGs reviewing migrated content
- **Phase 4 (Cutover):** Q2 2027 — `docs.cloudfoundry.org` DNS switched, old infrastructure decommissioned

## Proof of Concept

A working Docusaurus implementation already demonstrates the advantages of this proposal to the audience and SHOULD inform the Phase 2 review:

- **Docusaurus PoC** (@johha, @ZPascal) — [johha/cf-docs-new](https://github.com/johha/cf-docs-new), live at <https://johha.github.io/cf-docs-new/>. It automatically migrates all 41 files of `docs-cloudfoundry-concepts` from the legacy ERB/book pipeline to Docusaurus 3, regenerating the sidebar, variables, and MDX output from source with a single `npm run gen:all`. It shows the full set of benefits in one place: Markdown/MDX authoring, variables, full-text search, SEO-ready output, and a one-command local preview.
- **Repository-layout comparison** (@norman-abramovitz) — [norman-abramovitz/cf-docs-rfc-proposal](https://github.com/norman-abramovitz/cf-docs-rfc-proposal) builds representative content in both single-repository and separate-repository layouts and confirms that published URLs and links are identical regardless of layout — supporting the single-repository decision in §3.

## Impact and Consequences

### Positive

- **Lower contribution barrier:** Any developer familiar with Markdown and GitHub can contribute documentation without learning a proprietary toolchain.
- **Re-enabled search:** Full-text search improves discoverability for users and reduces support load.
- **Cost reduction:** GitHub Pages hosting eliminates ongoing infrastructure costs.
- **Community ownership:** Documentation deployment is run transparently by the Docs WG without depending on CFF staff.
- **AI and SEO readiness:** Modern static site output is well-suited for search engine indexing and AI developer tools.
- **Versioning:** Documentation versions tied to releases reduce confusion about what applies to which CF version. This is planned for Version 2, scheduled after the migration.

### Negative / Risks

- **Migration effort:** Converting ERB/HTML to Markdown at scale requires significant up-front work from Working Groups. If stakeholder bandwidth is insufficient, the migration may stall.
- **Link rot:** If redirect handling is incomplete, existing documentation links in blog posts, books, and third-party sites will break.
- **JavaScript dependency:** Docusaurus requires Node.js. Contributors who work without a JavaScript toolchain will need to install it; a Docker-based development option SHOULD be provided as an alternative.
- **Review bottleneck:** More contributor access may increase PR volume. Notifications mitigate but do not eliminate this.

## Open Questions

- Which repositories currently feed the public CF docs, and which Working Groups own them? (Phase 1.)
- Do downstream distributions (SAP, VMware Tanzu) consume the raw source or the rendered HTML, and would Markdown require changes on their end?
- Which search backend (Algolia DocSearch, Pagefind, or lunr.js) should back the Docusaurus site?
- Who owns and staffs the Phase 1 survey, the central migration team, and ongoing technical support for the new stack?
- Who can vet this proposal for the UAA API and CredHub API docs?
- Who owns the `docs.cloudfoundry.org` domain (registrar, DNS, hosting) and can change the DNS records for cutover?
