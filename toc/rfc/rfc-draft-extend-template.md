
## Meta
**Name:** Extend RFC Template with Related RFCs and AffectedComponent Fields

**Start Date:** 2025-01-23

**Author(s):** @beyhan

**Status:** Draft

**RFC Pull Request:** (fill in with PR link after you submit it)

## Summary
This RFC proposes extending the current [Cloud Foundry RFC template](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-template.md) with two additional metadata fields: `Related RFCs` and `Affected Component(s)`. These fields will improve traceability between related proposals and make it easier to identify which Cloud Foundry components are affected by a given RFC.


## Problem
The current RFC template lacks structured fields for capturing relationships between RFCs and identifying affected Cloud Foundry components. This makes it difficult to:

- Understand dependencies or relationships between proposals
- Quickly identify which teams or components need to review a given RFC
- Search and filter RFCs by affected component
- Understand the broader context of a proposal without reading the full document

## Proposal
The current Meta section of the RFC template should be extended with two additional fields:

**Current template:**
```markdown
Meta
Name: (fill in the feature name: My Feature)
Start Date: (fill in today's date: YYYY-MM-DD)
Author(s): (GitHub usernames)
Status: Draft
RFC Pull Request: (fill in with PR link after you submit it)
```

**Proposed template:**
```markdown
Meta
Name: (fill in the feature name: My Feature)
Start Date: (fill in today's date: YYYY-MM-DD)
Author(s): (GitHub usernames)
Status: Draft
RFC Pull Request: (fill in with PR link after you submit it)
Related RFCs: (links to related or dependent RFCs)
Affected Component(s): (affected Cloud Foundry components e.g., Diego, Gorouter)
```

### Field Definitions

**Related RFCs**
- This field MUST contain links to any RFCs that are directly related or dependent on this proposal
- This field MAY be left empty if no related RFCs exist
- Multiple RFCs SHOULD be listed as a comma separated list of links

**Affected Component(s)**
- This field MUST list all Cloud Foundry components affected by the proposal
- This field SHOULD reference the official component names as used in the Cloud Foundry GitHub organization
- Multiple components SHOULD be listed as a comma separated list