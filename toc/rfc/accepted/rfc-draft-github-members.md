# Meta
[meta]: #meta
- Name: Who is able to add and remove members of the Cloudfoundry GitHub org
- Start Date: 2022-01-26
- Author(s): @LeePorte
- Status: Draft
- RFC Pull Request: (fill in with PR link after you submit it)


## Summary

As the Cloudfoundry moves from the dojo model to an open committer model the existing central team in VMWare are no 
longer appropriately positioned to grant and revoke access to users of the Cloudfoundry GitHub org

## Problem

Previously re was a central team in VMWare that undertook adding of individuals on successful completion of the dojo, 
as this was the process for gaining committer rights on the repositories. However, as this model is no longer in use it
presents a problem in terms of who should fulfil this role.

## Proposal

As defined in the [roles](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md), contributor and above roles
should be members of the Cloudfoundry org and possibly other orgs if appropriate. As the responsibility to become a
contributor is to make multiple contributions and be an active member of the community, it should for the Approvers and 
Working Group Leads to make the judgement call on if an individual has met the criteria to become a contributor.

The addition of raising and merging PRs to add members to the cloudfoundry and other foundation org(s) is the 
responsibility of the working group approvers and leads.

Removing members of the cloudfoundry and other foundation org(s) may have unintended consequences. As a result the 
process is slightly different, raising PRs to remove members of the cloudfoundry and other foundation org(s) is the 
responsibility of the working group approvers and leads as they are closest to the members. However as there potential 
unintended consequences or removing members, the working group will not be responsible for the merging or closing of 
removal PRs. Removal PRs should be tagged `toc` and mention `@cloudfoundry/toc`. The TOC will then take responsibility 
for the merging or closing of the raised PRs.
