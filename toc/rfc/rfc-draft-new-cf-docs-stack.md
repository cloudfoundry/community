# Meta
[meta]: #meta
- Name: Cloud Foundry Documentation Modernization
- Start Date: 2026-10-01
- Author(s): @johha @ZPascal @Dominik23
- Status: Draft
- RFC Pull Request: https://github.com/cloudfoundry/community/pull/1642
- Affected Component(s): CF Documentation, all Working Groups maintaining documentation


## Summary

This RFC proposes migrating the Cloud Foundry documentation (CF, UAA API) from the current Ruby/ERB HTML build system to a Markdown-first toolchain hosted on GitHub Pages. The goals are to lower the contribution barrier, re-enable full-text search, cut hosting costs, and give the community full ownership of the documentation pipeline. Two exploratory proofs of concept support discussion and alignment during RFC review (see [Proof of Concept for RFC Review](#proof-of-concept-for-rfc-review)).

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

The CF documentation SHOULD be rewritten in plain Markdown and managed by **Docusaurus** (current major version, v3 or newer — maintained by Meta, MIT-licensed, widely adopted in the CNCF ecosystem). Phase 2 validates this choice (see [Phase 2](#phase-2-initial-implementation)). Docusaurus uses MDX for templating and reusable components, replacing the ERB templating.

Docusaurus provides the capabilities the new stack requires:

- Markdown/MDX authoring with no custom templating language
- Built-in full-text search (e.g., Algolia DocSearch or a self-hosted option such as Pagefind or lunr.js)
- Clear, easy-to-maintain navigation that helps readers, including first-time CF users, find their way through the documentation
- A one-command local development server (`npm start`)
- A lightweight component system (admonitions, tabs, reusable MDX partials/snippets) that does not require Ruby or ERB
- SEO-friendly output (structured metadata, canonical URLs, sitemap) and AI-agent-friendly crawlable HTML, optionally an `/llms.txt` index
- Handling of HTML tables, including column-width specification
- Variables for values that repeat across pages, in a way that is transparent to contributors
- Code snippets of various types (shell, console, json, yaml) displayed by language with a copy button

The migration SHOULD use a phased approach (see [Phases](#phases)).

### 2. Deployment: GitHub Pages with Full Community Access

The documentation site MUST be deployed to GitHub Pages under the `cloudfoundry` GitHub organization:

- **Zero hosting cost** for a static site within GitHub's free tier.
- **Full community visibility:** deployment is driven by a GitHub Actions workflow in a public repository.
- **Access model mirrors existing patterns:** repository access SHOULD follow the GitHub Teams pattern established for Concourse and other CF org repos (see RFC-0014), removing any dependency on CFF staff. Docs WG approvers and leads SHOULD be able to trigger publishing of approved content.

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

Contributors SHOULD be able to navigate between code repositories and their corresponding documentation sources.

#### Ownership and Notifications

Documentation is already a cross-Working-Group effort today, and the new repository MUST preserve that while making ownership clearer. Two properties MUST hold:

- **The Docs WG approves every merge.** Approval authority for merging into the docs repository rests with the Docs WG, regardless of which area a change touches.
- **The owning Working Group is notified for its area.** When a change touches a given area, the responsible WG is automatically informed and MAY review, but this is awareness and optional review — never a merge gate.

The exact mechanism is an implementation detail to be settled by the Docs WG, as long as it satisfies the two properties above. Area-to-WG ownership and the corresponding GitHub teams are defined in Phase 1 and SHOULD track WG membership in the community repo.

#### Review Process

1. A contributor opens a PR against the docs repository.
2. The owning WG is notified (see [Ownership and Notifications](#ownership-and-notifications)).
3. The Docs WG reviews and approves the PR, using a shared documentation style and structure guide that it maintains.
4. Merging into the main branch triggers build and deployment to GitHub Pages.

#### Automation

- Automated checks for document structure and broken links MUST run on every PR and pass before merge. Approvers SHOULD also be able to trigger these checks on demand.
- Spell-checking is planned as a follow-up, using a shared dictionary for CF and technical terms maintained by the Docs WG.
- Draft PRs are encouraged for early-stage work to enable async feedback.

### 4. Documentation Versioning

The documentation initially has only version `1.0`. This RFC does not define a documentation versioning concept. Although the toolchain technically supports multiple versions, a versioning concept MAY be introduced in a follow-up.

### 5. Extension and Customization

The new toolchain MUST support existing documentation content using standard formatting wherever possible. Custom HTML and layouts SHOULD be used only where standard formatting is insufficient. The Docs WG owns and approves shared tooling; contributors MUST NOT need to develop it themselves.

Initial implementation MUST validate the most complex existing pages and report any gaps.

### Phases

#### Phase 1: Discovery and Stakeholder Alignment (Prerequisite)

Before migration implementation begins:

- **Identify all doc sources:** Produce a definitive list of all repositories feeding the public CF docs and the WG responsible for each. This defines the migration scope and the per-area ownership mapping. Led by the TOC with input from all WGs.
- **Clarify ownership:** Each section MUST have a named WG owner before migration.
- **Onboard maintainers:** Plan a familiarization period with the new toolchain for current docs maintainers before cutover.

#### Phase 2: Initial Implementation

This phase establishes the initial documentation site as the foundation for the full migration. It SHOULD set up Docusaurus with a representative subset of CF docs, establish local dev, search, and GitHub Pages deployment, validate the domain redirect strategy, and gather feedback from at least three active contributors. The existing [RFC-review PoCs](#proof-of-concept-for-rfc-review) MAY inform this work, but do not replace it. Implementation results SHOULD be presented in a TOC / Docs WG meeting.

Docusaurus is the recommended engine. If initial implementation surfaces a requirement Docusaurus cannot meet, the implementation team MAY evaluate and propose an alternative, documenting the reason for the TOC / Docs WG to decide.

#### Phase 3: Full Migration

Building on the initial implementation and findings from Phase 2, all remaining content SHOULD be migrated to Markdown by **one central migration team** for consistency. A migration script MAY be developed and AI tooling MAY be used for bulk conversion, as long as cross-repository links are preserved. Every section receives a manual review pass by the owning WG. A full migration timeline MUST be published and agreed by all affected WGs before this phase begins.

#### Phase 3a: Parallel Operation

During parallel operation, existing repositories remain the source of truth until cutover. The Docs WG defines synchronization, review, and conflict handling to ensure no changes are lost. Cutover follows confirmation from all affected WGs that their content is fully migrated.

#### Phase 4: Cutover and Decommission

- The new site goes live at `docs.cloudfoundry.org`.
- The old build system is archived (not deleted) for historical reference.
- The old hosting infrastructure is decommissioned after a defined stabilization window (suggested: 90 days).

### Suggested Timeline

- **Phase 1 (Discovery):** December 2026 – January 2027 — repository inventory and ownership mapping published
- **Phase 2 (Initial Implementation):** February – March 2027 — working Docusaurus site with representative content, deployed to GitHub Pages
- **Phase 3 (Full Migration):** Q2 2027 — all content migrated, ownership mapping in place, CI pipeline live
- **Phase 3a (Parallel Operation):** Q2–Q3 2027 — synchronization running, WGs reviewing migrated content
- **Phase 4 (Cutover):** Q3 2027 — `docs.cloudfoundry.org` DNS switched, old infrastructure decommissioned

## Proof of Concept for RFC Review

The following small, exploratory proofs of concept were created to make this RFC easier to discuss and give reviewers concrete examples of the proposed approach. They do not replace the Phase 2 initial implementation:

- **Docusaurus PoC** (@johha, @ZPascal) — [johha/cf-docs-new](https://github.com/johha/cf-docs-new), live at <https://johha.github.io/cf-docs-new/>. It automatically migrates all 41 files of `docs-cloudfoundry-concepts` from the legacy ERB/book pipeline to Docusaurus 3, regenerating the sidebar, variables, and MDX output from source with a single `npm run gen:all`. It shows the full set of benefits in one place: Markdown/MDX authoring, variables, full-text search, SEO-ready output, and a one-command local preview.
- **Repository-layout comparison** (@norman-abramovitz) — [norman-abramovitz/cf-docs-rfc-proposal](https://github.com/norman-abramovitz/cf-docs-rfc-proposal) builds representative content in both single-repository and separate-repository layouts and confirms that published URLs and links are identical regardless of layout.

## Impact and Consequences

### Positive

- **Lower contribution barrier:** Any developer familiar with Markdown and GitHub can contribute documentation without learning a proprietary toolchain.
- **Re-enabled search:** Full-text search improves discoverability for users and reduces support load.
- **Cost reduction:** GitHub Pages hosting eliminates ongoing infrastructure costs.
- **Community ownership:** Documentation deployment is run transparently by the Docs WG without depending on CFF staff.
- **AI and SEO readiness:** Modern static site output is well-suited for search engine indexing and AI developer tools.

### Negative / Risks

- **Migration effort:** Converting ERB/HTML to Markdown at scale requires significant up-front work from Working Groups. If stakeholder bandwidth is insufficient, the migration may stall.
- **Link rot:** If redirect handling is incomplete, existing documentation links in blog posts, books, and third-party sites will break.
- **JavaScript dependency:** Docusaurus requires Node.js. Contributors who work without a JavaScript toolchain will need to install it; a Docker-based development option SHOULD be provided as an alternative.
- **Review bottleneck:** More contributor access may increase PR volume. Notifications mitigate but do not eliminate this.

## Open Questions

- After initial implementation, do any downstream companies still republish or derive the official CF documentation, and are there compatibility requirements to consider?
- Which search backend (Algolia DocSearch, Pagefind, or lunr.js) should back the Docusaurus site?
- Who owns and staffs discovery, the central migration team, and ongoing technical support for the new stack?
- Who can vet this proposal for the UAA API and CredHub API docs?
- Who owns the `docs.cloudfoundry.org` domain (registrar, DNS, hosting) and can change the DNS records for cutover?
