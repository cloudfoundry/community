# Generates cloudfound org configuration for Peribolos from:
# - a static configuration: orgs.yml
# - a contributors list: contributors.yml
# - the WG charters: ../toc/working-groups/*.md (yaml block)
# - the TOC charter: ../toc/TOC.md (yaml block)
#
# See readme.md

import glob
import os
import re
from pathlib import Path
from typing import Any, TextIO, final, override

import jsonschema
import yaml

_SCRIPT_PATH = Path(__file__).parent.parent.resolve()


# pyyaml silently ignores duplicate keys but they shall be rejected
# https://yaml.org/spec/1.2.2/ requires unique keys
class UniqueKeyLoader(yaml.SafeLoader):
    @override
    def construct_mapping(self, node: Any, deep: bool = False):
        mapping = set[str]()
        for key_node, _ in node.value:
            key: str = str(self.construct_object(key_node, deep=deep))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
            if key in mapping:
                raise yaml.MarkedYAMLError(f"Duplicate key {key!r} found.", key_node.start_mark)
            mapping.add(key)
        return super().construct_mapping(node, deep)


@final
class OrgGenerator:
    # list of managed orgs, should match ./ORGS.md
    _MANAGED_ORGS = ["cloudfoundry"]
    _DEFAULT_ORG = "cloudfoundry"

    # parameters intended for testing only, all params are yaml docs
    def __init__(
        self,
        static_org_cfg: str | None = None,
        contributors: str | None = None,
        toc: str | None = None,
        working_groups: list[str] | None = None,
        branch_protection: str | None = None,
    ):
        self.org_cfg: dict[str, Any] = (
            OrgGenerator._validate_github_org_cfg(OrgGenerator._yaml_load(static_org_cfg)) if static_org_cfg else {"orgs": {}}
        )
        self.contributors = dict[str, set[str]]()
        self.working_groups: dict[str, Any] = {}
        self.branch_protection: dict[str, Any] = (
            OrgGenerator._validate_branch_protection(OrgGenerator._yaml_load(branch_protection))
            if branch_protection
            else {"branch-protection": {"orgs": {}}}
        )
        for org in OrgGenerator._MANAGED_ORGS:
            if org not in self.org_cfg["orgs"]:
                self.org_cfg["orgs"][org] = {"admins": [], "members": [], "teams": {}, "repos": {}}
            self.contributors[org] = set()
            self.working_groups[org] = []
            if org not in self.branch_protection["branch-protection"]["orgs"]:
                self.branch_protection["branch-protection"]["orgs"][org] = {"repos": {}}
        if contributors:
            contributors_yaml = OrgGenerator._yaml_load(contributors)
            OrgGenerator._validate_contributors(contributors_yaml)
            for org in contributors_yaml["orgs"]:
                self.contributors[org] = set(contributors_yaml["orgs"][org]["contributors"])

        self.toc = OrgGenerator._yaml_load(toc) if toc else OrgGenerator._empty_wg_config("TOC")
        OrgGenerator._validate_wg(self.toc)
        self.toc_org = self.toc["org"]
        wgs = [OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg)) for wg in working_groups] if working_groups else []
        for wg in wgs:
            org = wg["org"]
            if org not in OrgGenerator._MANAGED_ORGS:
                raise ValueError(f"Invalid org {org} in WG {wg['name']}, expected one of {OrgGenerator._MANAGED_ORGS}")
            self.working_groups[org].append(wg)

    def load_from_project(self):
        path = f"{_SCRIPT_PATH}/orgs.yml"
        print(f"Reading static org configuration from {path}")
        self.org_cfg = OrgGenerator._validate_github_org_cfg(OrgGenerator._read_yml_file(path))
        for org in OrgGenerator._MANAGED_ORGS:
            if org not in self.org_cfg["orgs"]:
                self.org_cfg["orgs"][org] = {"admins": [], "members": [], "teams": {}, "repos": {}}

        path = f"{_SCRIPT_PATH}/contributors.yml"
        if os.path.exists(path):
            print(f"Reading contributors from {path}")
            contributors_yaml = OrgGenerator._read_yml_file(path)
            OrgGenerator._validate_contributors(contributors_yaml)
            for org in contributors_yaml["orgs"]:
                self.contributors[org] = set(contributors_yaml["orgs"][org]["contributors"])

        path = f"{_SCRIPT_PATH}/branchprotection.yml"
        print(f"Reading branch protection configuration from {path}")
        self.branch_protection = OrgGenerator._validate_branch_protection(OrgGenerator._read_yml_file(path))
        for org in OrgGenerator._MANAGED_ORGS:
            if org not in self.branch_protection["branch-protection"]["orgs"]:
                self.branch_protection["branch-protection"]["orgs"][org] = {"repos": {}}

        # working group charters (including TOC and ADMIN), ignore WGs without yaml block
        toc = OrgGenerator._read_wg_charter(f"{_SCRIPT_PATH}/../toc/TOC.md")
        if toc:
            self.toc = toc
            self.toc_org = toc["org"]

        wg_files = glob.glob(f"{_SCRIPT_PATH}/../toc/working-groups/*.md")
        wg_files += glob.glob(f"{_SCRIPT_PATH}/../toc/ADMIN.md")
        for wg_file in wg_files:
            if not wg_file.endswith("/WORKING-GROUPS.md"):
                wg = OrgGenerator._read_wg_charter(wg_file)
                if wg:
                    org = wg["org"]
                    if org not in OrgGenerator._MANAGED_ORGS:
                        raise ValueError(f"Invalid org {org} in WG {wg['name']}, expected one of {OrgGenerator._MANAGED_ORGS}")
                    self.working_groups[org].append(wg)

    def validate_repo_ownership(self) -> bool:
        valid = True

        # rfc-0007-repository-ownership: a repo can't be owned by multiple WGs, scope is github org
        for org in OrgGenerator._MANAGED_ORGS:
            repo_owners = {}
            for wg in self.working_groups[org]:
                wg_name = wg["name"]
                wg_repos = set(r for a in wg["areas"] for r in a["repositories"])
                for repo in wg_repos:
                    if repo in repo_owners:
                        print(f"ERROR: Repository {repo} is owned by multiple WGs: {repo_owners[repo]}, {wg_name}")
                        valid = False
                    else:
                        repo_owners[repo] = wg_name

        # rfc-0036-multiple-github-orgs: Working Groups MUST only contain repos from one CFF Github Org (but repos from unmanaged orgs are allowed as temporary exception)
        for org in self.working_groups.keys():
            for wg in self.working_groups[org]:
                wg_name = wg["name"]
                wg_repos = set(r for a in wg["areas"] for r in a["repositories"])
                for repo in wg_repos:
                    repo_org = repo.split("/")[0]
                    if repo_org != org and repo_org in OrgGenerator._MANAGED_ORGS:
                        print(
                            f"ERROR: Working Group {wg_name} assigned to Github org {org} contains repository {repo} from different managed org."
                        )
                        valid = False

        return valid

    def get_contributors(self, org: str) -> set[str]:
        return set(self.contributors[org]) if org in self.contributors else set()

    def get_community_members_with_role_by_wg(self, org: str) -> dict[str, set[str]]:
        # TOC is always added
        result = {"toc": set(OrgGenerator._wg_github_users(self.toc))}
        for wg in self.working_groups[org]:
            result[wg["name"]] = OrgGenerator._wg_github_users(wg)
        return result

    def generate_org_members(self):
        for org in OrgGenerator._MANAGED_ORGS:
            org_members = set(self.org_cfg["orgs"][org]["members"])  # just in case, should be empty list
            org_members |= self.get_contributors(org)
            for wg in self.working_groups[org]:
                org_members |= OrgGenerator._wg_github_users(wg)
            # wg-leads of all WGs shall be members in cloudfoundy org for access to community repo
            if org == self.toc_org:
                for _org in OrgGenerator._MANAGED_ORGS:
                    for wg in self.working_groups[_org]:
                        org_members |= OrgGenerator._wg_github_users_leads(wg)
            org_admins = set(self.org_cfg["orgs"][org]["admins"])
            org_admins |= OrgGenerator._wg_github_users_leads(self.toc)
            org_members = org_members - org_admins
            self.org_cfg["orgs"][org]["members"] = sorted(org_members)
            self.org_cfg["orgs"][org]["admins"] = sorted(org_admins)

    def generate_teams(self):
        # overwrites any teams in orgs.yml that match a generated team name according to RFC-0005
        # toc team, only in cloudfoundry org
        # TOC members have org admin access in all managed orgs
        (name, team) = OrgGenerator._generate_toc_team(self.toc)
        self.org_cfg["orgs"][self.toc["org"]]["teams"][name] = team
        # wg teams for all orgs
        for org in OrgGenerator._MANAGED_ORGS:
            # working group teams
            for wg in self.working_groups[org]:
                if wg["org"] == org:
                    (name, team) = OrgGenerator._generate_wg_teams(wg)
                    self.org_cfg["orgs"][org]["teams"][name] = team
            # wg-leads team
            (name, team) = OrgGenerator._generate_wg_leads_team(self.working_groups[org])
            self.org_cfg["orgs"][org]["teams"][name] = team

        # wg-leads get write access to community repo which is in cloudfoundry org
        # RFC-0005 lists community repo explicitly (not all TOC repos)
        self.org_cfg["orgs"][self.toc_org]["teams"]["wg-leads"]["repos"] = {"community": "write"}
        # wg leads of other orgs -> create extra wg-leads-<org> team in cloudfoundry org
        for org in OrgGenerator._MANAGED_ORGS:
            if org != self.toc_org:
                wg_leads_other_org = self.org_cfg["orgs"][org]["teams"]["wg-leads"]
                team = {
                    "description": f"Technical and Execution Leads for all WGs in organization {org}",
                    "privacy": "closed",
                    "members": wg_leads_other_org["members"],
                    "repos": {"community": "write"},
                }
                self.org_cfg["orgs"][self.toc_org]["teams"][f"wg-leads-{org}"] = team

    def generate_branch_protection(self):
        # basis is static config in self.branch_protection which is never overwritten
        # generate RFC0015 branch protection rules for every WG+TOC by default
        for org in OrgGenerator._MANAGED_ORGS:
            branch_protection_repos = self.branch_protection["branch-protection"]["orgs"][org]["repos"]
            wgs = self.working_groups[org]
            if org == self.toc["org"]:
                wgs.append(self.toc)
            for wg in wgs:
                repo_rules = self._generate_wg_branch_protection(wg)
                for repo in repo_rules:
                    if repo not in branch_protection_repos:
                        branch_protection_repos[repo] = repo_rules[repo]

    def write_org_config(self, path: str):
        print(f"Writing org configuration to {path}")
        with open(path, "w") as stream:
            return yaml.safe_dump(self.org_cfg, stream)

    def write_branch_protection(self, path: str):
        print(f"Writing branch protection to {path}")
        with open(path, "w") as stream:
            return yaml.safe_dump(self.branch_protection, stream)

    @staticmethod
    def _yaml_load(stream: TextIO | str) -> dict[str, Any]:
        # safe_load + reject unique keys
        return yaml.load(stream, UniqueKeyLoader)

    @staticmethod
    def _read_yml_file(path: str):
        with open(path) as stream:
            return OrgGenerator._yaml_load(stream)

    @staticmethod
    def _read_wg_charter(path: str):
        print(f"Reading WG from {path}")
        with open(path) as stream:
            wg_charter = stream.read()
            wg = OrgGenerator._extract_wg_config(wg_charter)
            if not wg:
                wg = None
                print("... Ignoring. Missing yaml block with WG definition.")
            return wg

    _YAML_BLOCK_RE = re.compile("```yaml(.*)```", re.DOTALL)

    @staticmethod
    def _extract_wg_config(wg_charter: str):
        # extract (first) yaml block
        match = re.search(OrgGenerator._YAML_BLOCK_RE, wg_charter)
        return OrgGenerator._validate_wg(OrgGenerator._yaml_load(match.group(1))) if match else None

    @staticmethod
    def _empty_wg_config(name: str) -> dict[str, Any]:
        return {
            "name": name,
            "org": OrgGenerator._DEFAULT_ORG,
            "execution_leads": [],
            "technical_leads": [],
            "bots": [],
            "areas": [],
        }

    @staticmethod
    def _wg_github_users(wg: dict[str, Any]) -> set[str]:
        users = {u["github"] for u in wg["execution_leads"]}
        users |= {u["github"] for u in wg["technical_leads"]}
        users |= {u["github"] for u in wg["bots"]}
        for area in wg["areas"]:
            users |= {u["github"] for u in area["approvers"]}
            if "reviewers" in area:
                users |= {u["github"] for u in area["reviewers"]}
            if "bots" in area:
                users |= {u["github"] for u in area["bots"]}
        return users

    @staticmethod
    def _wg_github_users_leads(wg: dict[str, Any]) -> set[str]:
        users = {u["github"] for u in wg["execution_leads"]}
        users |= {u["github"] for u in wg["technical_leads"]}
        return users

    _CONTRIBUTORS_SCHEMA = {
        "type": "object",
        "properties": {
            "orgs": {
                "type": "object",
                "patternProperties": {
                    "^\\w+$": {
                        "type": "object",
                        "properties": {"contributors": {"type": "array", "items": {"type": "string"}}},
                        "required": ["contributors"],
                        "additionalProperties": False,
                    }
                },
                "additionalProperties": False,
            }
        },
        "required": ["orgs"],
        "additionalProperties": False,
    }

    @staticmethod
    def _validate_contributors(contributors: dict[str, Any]) -> dict[str, Any]:
        jsonschema.validate(contributors, OrgGenerator._CONTRIBUTORS_SCHEMA)
        # check that orgs are in _ORGS
        for org in contributors["orgs"]:
            if org not in OrgGenerator._MANAGED_ORGS:
                raise ValueError(f"Invalid org {org} in orgs.yml, expected one of {OrgGenerator._MANAGED_ORGS}")
        return contributors

    _WG_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "org": {"type": "string", "default": "cloudfoundry"},
            "execution_leads": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
            "technical_leads": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
            "bots": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
            "areas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "approvers": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
                        "reviewers": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
                        "bots": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
                        "repositories": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["name", "approvers", "repositories"],
                    "additionalProperties": False,
                },
            },
            "config": {"type": "object"},
        },
        "required": ["name", "execution_leads", "technical_leads", "bots", "areas"],
        "additionalProperties": False,
        "$defs": {
            "githubUser": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "github": {"type": "string"}},
                "required": ["name", "github"],
                "additionalProperties": False,
            }
        },
    }

    @staticmethod
    def _validate_wg(wg: dict[str, Any]) -> dict[str, Any]:
        jsonschema.validate(wg, OrgGenerator._WG_SCHEMA)
        # validate org and use 'cloudfoundry' if missing
        if "org" not in wg:
            wg["org"] = OrgGenerator._DEFAULT_ORG
        if wg["org"] not in OrgGenerator._MANAGED_ORGS:
            raise ValueError(f"Invalid org {wg['org']} in {wg['name']}, expected one of {OrgGenerator._MANAGED_ORGS}")
        return wg

    # schema for referenced fields only, not for complete config
    _GITHUB_ORG_CFG_SCHEMA = {
        "type": "object",
        "properties": {
            "orgs": {
                "type": "object",
                "patternProperties": {
                    "^\\w+$": {
                        "type": "object",
                        "properties": {
                            "admins": {"type": "array", "items": {"type": "string"}},
                            "members": {"type": "array", "items": {"type": "string"}},
                            "teams": {"type": "object"},
                        },
                        "required": ["admins", "members", "teams", "repos"],
                    },
                },
            },
        },
        "required": ["orgs"],
    }

    @staticmethod
    def _validate_github_org_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
        jsonschema.validate(cfg, OrgGenerator._GITHUB_ORG_CFG_SCHEMA)
        # check that orgs are in _ORGS
        for org in cfg["orgs"]:
            if org not in OrgGenerator._MANAGED_ORGS:
                raise ValueError(f"Invalid org {org} in orgs.yml, expected one of {OrgGenerator._MANAGED_ORGS}")
        return cfg

    # schema for referenced fields only, not for complete config
    _BRANCH_PROTECTION_SCHEMA = {
        "type": "object",
        "properties": {
            "branch-protection": {
                "type": "object",
                "properties": {
                    "orgs": {
                        "type": "object",
                        "patternProperties": {
                            "^\\w+$": {
                                "type": "object",
                                "properties": {
                                    "repos": {"type": "object"},
                                },
                                "required": ["repos"],
                            },
                        },
                    },
                },
                "required": ["orgs"],
            },
        },
        "required": ["branch-protection"],
    }

    @staticmethod
    def _validate_branch_protection(cfg: dict[str, Any]) -> dict[str, Any]:
        jsonschema.validate(cfg, OrgGenerator._BRANCH_PROTECTION_SCHEMA)
        # check that orgs are in _ORGS
        for org in cfg["branch-protection"]["orgs"]:
            if org not in OrgGenerator._MANAGED_ORGS:
                raise ValueError(f"Invalid org {org} in branchprotection.yml, expected one of {OrgGenerator._MANAGED_ORGS}")
        return cfg

    # https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0005-github-teams-and-access.md
    @staticmethod
    def _generate_wg_teams(wg: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        org = wg["org"]
        org_prefix = org + "/"
        org_prefix_len = len(org_prefix)
        name = OrgGenerator._kebab_case(f"wg-{wg['name']}")
        maintainers = {u["github"] for u in wg["execution_leads"]}
        maintainers |= {u["github"] for u in wg["technical_leads"]}
        approvers = {u["github"] for a in wg["areas"] for u in a["approvers"]}
        repositories = {r[org_prefix_len:] for a in wg["areas"] for r in a["repositories"] if r.startswith(org_prefix)}
        # WG team and teams for WG areas
        team: dict[str, Any] = {
            "description": f"Leads and approvers for {wg['name']} WG",
            "privacy": "closed",
            "maintainers": sorted(maintainers),
            "members": sorted(approvers - maintainers),
            "teams": {
                f"{name}-leads": {
                    "description": f"Leads for {wg['name']} WG",
                    "privacy": "closed",
                    "maintainers": sorted(maintainers),
                    "repos": {r: "admin" for r in repositories},
                },
                f"{name}-bots": {
                    "description": f"Bot accounts for {wg['name']} WG",
                    "privacy": "closed",
                    "maintainers": sorted(maintainers),
                    "members": sorted({u["github"] for u in wg["bots"]} - maintainers),
                    "repos": {r: "write" for r in repositories},
                },
            },
        }
        # approvers per area
        team["teams"] |= {
            OrgGenerator._kebab_case(f"{name}-{a['name']}-approvers"): {
                "description": f"Approvers for {wg['name']} WG, {a['name']} area",
                "privacy": "closed",
                "maintainers": sorted(maintainers),
                "members": sorted({u["github"] for u in a["approvers"]} - maintainers),
                "repos": {r[org_prefix_len:]: "write" for r in a["repositories"] if r.startswith(org_prefix)},
            }
            for a in wg["areas"]
        }
        # optional reviewers per area
        team["teams"] |= {
            OrgGenerator._kebab_case(f"{name}-{a['name']}-reviewers"): {
                "description": f"Reviewers for {wg['name']} WG, {a['name']} area",
                "privacy": "closed",
                "maintainers": sorted(maintainers),
                "members": sorted({u["github"] for u in a["reviewers"]} - maintainers),
                "repos": {r[org_prefix_len:]: "read" for r in a["repositories"] if r.startswith(org_prefix)},
            }
            for a in wg["areas"]
            if "reviewers" in a
        }
        # optional bots per area
        team["teams"] |= {
            OrgGenerator._kebab_case(f"{name}-{a['name']}-bots"): {
                "description": f"Bot accounts for {wg['name']} WG, {a['name']} area",
                "privacy": "closed",
                "maintainers": sorted(maintainers),
                "members": sorted({u["github"] for u in a["bots"]} - maintainers),
                "repos": {r[org_prefix_len:]: "write" for r in a["repositories"] if r.startswith(org_prefix)},
            }
            for a in wg["areas"]
            if "bots" in a
        }
        return (name, team)

    @staticmethod
    def _generate_toc_team(wg: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        org = wg["org"]
        org_prefix = org + "/"
        org_prefix_len = len(org_prefix)
        # assumption: TOC members are execution_leads
        repositories = {r[org_prefix_len:] for a in wg["areas"] for r in a["repositories"] if r.startswith(org_prefix)}
        team = {
            "description": wg["name"],
            "privacy": "closed",
            "maintainers": sorted({u["github"] for u in wg["execution_leads"]}),
            "repos": {r: "admin" for r in repositories},
        }
        return ("toc", team)

    @staticmethod
    def _generate_wg_leads_team(wgs: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
        members = {u for wg in wgs for u in OrgGenerator._wg_github_users_leads(wg)}
        team = {
            "description": "Technical and Execution Leads for all WGs",
            "privacy": "closed",
            "members": sorted(members),
        }
        return ("wg-leads", team)

    # https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0015-branch-protection.md
    # returns hash with branch protection rules per repo
    def _generate_wg_branch_protection(self, wg: dict[str, Any]) -> dict[str, Any]:
        org = wg["org"]
        org_prefix = org + "/"
        org_prefix_len = len(org_prefix)
        # count approvers per repo over all WG areas, TODO: repos shared between WGs?
        repos = {r[org_prefix_len:] for a in wg["areas"] for r in a["repositories"] if r.startswith(org_prefix)}
        wg_name = f"wg-{wg['name']}"
        wg_bots = OrgGenerator._kebab_case(f"{wg_name}-bots")
        return {
            repo: {
                "protect": True,
                "enforce_admins": True,
                "allow_force_pushes": False,
                "allow_deletions": False,
                "allow_disabled_policies": True,  # needed to allow branches w/o branch protection
                "include": [f"^{self._get_default_branch(org, repo)}$", "^v[0-9]*$"],
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True,
                    "required_approving_review_count": (
                        0
                        if len({u["github"] for a in wg["areas"] if org_prefix + repo in a["repositories"] for u in a["approvers"]}) < 4
                        else 1
                    ),
                    "bypass_pull_request_allowances": {
                        "teams": [wg_bots]  # wg bot team
                        + [
                            OrgGenerator._kebab_case(f"{wg_name}-{a['name']}-bots")
                            for a in wg["areas"]
                            if org_prefix + repo in a["repositories"] and "bots" in a and len(a["bots"]) > 0
                        ]  # area bot teams
                    },
                },
            }
            for repo in repos
        }

    def _get_default_branch(self, org: str, repo: str) -> str:
        # https://github.com/organizations/cloudfoundry/settings/repository-defaults - Repository default branch = main (for new repos)
        # But in orgs.yml: all repos w/o default_branch use master (data was generated by peribolos)
        # https://github.com/kubernetes/test-infra/blob/master/prow/config/org/org.go#L173
        # Looks like trouble ahead. Should not create new repos w/o default_branch setting.
        return self.org_cfg["orgs"][org]["repos"].get(repo, {}).get("default_branch", "master")

    _KEBAB_CASE_RE = re.compile(r"[\W_]+")

    @staticmethod
    def _kebab_case(name: str) -> str:
        # kebab case = lower case and all special chars replaced by dash
        # no leading, trailing or double dashes
        return OrgGenerator._KEBAB_CASE_RE.sub("-", name.lower()).strip("-")
