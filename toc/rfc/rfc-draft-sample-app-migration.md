# Meta
[meta]: #meta
- Name: Sample Application Migration and Portfolio Consolidation
- Start Date: 2026-10-09
- Author(s): @benjaminguttmann-avtq
- Status: Draft
- RFC Pull Request: [community#1657](https://github.com/cloudfoundry/community/pull/1657)
- Related RFCs:
- Approving Working Groups: Buildpacks and Stacks; Docs
- Affected Component(s): cloudfoundry-samples repositories; Docs working group charter (Cloud Foundry Tutorials area); sample documentation and validation for classic Cloud Foundry buildpacks

## Summary

Maintain a focused, owned set of Cloud Foundry sample applications instead of
migrating all 73 repositories in cloudfoundry-samples unchanged. Keep examples that
show distinct buildpack capabilities, consolidate duplicates, add samples for
uncovered buildpacks, and keep everything current with automated dependency updates
and tests on kind-deployment.

A static source review (Appendix) recommends retaining 12 samples, replacing 8
while preserving their capabilities, consolidating 34 into 10 existing repositories,
deciding 11 platform/service demos separately, and excluding 8 helper or superseded
projects. The Cloud Foundry Tutorials area of the Docs working group will own the
samples. This RFC archives or deletes no repository.

## Problem

The organization holds many historical applications: overlapping frameworks,
obsolete instructions, service demos and helper projects. Migrating them unchanged
carries forward duplicate maintenance and unsupported assumptions; dropping them by
age or language would lose useful deployment examples.

Language coverage is not feature coverage. A Spring Boot JAR and a Tomcat WAR differ,
a WAR-packaged JRuby app does not show JRuby on the Ruby buildpack, and old PHP
samples rely on Python user extensions the reviewed PHP buildpack no longer supports.
No sample uses Staticfile, Nginx, R or Binary.

## Proposal

### Goals and non-goals

**Goals:** a small, owned set of examples covering distinct CF deployment capabilities,
kept current by automation.

**Non-goals:** Paketo/CNB, buildpack or CF runtime changes, and preserving the
business workflows of old applications.

### Consolidation

Each of the 34 consolidation candidates maps to one of 10 existing destination
repositories. These are not new repositories or the final portfolio size. The
[Appendix](#appendix) links to the full analysis with destinations, missing variants
and the mapping for each source.
Replacements keep deployment and configuration demonstrations only, not business
workflows. Variants stay small and independent and are built once per destination.
For example, enki, rails_sample_app and pong_matcher_rails map to cf-sample-app-rails,
which first needs database bindings and migrations.

### Coverage additions

Add small samples for Staticfile, Nginx, R and Binary; names and locations are open.
Preserve the Java WAR, JAR, Groovy, Play and DistZip paths, direct JRuby, PHP
CLI/tasks and Apt composition. Verify the PHP JSON user-extension loader before
relying on it.

### Ownership

The samples will be owned by the Cloud Foundry Tutorials area of the Docs WG.

### Automated dependency maintenance

Maintained repositories MUST configure automated update PRs (Dependabot, Renovate or
equivalent). Update PRs run build and smoke tests on kind-deployment with the latest
published buildpack releases on all stacks, currently cflinuxfs4 and cflinuxfs5.
Failed, missing, skipped or stale checks MUST block merging.

Dependency-only PRs from trusted automation may auto-merge without maintainer review
under an owner-approved policy, starting with patch and minor updates covered by
tests. Auto-merge cannot bypass required checks. Major versions, runtime-target and
CI/test changes, and anything outside the policy MUST get maintainer review.

Use least-privilege credentials. If an auto-merged update breaks an example, pause
that update class, fix the issue, and rerun the matrix. This automation is proposed,
not configured.

## Retirement criteria

A source repository MUST NOT be archived until:

- its replacement capabilities are validated, or its owner agrees none is needed;
- known users and documentation references are checked, and its README names the
  successor and limitations;
- useful tests and recipes are preserved and required approvals are recorded.

Prefer archiving; this RFC authorizes no deletion. If validation fails, retirement waits.

## Alternatives considered

| Alternative | Assessment |
| --- | --- |
| Migrate all 73 unchanged | Carries obsolete instructions and duplicates forward. |
| One application per language | Loses packaging, worker and composition capabilities. |
| Archive outdated repositories now | Removes references without validated successors. |

The trade-off is less duplicate maintenance against the effort required for shared
variants, a two-stack test environment and dependency automation; neither effort nor
savings is measured.

## Open decisions before implementation

- Which maintainers, and what capacity, does the Docs working group commit to the
  samples?
- kind-deployment installs no MySQL, Redis, RabbitMQ or MongoDB: how are
  service-dependent variants tested, and who maintains repeatable validation?
- What are the owner decisions for the 11 platform/service demos and 8 helper or
  superseded projects?

## Appendix

The supporting material is in [Sample application migration and portfolio consolidation](https://gist.githubusercontent.com/benjaminguttmann-avtq/8b1411c732b1ec187c4b1cd12dcfbae0/raw/8ae3c98176c3ff74a96369a036dd261c15225c7b/sample_application_migration_portfolio_consolidation.md). It covers the portfolio decisions, ownership and repository transfer, rollout and validation, risks and failure scenarios, consolidation destinations and missing variants, and the full sample application analysis, including the decision matrix for all 73 repositories.
