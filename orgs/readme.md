# CFF Managed Github Orgs

:construction: Multiple CFF Managed Github Orgs is work-in-progress. Currently, only the `cloudfoundry` org is supported as CFF Managed Github Org.

The projects, teams and org membership in CFF Managed Github Orgs are maintained according to a number of [RFCs](https://github.com/cloudfoundry/community/tree/main/toc/rfc). The RFCs require PRs to one of the following files:

- [orgs.yml](https://github.com/cloudfoundry/community/blob/main/orgs/orgs.yml) - static org configuration and projects
- [contributors.yml](https://github.com/cloudfoundry/community/blob/main/orgs/contributors.yml) - list of [Contributors](https://github.com/cloudfoundry/community/blob/main/toc/ROLES.md#contributor) per org
- [branchprotection.yml](https://github.com/cloudfoundry/community/blob/main/orgs/branchprotection.yml) - static branch protection rules for projects
- [TOC.md](https://github.com/cloudfoundry/community/blob/main/toc/TOC.md) - projects owned by the TOC (specified in yaml block)
- [ADMIN.md](https://github.com/cloudfoundry/community/blob/main/toc/ADMIN.md) - special WG for maintaining administrative repositories owned by CFF staff
- [Working Group Charters](https://github.com/cloudfoundry/community/tree/main/toc/working-groups) - projects owned by working groups (specified in yaml block)

Once approved and merged, the github action [org-management.yml](https://github.com/cloudfoundry/community/actions/workflows/org-management.yml) compiles a resulting Github org configuration from the files mentioned above and applies it with [peribolos](https://github.com/kubernetes/test-infra/tree/master/prow/cmd/peribolos).

[org_management.py](https://github.com/cloudfoundry/community/blob/main/orgs/org-management.py) generates the following parts of the resulting CFF Managed Github Org configuration:

### Organization Members
Organization members are generated according to [rfc-0002-github-members](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0002-github-members.md) and [rfc-0008-role-change-process](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0008-role-change-process.md):
- any members specified in [orgs.yml](https://github.com/cloudfoundry/community/blob/main/orgs/orgs.yml) (should be none)
- all contributors from [contributors.yml](https://github.com/cloudfoundry/community/blob/main/orgs/contributors.yml)
- all working group leads, approvers, reviewers and bots specified in the [Working Group Charters](https://github.com/cloudfoundry/community/tree/main/toc/working-groups)
- org admins and TOC members must not be added to org member list
- WG leads of all github orgs are added as members to the `cloudfoundy` org to get access to the `community` repo

### Organization Admins
Organization admins are:
- any admin specified in [orgs.yml](https://github.com/cloudfoundry/community/blob/main/orgs/orgs.yml) (should be none)
- all TOC execution leads and technical leads specified in [TOC.md](https://github.com/cloudfoundry/community/blob/main/toc/TOC.md) 

### Github Teams for Working Group Areas
Github Teams for the TOC, all Working Group Leads, Working Groups and Working Group Areas are generated according to [rfc-0014-github-teams-and-access.md](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0014-github-teams-and-access.md).
Repositories listed in the working group yaml block that belong to github organizations other than the one specified in the working group yaml (default github organization is `cloudfoundy`) are ignored.

### Branch Protection Rules

Working groups can opt-in into branch protection rule generation for their projects according to [rfc-0015-branch-protection](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0015-branch-protection.md) by setting a configuration flag in the working group charter yaml:

```
config:
  generate_rfc0015_branch_protection_rules: true
```

Branch protection rules are applied using the [branchprotector tool from the prow toolset](https://docs.prow.k8s.io/docs/components/optional/branchprotector/).
Rules specified in [branchprotection.yml](https://github.com/cloudfoundry/community/blob/main/orgs/branchprotection.yml) take precedence, i.e. no RFC-0015 rules are generated for repositories listed here but the static configuration is taken without modification.

The generated branch protection rules specification for working group projects look like:
```
branch-protection:
  orgs:
    cloudfoundry:
      repos:
        # automation generates config for all repos belonging to a WG unless an explicit configuration exists in branchprotection.yml
        <projectname>:
          protect: true
          enforce_admins: true
          allow_force_pushes: false
          allow_deletions: false
          allow_disabled_policies: true  # needed to allow branches w/o branch protection
          required_pull_request_reviews:
            dismiss_stale_reviews: true
            require_code_owner_reviews: true
            required_approving_review_count: 0 (if project has <=3 approvers) or 1 (if project has >=4 approvers)
            bypass_pull_request_allowances:
              teams: [<WG and WG area bot teams>]
          include: [ "^<default branch>$", "^v[0-9]*$"]  # note the surrounding ^...$ to avoid matching branches containing 'main' or 'v'
```

Best Practices:
- Replace github deploy keys by working group bot users. Branch protection rules enforce PRs for commits with deploy keys (enforce_admins=true).
- Ensure that all bot users are members of the working group bots team or working group area bots team.
- Remove all direct repository users in 'Settings > Collaborators and teams'. Repository access shall be governed by the generated teams only.
- You may exclude repos w/o source code (e.g. bbl config and state, semver). See [branchprotection.yml](https://github.com/cloudfoundry/community/blob/main/orgs/branchprotection.yml) for examples.

Limitations:
- The branchprotector doesn't support wildcards for branch rules. I.e. every version branch gets its own rule.
- The branchprotector doesn't delete unneeded branch protection rules e.g. when a version branch got deleted.

### Inactive User Management
Inactive users according to the criteria defined in
[rfc-0025-define-criteria-and-removal-process-for-inactive-members](https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0025-define-criteria-and-removal-process-for-inactive-members.md) are identified by an automation which opens a pull-request to delete those.


## Development

Requires Python 3.9.

How to run locally:
```
cd ./orgs
python -m venv <path/to/venv>
source <path/to/venv>/bin/activate
pip install -r requirements.txt
python -m org_management --help
python -m org_user_management --help
```

Usage:
```
$ python -m org_management --help
usage: org_management.py [-h] [-o OUT] [-b BRANCHPROTECTION]

Cloud Foundry Org Generator

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     output file for generated org configuration
  -b BRANCHPROTECTION, --branchprotection BRANCHPROTECTION
                        output file for generated branch protection rules
```

```
python -m org_user_management --help
usage: org_user_management.py [-h] [-goid GITHUBORGID] [-go GITHUBORG] [-sd SINCEDATE] [-gt GITHUBTOKEN] [-dr DRYRUN] [-tu TAGUSERS]

Cloud Foundry Org Inactive User Handler

options:
  -h, --help            show this help message and exit
  -goid GITHUBORGID, --githuborgid GITHUBORGID
                        Cloud Foundry Github org ID
  -go GITHUBORG, --githuborg GITHUBORG
                        Cloud Foundry Github org name
  -sd SINCEDATE, --sincedate SINCEDATE
                        Since when to analyze in format 'Y-m-dTH:M:SZ'
  -gt GITHUBTOKEN, --githubtoken GITHUBTOKEN
                        Github API access token. Supported also as env var 'GH_TOKEN'
  -dr DRYRUN, --dryrun DRYRUN
                        Dry run execution. Supported also as env var 'INACTIVE_USER_MANAGEMENT_DRY_RUN'
  -tu TAGUSERS, --tagusers TAGUSERS
                        Tag users to be notified. Supported also as env var 'INACTIVE_USER_MANAGEMENT_TAG_USERS'
```

How to run tests:
```
cd ./org
python -m venv <path/to/venv>
source <path/to/venv>/bin/activate
pip install -r requirements-dev.txt
python -m flake8
python -m unittest discover -s .
```