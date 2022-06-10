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
from typing import Set, List, Optional

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


class OrgGenerator:
    # parameters intended for testing only, all params are yaml docs
    def __init__(
        self,
        static_org_cfg: Optional[str] = None,
        contributors: Optional[str] = None,
        toc: Optional[str] = None,
        working_groups: Optional[List[str]] = None,
    ):
        self.org_cfg = yaml.safe_load(static_org_cfg) if static_org_cfg else {"orgs": {"cloudfoundry": {"admins": [], "members": []}}}
        OrgGenerator._validate_github_org_cfg(self.org_cfg)
        self.contributors = (
            set(OrgGenerator._validate_contributors(yaml.safe_load(contributors))["contributors"]) if contributors else set()
        )
        self.toc = yaml.safe_load(toc) if toc else OrgGenerator._empty_wg_config("TOC")
        OrgGenerator._validate_wg(self.toc)
        self.working_groups = [OrgGenerator._validate_wg(yaml.safe_load(wg)) for wg in working_groups] if working_groups else []

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

        # working group charters (including TOC)
        self.toc = OrgGenerator._read_wg_charter(f"{_SCRIPT_PATH}/../toc/TOC.md")
        for wg_file in glob.glob(f"{_SCRIPT_PATH}/../toc/working-groups/*.md"):
            if not wg_file.endswith("/WORKING-GROUPS.md"):
                self.working_groups.append(OrgGenerator._read_wg_charter(wg_file))

    def generate_org_members(self):
        org_members = set(self.org_cfg["orgs"]["cloudfoundry"]["members"])  # just in case, should be empty list
        org_members |= self.contributors
        for wg in self.working_groups:
            org_members |= OrgGenerator._wg_github_users(wg)
        org_admins = OrgGenerator._wg_github_users(self.toc)
        org_admins |= set(self.org_cfg["orgs"]["cloudfoundry"]["admins"])
        org_members = org_members - org_admins
        self.org_cfg["orgs"]["cloudfoundry"]["members"] = sorted(org_members)

    def write_org_config(self, path: str):
        print(f"Writing org configuration to {path}")
        with open(path, "w") as stream:
            return yaml.safe_dump(self.org_cfg, stream)

    @staticmethod
    def _read_yml_file(path: str):
        with open(path, "r") as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def _read_wg_charter(path: str):
        print(f"Reading WG from {path}")
        with open(path, "r") as stream:
            wg_charter = stream.read()
            wg = OrgGenerator._extract_wg_config(wg_charter)
            if not wg:
                wg = OrgGenerator._empty_wg_config(path)
                print("... Ignoring. Missing yaml block with WG definition.")
            return wg

    _YAML_BLOCK_RE = re.compile("```yaml(.*)```", re.DOTALL)

    @staticmethod
    def _extract_wg_config(wg_charter: str):
        # extract (first) yaml block
        match = re.search(OrgGenerator._YAML_BLOCK_RE, wg_charter)
        return OrgGenerator._validate_wg(yaml.safe_load(match.group(1))) if match else None

    @staticmethod
    def _empty_wg_config(name: str):
        return {
            "name": name,
            "execution_leads": [],
            "technical_leads": [],
            "areas": [],
        }

    @staticmethod
    def _wg_github_users(wg) -> Set[str]:
        users = {u["github"] for u in wg["execution_leads"]}
        users |= {u["github"] for u in wg["technical_leads"]}
        for area in wg["areas"]:
            users |= {u["github"] for u in area["approvers"]}
        return users

    _CONTRIBUTORS_SCHEMA = {
        "type": "object",
        "properties": {"contributors": {"type": "array", "items": {"type": "string"}}},
        "required": ["contributors"],
        "additionalProperties": False
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
            "areas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "approvers": {"type": "array", "items": {"$ref": "#/$defs/githubUser"}},
                        "repositories": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["name", "approvers", "repositories"],
                    "additionalProperties": False
                },
            },
            "config": {"type": "object"}
        },
        "required": ["name", "execution_leads", "technical_leads", "areas"],
        "additionalProperties": False,
        "$defs": {
            "githubUser": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "github": {"type": "string"}},
                "required": ["name", "github"],
                "additionalProperties": False
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
                        },
                        "required": ["admins", "members"],
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloud Foundry Org Generator")
    parser.add_argument("-o", "--out", default="cloudfoundry.out.yml", help="output file for generated org configuration")
    args = parser.parse_args()

    print("Generating cloudfoundry org configuration.")
    generator = OrgGenerator()
    generator.load_from_project()
    generator.generate_org_members()
    generator.write_org_config(args.out)
