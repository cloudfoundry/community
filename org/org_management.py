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
        self.org_cfg = yaml.safe_load(static_org_cfg) if static_org_cfg else {"orgs": {"cloudfoundry": {"members": []}}}
        self.contributors = set(yaml.safe_load(contributors)["contributors"]) if contributors else set()
        self.toc = OrgGenerator._extract_wg_config(toc) if toc else OrgGenerator._empty_wg_config("TOC")
        self.working_groups = [yaml.safe_load(wg) for wg in working_groups] if working_groups else []

    def load_from_project(self):
        path = f"{_SCRIPT_PATH}/cloudfoundry.yml"
        print(f"Reading static org configuration from {path}")
        self.org_cfg = OrgGenerator._read_yml_file(path)

        path = f"{_SCRIPT_PATH}/contributors.yml"
        if os.path.exists(path):
            print(f"Reading contributors from {path}")
            contributors_yaml = OrgGenerator._read_yml_file(path)
            self.contributors = set(contributors_yaml["contributors"])

        # working group charters (including TOC)
        self.toc = OrgGenerator._read_wg_charter(f"{_SCRIPT_PATH}/../toc/TOC.md")
        for wg_file in glob.glob(f"{_SCRIPT_PATH}/../toc/working-groups/*.md"):
            if not wg_file.endswith("/WORKING-GROUPS.md"):
                self.working_groups.append(OrgGenerator._read_wg_charter(wg_file))

    def generate_org_members(self):
        org_members = set(self.org_cfg["orgs"]["cloudfoundry"]["members"])  # just in case, should be empty list
        org_members |= self.contributors
        org_members |= OrgGenerator._wg_github_users(self.toc)
        for wg in self.working_groups:
            org_members |= OrgGenerator._wg_github_users(wg)
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
        # TODO: some validation of wg definition
        return yaml.safe_load(match.group(1)) if match else None

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
        if "technical_leads" in wg:
            users |= {u["github"] for u in wg["technical_leads"]}
        for area in wg["areas"]:
            if "approvers" in area and isinstance(area["approvers"], list):
                users |= {u["github"] for u in area["approvers"]}
        return users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloud Foundry Org Generator")
    parser.add_argument("-o", "--out", default="cloudfoundry.out.yml", help="output file for generated org configuration")
    args = parser.parse_args()

    print("Generating cloudfoundry org configuration.")
    generator = OrgGenerator()
    generator.load_from_project()
    generator.generate_org_members()
    generator.write_org_config(args.out)
