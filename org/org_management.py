# Generates cloudfound org configuration for Peribolos from:
# - a static configuration: cloudfoundry.yml
# - a contributors list: contributors.yml
# - the WG charters: ../toc/working-groups/*.md (yaml block)
# - the TOC charter: ../toc/TOC.md (yaml block)
#
# See readme.md

import glob
import yaml
import re
import os
import argparse
import jsonschema
from typing import Any, Dict, Set, List, Optional, Tuple

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


# pyyaml silently ignores duplicate keys but they shall be rejected
# https://yaml.org/spec/1.2.2/ requires unique keys
class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.MarkedYAMLError(f"Duplicate key {key!r} found.", key_node.start_mark)
            mapping.add(key)
        return super().construct_mapping(node, deep)


class OrgGenerator:
    # parameters intended for testing only, all params are yaml docs
    def __init__(
        self,
        static_org_cfg: Optional[str] = None,
        contributors: Optional[str] = None,
        toc: Optional[str] = None,
        working_groups: Optional[List[str]] = None,
        branch_protection: Optional[str] = None,
    ):
        self.org_cfg = (
            OrgGenerator._yaml_load(static_org_cfg)
            if static_org_cfg
            else {"orgs": {"cloudfoundry": {"admins": [], "members": [], "teams": {}, "repos": {}}}}
        )
        OrgGenerator._validate_github_org_cfg(self.org_cfg)
        self.contributors = (
            set(OrgGenerator._validate_contributors(OrgGenerator._yaml_load(contributors))["contributors"]) if contributors else set()
        )
        self.toc = OrgGenerator._yaml_load(toc) if toc else OrgGenerator._empty_wg_config("TOC")
        OrgGenerator._validate_wg(self.toc)
        self.working_groups = [OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg)) for wg in working_groups] if working_groups else []
        self.branch_protection = (
            OrgGenerator._yaml_load(branch_protection)
            if branch_protection
            else {"branch-protection": {"orgs": {"cloudfoundry": {"repos": {}}}}}
        )
        OrgGenerator._validate_branch_protection(self.branch_protection)

    def load_from_project(self):
        path = f"{_SCRIPT_PATH}/cloudfoundry.yml"
        print(f"Reading static org configuration from {path}")
        self.org_cfg = OrgGenerator._validate_github_org_cfg(OrgGenerator._read_yml_file(path))

        path = f"{_SCRIPT_PATH}/contributors.yml"
        if os.path.exists(path):
            print(f"Reading contributors from {path}")
            contributors_yaml = OrgGenerator._read_yml_file(path)
            OrgGenerator._validate_contributors(contributors_yaml)
            self.contributors = set(contributors_yaml["contributors"])

        path = f"{_SCRIPT_PATH}/branchprotection.yml"
        print(f"Reading branch protection configuration from {path}")
        self.branch_protection = OrgGenerator._validate_branch_protection(OrgGenerator._read_yml_file(path))

        # working group charters (including TOC and ADMIN), ignore WGs without yaml block
        self.toc = OrgGenerator._read_wg_charter(f"{_SCRIPT_PATH}/../toc/TOC.md")
        wg_files = glob.glob(f"{_SCRIPT_PATH}/../toc/working-groups/*.md")
        wg_files += glob.glob(f"{_SCRIPT_PATH}/../toc/ADMIN.md")
        for wg_file in wg_files:
            if not wg_file.endswith("/WORKING-GROUPS.md"):
                wg = OrgGenerator._read_wg_charter(wg_file)
                if wg:
                    self.working_groups.append(wg)

    def get_contributors(self) -> Set[str]:
        return set(self.contributors)

    def get_community_members_with_role_by_wg(self) -> Dict[str, Set[str]]:
        result = dict()
        result["toc"] = set(self.toc)
        for wg in self.working_groups:
            result[wg["name"]] = OrgGenerator._wg_github_users(wg)
        return result

    def generate_org_members(self):
        org_members = set(self.org_cfg["orgs"]["cloudfoundry"]["members"])  # just in case, should be empty list
        org_members |= self.contributors
        for wg in self.working_groups:
            org_members |= OrgGenerator._wg_github_users(wg)
        org_admins = set(self.org_cfg["orgs"]["cloudfoundry"]["admins"])
        org_admins |= OrgGenerator._wg_github_users_leads(self.toc)
        org_members = org_members - org_admins
        self.org_cfg["orgs"]["cloudfoundry"]["members"] = sorted(org_members)
        self.org_cfg["orgs"]["cloudfoundry"]["admins"] = sorted(org_admins)

    def generate_teams(self):
        # overwrites any teams in cloudfoundry.yml that match a generated team name according to RFC-0005
        # working group teams
        for wg in self.working_groups:
            (name, team) = OrgGenerator._generate_wg_teams(wg)
            self.org_cfg["orgs"]["cloudfoundry"]["teams"][name] = team
        # toc team
        (name, team) = OrgGenerator._generate_toc_team(self.toc)
        self.org_cfg["orgs"]["cloudfoundry"]["teams"][name] = team
        # wg-leads team
        (name, team) = OrgGenerator._generate_wg_leads_team(self.working_groups)
        self.org_cfg["orgs"]["cloudfoundry"]["teams"][name] = team

    def generate_branch_protection(self):
        # basis is static config in self.branch_protection which is never overwritten
        # generate RFC0015 branch protection rules for every WG+TOC that opted in
        branch_protection_repos = self.branch_protection["branch-protection"]["orgs"]["cloudfoundry"]["repos"]
        for wg in self.working_groups + [self.toc]:
            if wg.get("config", {}).get("generate_rfc0015_branch_protection_rules", False):  # config is optional
                repo_rules = self._generate_wb_branch_protection(wg)
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
    def _yaml_load(stream):
        # safe_load + reject unique keys
        return yaml.load(stream, UniqueKeyLoader)

    @staticmethod
    def _read_yml_file(path: str):
        with open(path, "r") as stream:
            return OrgGenerator._yaml_load(stream)

    @staticmethod
    def _read_wg_charter(path: str):
        print(f"Reading WG from {path}")
        with open(path, "r") as stream:
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
    def _empty_wg_config(name: str):
        return {
            "name": name,
            "execution_leads": [],
            "technical_leads": [],
            "bots": [],
            "areas": [],
        }

    @staticmethod
    def _wg_github_users(wg) -> Set[str]:
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
    def _wg_github_users_leads(wg) -> Set[str]:
        users = {u["github"] for u in wg["execution_leads"]}
        users |= {u["github"] for u in wg["technical_leads"]}
        return users

    _CONTRIBUTORS_SCHEMA = {
        "type": "object",
        "properties": {"contributors": {"type": "array", "items": {"type": "string"}}},
        "required": ["contributors"],
        "additionalProperties": False,
    }

    @staticmethod
    def _validate_contributors(contributors):
        jsonschema.validate(contributors, OrgGenerator._CONTRIBUTORS_SCHEMA)
        return contributors

    _WG_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
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
    def _validate_wg(wg):
        jsonschema.validate(wg, OrgGenerator._WG_SCHEMA)
        return wg

    # schema for referenced fields only, not for complete config
    _GITHUB_ORG_CFG_SCHEMA = {
        "type": "object",
        "properties": {
            "orgs": {
                "type": "object",
                "properties": {
                    "cloudfoundry": {
                        "type": "object",
                        "properties": {
                            "admins": {"type": "array", "items": {"type": "string"}},
                            "members": {"type": "array", "items": {"type": "string"}},
                            "teams": {"type": "object"},
                        },
                        "required": ["admins", "members", "teams", "repos"],
                    },
                },
                "required": ["cloudfoundry"],
            },
        },
        "required": ["orgs"],
    }

    @staticmethod
    def _validate_github_org_cfg(cfg):
        jsonschema.validate(cfg, OrgGenerator._GITHUB_ORG_CFG_SCHEMA)
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
                        "properties": {
                            "cloudfoundry": {
                                "type": "object",
                                "properties": {
                                    "repos": {"type": "object"},
                                },
                                "required": ["repos"],
                            },
                        },
                        "required": ["cloudfoundry"],
                    },
                },
                "required": ["orgs"],
            },
        },
        "required": ["branch-protection"],
    }

    @staticmethod
    def _validate_branch_protection(cfg):
        jsonschema.validate(cfg, OrgGenerator._BRANCH_PROTECTION_SCHEMA)
        return cfg

    _CF_ORG_PREFIX = "cloudfoundry/"
    _CF_ORG_PREFIX_LEN = len(_CF_ORG_PREFIX)

    # https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0005-github-teams-and-access.md
    @staticmethod
    def _generate_wg_teams(wg) -> Tuple[str, Dict[str, Any]]:
        name = OrgGenerator._kebab_case(f"wg-{wg['name']}")
        maintainers = {u["github"] for u in wg["execution_leads"]}
        maintainers |= {u["github"] for u in wg["technical_leads"]}
        approvers = {u["github"] for a in wg["areas"] for u in a["approvers"]}
        repositories = {
            r[OrgGenerator._CF_ORG_PREFIX_LEN :]
            for a in wg["areas"]
            for r in a["repositories"]
            if r.startswith(OrgGenerator._CF_ORG_PREFIX)
        }
        # WG team and teams for WG areas
        team = {
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
                "repos": {
                    r[OrgGenerator._CF_ORG_PREFIX_LEN :]: "write" for r in a["repositories"] if r.startswith(OrgGenerator._CF_ORG_PREFIX)
                },
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
                "repos": {
                    r[OrgGenerator._CF_ORG_PREFIX_LEN :]: "read" for r in a["repositories"] if r.startswith(OrgGenerator._CF_ORG_PREFIX)
                },
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
                "repos": {
                    r[OrgGenerator._CF_ORG_PREFIX_LEN :]: "write" for r in a["repositories"] if r.startswith(OrgGenerator._CF_ORG_PREFIX)
                },
            }
            for a in wg["areas"]
            if "bots" in a
        }
        return (name, team)

    @staticmethod
    def _generate_toc_team(wg) -> Tuple[str, Dict[str, Any]]:
        # assumption: TOC members are execution_leads
        repositories = {
            r[OrgGenerator._CF_ORG_PREFIX_LEN :]
            for a in wg["areas"]
            for r in a["repositories"]
            if r.startswith(OrgGenerator._CF_ORG_PREFIX)
        }
        team = {
            "description": wg["name"],
            "privacy": "closed",
            "maintainers": sorted({u["github"] for u in wg["execution_leads"]}),
            "repos": {r: "admin" for r in repositories},
        }
        return ("toc", team)

    @staticmethod
    def _generate_wg_leads_team(wgs: List[Any]) -> Tuple[str, Dict[str, Any]]:
        # RFC-0005 lists community repo explicitly (not all TOC repos)
        repositories = {"community"}  # without cloudfoundry/ prefix
        members = {u for wg in wgs for u in OrgGenerator._wg_github_users_leads(wg)}
        team = {
            "description": "Technical and Execution Leads for all WGs",
            "privacy": "closed",
            "members": sorted(members),
            "repos": {r: "write" for r in repositories},
        }
        return ("wg-leads", team)

    # https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0015-branch-protection.md
    # returns hash with branch protection rules per repo
    def _generate_wb_branch_protection(self, wg) -> Dict[str, Any]:
        # count approvers per repo over all WG areas, TODO: repos shared between WGs?
        repos = {
            r[OrgGenerator._CF_ORG_PREFIX_LEN :]
            for a in wg["areas"]
            for r in a["repositories"]
            if r.startswith(OrgGenerator._CF_ORG_PREFIX)
        }
        wg_name = f"wg-{wg['name']}"
        wg_bots = OrgGenerator._kebab_case(f"{wg_name}-bots")
        return {
            repo: {
                "protect": True,
                "enforce_admins": True,
                "allow_force_pushes": False,
                "allow_deletions": False,
                "allow_disabled_policies": True,  # needed to allow branches w/o branch protection
                "include": [f"^{self._get_default_branch(repo)}$", "^v[0-9]*$"],
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True,
                    "required_approving_review_count": 0
                    if len(
                        {
                            u["github"]
                            for a in wg["areas"]
                            if OrgGenerator._CF_ORG_PREFIX + repo in a["repositories"]
                            for u in a["approvers"]
                        }
                    )
                    < 4
                    else 1,
                    "bypass_pull_request_allowances": {
                        "teams": [wg_bots]  # wg bot team
                        + [
                            OrgGenerator._kebab_case(f"{wg_name}-{a['name']}-bots")
                            for a in wg["areas"]
                            if OrgGenerator._CF_ORG_PREFIX + repo in a["repositories"] and "bots" in a and len(a["bots"]) > 0
                        ]  # area bot teams
                    },
                },
            }
            for repo in repos
        }

    def _get_default_branch(self, repo: str) -> str:
        # https://github.com/organizations/cloudfoundry/settings/repository-defaults - Repository default branch = main (for new repos)
        # But in cloudfoundry.yml: all repos w/o default_branch use master (data was generated by peribolos)
        # https://github.com/kubernetes/test-infra/blob/master/prow/config/org/org.go#L173
        # Looks like trouble ahead. Should not create new repos w/o default_branch setting.
        return self.org_cfg["orgs"]["cloudfoundry"]["repos"].get(repo, {}).get("default_branch", "master")

    _KEBAB_CASE_RE = re.compile(r"[\W_]+")

    @staticmethod
    def _kebab_case(name: str) -> str:
        # kebab case = lower case and all special chars replaced by dash
        # no leading, trailing or double dashes
        return OrgGenerator._KEBAB_CASE_RE.sub("-", name.lower()).strip("-")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloud Foundry Org Generator")
    parser.add_argument("-o", "--out", default="cloudfoundry.out.yml", help="output file for generated org configuration")
    parser.add_argument(
        "-b", "--branchprotection", default="branchprotection.out.yml", help="output file for generated branch protection rules"
    )
    args = parser.parse_args()

    print("Generating cloudfoundry org configuration.")
    generator = OrgGenerator()
    generator.load_from_project()
    generator.generate_org_members()
    generator.generate_teams()
    generator.generate_branch_protection()
    generator.write_org_config(args.out)
    generator.write_branch_protection(args.branchprotection)
