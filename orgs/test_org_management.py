import unittest
import yaml
import jsonschema
from org_management import OrgGenerator

org_cfg = """
---
orgs:
  cloudfoundry:
    admins:
    - admin1
    members:
    - member1
    teams: {}
    repos:
      repo1:
        default_branch: main
      repo3:
        default_branch: defbranch
"""

org_cfg_multiple = """
---
orgs:
  cloudfoundry:
    admins:
    - admin1
    members:
    - member1
    teams: {}
    repos:
      repo1:
        default_branch: main
      repo3:
        default_branch: defbranch
  cloudfoundry2:
    admins:
    - admin2
    members:
    - member2
    teams: {}
    repos:
      repo1:
        default_branch: main
      repo3:
        default_branch: defbranch
"""

wg1 = """
name: WG1 Name
execution_leads:
- name: Execution Lead WG1
  github: execution-lead-wg1
technical_leads:
- name: Technical Lead WG1
  github: technical-lead-wg1
bots:
- name: WG1 CI Bot
  github: bot1-wg1
areas:
- name: Area 1
  approvers:
  - github: approver1-wg1-a1
    name: User 1
  - github: approver2-wg1-a1-a2
    name: User 2
  repositories:
  - cloudfoundry/repo1
  - cloudfoundry/repo2
- name: Area 2
  approvers:
  - github: approver2-wg1-a1-a2
    name: User 2
  - github: approver3-wg1-a2
    name: User 3
  reviewers:
  - github: reviewer1-wg1-a2
    name: User 4
  bots:
  - github: bot2-wg1-a2
    name: WG1 Area2 Bot
  repositories:
  - cloudfoundry/repo3
  - cloudfoundry/repo4
"""

wg2 = """
name: WG2 Name
execution_leads:
- name: Execution Lead WG2
  github: execution-lead-wg2
technical_leads:
- name: Technical Lead WG2
  github: technical-lead-wg2
bots: []
areas:
- name: Area 1
  approvers:
  - github: approver1-wg2-a1
    name: User 10
  repositories:
  - cloudfoundry/repo10
  - cloudfoundry/repo11
  - non-cloudfoundry/repo12
"""

# for testing branch protection, different number of approvers, repos in multiple areas
wg3 = """
name: WG3 Name
execution_leads:
- name: Execution Lead WG3
  github: execution-lead-wg3
technical_leads:
- name: Technical Lead WG3
  github: technical-lead-wg3
bots: []
areas:
- name: Area 1
  approvers: []
  repositories:
  - cloudfoundry/repo1
  - cloudfoundry/repo2
  - non-cloudfoundry/repo12
- name: Area 2
  approvers:
  - github: u1
    name: User 1
  - github: u2
    name: User 2
  repositories:
  - cloudfoundry/repo2
  - cloudfoundry/repo3
- name: Area 3
  approvers:
  - github: u3
    name: User 3
  - github: u4
    name: User 4
  repositories:
  - cloudfoundry/repo3
  - cloudfoundry/repo4
- name: Area 4
  approvers:
  - github: u1
    name: User 1
  - github: u2
    name: User 2
  - github: u3
    name: User 3
  - github: u4
    name: User 4
  repositories:
  - cloudfoundry/repo4
  - cloudfoundry/repo5
- name: Area 5
  approvers:
  - github: u1
    name: User 1
  - github: u2
    name: User 2
  repositories:
  - cloudfoundry/repo2
  - cloudfoundry/repo5
  bots:
  - github: bot-wg1-a5
    name: WG3 Area5 Bot
config:
  generate_rfc0015_branch_protection_rules: true
"""

wg4_other_org = """
name: WG4 Name
org: cloudfoundry2
execution_leads:
- name: Execution Lead WG4
  github: execution-lead-wg4
technical_leads:
- name: Technical Lead WG4
  github: technical-lead-wg4
bots:
- name: WG4 CI Bot
  github: bot1-wg4
areas:
- name: Area 1
  approvers:
  - github: approver1-wg4-a1
    name: User 1
  - github: approver2-wg4-a1-a2
    name: User 2
  repositories:
  - cloudfoundry2/repo1
  - cloudfoundry2/repo2
- name: Area 2
  approvers:
  - github: approver2-wg4-a1-a2
    name: User 2
  - github: approver3-wg4-a2
    name: User 3
  reviewers:
  - github: reviewer1-wg4-a2
    name: User 4
  bots:
  - github: bot2-wg4-a2
    name: WG4 Area2 Bot
  repositories:
  - cloudfoundry2/repo3
  - cloudfoundry2/repo4
  - cloudfoundry/repo5
config:
  generate_rfc0015_branch_protection_rules: true
"""

toc = """
name: Technical Oversight Committee
execution_leads:
- name: TOC Member 1
  github: toc-member-1
- name: TOC Member 2
  github: toc-member-2
technical_leads:
- name: TOC Tech Lead 1
  github: toc-tech-lead-1
bots:
- name: TOC bot
  github: toc-bot
areas:
- name: CloudFoundry Community
  approvers:
  - name: User TOC
    github: approver-toc-a1
  repositories:
  - cloudfoundry/community
config:
  generate_rfc0015_branch_protection_rules: true
  github_project_sync:
    mapping:
      cloudfoundry: 31
"""

contributors = """
orgs:
  cloudfoundry:
    contributors:
    - contributor1
    - Contributor2
"""

contributors_multiple_orgs = """
orgs:
  cloudfoundry:
    contributors:
    - contributor1
    - contributor2
  cloudfoundry2:
    contributors:
    - contributor2
    - contributor3
    - contributor4
"""

branch_protection = """
branch-protection:
  orgs:
    cloudfoundry:
      repos:
        repo1:
          protect: true
"""

branch_protection_multiple_orgs = """
branch-protection:
  orgs:
    cloudfoundry:
      repos:
        repo1:
          protect: true
    cloudfoundry2:
      repos:
        repo1:
          protect: true
"""


class TestOrgGenerator(unittest.TestCase):
    def setUp(self) -> None:
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry"]

    def test_empty_org(self):
        o = OrgGenerator()
        o.generate_org_members()
        self.assertListEqual([], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_org_members_contributors(self):
        o = OrgGenerator(contributors=contributors)
        o.generate_org_members()
        self.assertListEqual(["Contributor2", "contributor1"], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_org_members_wg(self):
        o = OrgGenerator(working_groups=[wg1, wg2])
        o.generate_org_members()
        members = o.org_cfg["orgs"]["cloudfoundry"]["members"]
        self.assertEqual(8 + 3, len(members))
        self.assertIn("execution-lead-wg1", members)
        self.assertIn("approver1-wg1-a1", members)
        self.assertIn("reviewer1-wg1-a2", members)
        self.assertIn("bot1-wg1", members)
        self.assertIn("bot2-wg1-a2", members)
        self.assertIn("approver1-wg2-a1", members)

    def test_org_admins_cannot_be_org_members(self):
        contributors = """
          orgs:
            cloudfoundry:
              contributors:
              - contributor1
              - Contributor2
              - admin1
        """
        o = OrgGenerator(static_org_cfg=org_cfg, contributors=contributors)
        o.generate_org_members()
        self.assertListEqual(["admin1"], o.org_cfg["orgs"]["cloudfoundry"]["admins"])
        self.assertListEqual(["Contributor2", "contributor1", "member1"], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_toc_members_are_org_admins(self):
        contributors = """
          orgs:
            cloudfoundry:
              contributors:
              - contributor1
              - Contributor2
              - toc-member-1
              - toc-member-2
        """
        o = OrgGenerator(toc=toc, contributors=contributors)
        o.generate_org_members()
        # bots and toc area approvers shall not be org admins
        self.assertListEqual(["toc-member-1", "toc-member-2", "toc-tech-lead-1"], o.org_cfg["orgs"]["cloudfoundry"]["admins"])
        # being org admins, toc members can't be org members
        self.assertListEqual(["Contributor2", "contributor1"], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_org_members_multiple_orgs(self):
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        o = OrgGenerator(contributors=contributors_multiple_orgs, toc=toc, working_groups=[wg1, wg2, wg4_other_org])
        o.generate_org_members()
        # 2 contributors, 8 wg1, 3 wg2, 2 wg-leads of cloudfoundry2
        self.assertEqual(2 + 8 + 3 + 2, len(o.org_cfg["orgs"]["cloudfoundry"]["members"]))
        # 3 toc
        self.assertEqual(3, len(o.org_cfg["orgs"]["cloudfoundry"]["admins"]))

        # 3 contributors, 8 wg4_other_org
        self.assertEqual(3 + 8, len(o.org_cfg["orgs"]["cloudfoundry2"]["members"]))
        # 3 toc
        self.assertEqual(3, len(o.org_cfg["orgs"]["cloudfoundry2"]["admins"]))

    def test_extract_wg_config(self):
        self.assertIsNone(OrgGenerator._extract_wg_config(""))
        wg = OrgGenerator._extract_wg_config(f"bla bla ```yaml {wg1} ```")
        assert wg is not None
        self.assertEqual("WG1 Name", wg["name"])

    def test_wg_github_users(self):
        wg = OrgGenerator._yaml_load(wg1)
        users = OrgGenerator._wg_github_users(wg)
        self.assertEqual(8, len(users))
        self.assertIn("execution-lead-wg1", users)
        self.assertIn("technical-lead-wg1", users)
        self.assertIn("approver1-wg1-a1", users)
        self.assertIn("reviewer1-wg1-a2", users)
        self.assertIn("bot1-wg1", users)
        self.assertIn("bot2-wg1-a2", users)

    def test_wg_github_users_leads(self):
        wg = OrgGenerator._yaml_load(wg1)
        users = OrgGenerator._wg_github_users_leads(wg)
        self.assertSetEqual({"execution-lead-wg1", "technical-lead-wg1"}, users)

    def test_validate_yaml_unique_keys(self):
        with self.assertRaises(yaml.MarkedYAMLError):
            yml = """
            key: 1
            key: 2
            """
            OrgGenerator._yaml_load(yml)

    def test_validate_contributors(self):
        OrgGenerator._validate_contributors({"orgs": {"cloudfoundry": {"contributors": []}}})
        OrgGenerator._validate_contributors(OrgGenerator._yaml_load(contributors))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_contributors({})
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_contributors({"contributors": 1})

        # multiple orgs
        with self.assertRaises(ValueError):
            OrgGenerator._validate_contributors(OrgGenerator._yaml_load(contributors_multiple_orgs))
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        OrgGenerator._validate_contributors(OrgGenerator._yaml_load(contributors_multiple_orgs))

    def test_validate_wg(self):
        wg = OrgGenerator._validate_wg(OrgGenerator._empty_wg_config("wg"))
        self.assertEqual("wg", wg["name"])
        self.assertEqual("cloudfoundry", wg["org"])
        wg = OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg1))
        self.assertEqual("cloudfoundry", wg["org"])
        wg = OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg2))
        wg = OrgGenerator._validate_wg(OrgGenerator._yaml_load(toc))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_wg({})
        with self.assertRaises(jsonschema.ValidationError):
            wg = """
                name: WG1 Name
                execution_leads: []
                technical_leads: []
                areas:
                - name: Area 1
                  approvers: x
                  repositories: 1
            """
            OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg))
        with self.assertRaises(jsonschema.ValidationError):
            wg = """
                name: WG1 Name
                execution_leads: []
                technical_leads: []
                areas:
                - name: Area 1
                  approvers: []
                  repositories: []
                  notAllowed: 1
            """
            OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg))

        # multiple orgs
        with self.assertRaises(ValueError):
            OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg4_other_org))
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        wg = OrgGenerator._validate_wg(OrgGenerator._yaml_load(wg4_other_org))
        self.assertEqual("cloudfoundry2", wg["org"])

    def test_validate_github_org_cfg(self):
        OrgGenerator._validate_github_org_cfg(OrgGenerator._yaml_load(org_cfg))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_github_org_cfg({})

        # multiple orgs
        with self.assertRaises(ValueError):
            OrgGenerator._validate_github_org_cfg(OrgGenerator._yaml_load(org_cfg_multiple))
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        OrgGenerator._validate_github_org_cfg(OrgGenerator._yaml_load(org_cfg_multiple))

    def test_kebab_case(self):
        self.assertEqual("", OrgGenerator._kebab_case(""))
        self.assertEqual("wg-a-b-c-d-e", OrgGenerator._kebab_case("wg-a b_c-d  e"))
        self.assertEqual("wg-a-b-c", OrgGenerator._kebab_case(":wg-a (b)/?=c "))
        self.assertEqual("wg-app-runtime-deployments", OrgGenerator._kebab_case("wg-App Runtime Deployments"))
        self.assertEqual(
            "wg-app-runtime-deployments-cf-deployments-approvers",
            OrgGenerator._kebab_case("wg-App Runtime Deployments-CF Deployments-approvers"),
        )
        self.assertEqual(
            "wg-foundational-infrastructure-integrated-databases-mysql-postgres-approvers",
            OrgGenerator._kebab_case("wg-Foundational Infrastructure-Integrated Databases (Mysql / Postgres)-approvers"),
        )

    def test_validate_repo_ownership(self):
        o = OrgGenerator(static_org_cfg=org_cfg, toc=toc, working_groups=[wg1])
        self.assertTrue(o.validate_repo_ownership())
        o = OrgGenerator(static_org_cfg=org_cfg, toc=toc, working_groups=[wg1, wg2])
        self.assertTrue(o.validate_repo_ownership())
        o = OrgGenerator(static_org_cfg=org_cfg, toc=toc, working_groups=[wg3])
        self.assertTrue(o.validate_repo_ownership())
        o = OrgGenerator(static_org_cfg=org_cfg, toc=toc, working_groups=[wg1, wg2, wg3])
        self.assertFalse(o.validate_repo_ownership())

    def test_generate_wg_teams(self):
        _wg1 = OrgGenerator._yaml_load(wg1)
        OrgGenerator._validate_wg(_wg1)
        (name, wg_team) = OrgGenerator._generate_wg_teams(_wg1)

        self.assertEqual("wg-wg1-name", name)
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], wg_team["maintainers"])
        self.assertListEqual(["approver1-wg1-a1", "approver2-wg1-a1-a2", "approver3-wg1-a2"], wg_team["members"])

        team = wg_team["teams"]["wg-wg1-name-leads"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertDictEqual({f"repo{i}": "admin" for i in range(1, 5)}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-bots"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertListEqual(["bot1-wg1"], team["members"])
        self.assertDictEqual({f"repo{i}": "write" for i in range(1, 5)}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-area-1-approvers"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertListEqual(["approver1-wg1-a1", "approver2-wg1-a1-a2"], team["members"])
        self.assertDictEqual({"repo1": "write", "repo2": "write"}, team["repos"])

        self.assertNotIn("wg-wg1-name-area-1-reviewers", wg_team["teams"])
        self.assertNotIn("wg-wg1-name-area-1-bots", wg_team["teams"])

        team = wg_team["teams"]["wg-wg1-name-area-2-approvers"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertListEqual(["approver2-wg1-a1-a2", "approver3-wg1-a2"], team["members"])
        self.assertDictEqual({"repo3": "write", "repo4": "write"}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-area-2-reviewers"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertListEqual(["reviewer1-wg1-a2"], team["members"])
        self.assertDictEqual({"repo3": "read", "repo4": "read"}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-area-2-bots"]
        self.assertListEqual(["execution-lead-wg1", "technical-lead-wg1"], team["maintainers"])
        self.assertListEqual(["bot2-wg1-a2"], team["members"])
        self.assertDictEqual({"repo3": "write", "repo4": "write"}, team["repos"])

    def test_generate_wg_teams_exclude_non_org_repos(self):
        _wg2 = OrgGenerator._yaml_load(wg2)
        OrgGenerator._validate_wg(_wg2)

        (name, wg_team) = OrgGenerator._generate_wg_teams(_wg2)

        self.assertEqual("wg-wg2-name", name)
        self.assertListEqual(["execution-lead-wg2", "technical-lead-wg2"], wg_team["maintainers"])
        self.assertListEqual(["approver1-wg2-a1"], wg_team["members"])

        team = wg_team["teams"]["wg-wg2-name-leads"]
        self.assertListEqual(["execution-lead-wg2", "technical-lead-wg2"], team["maintainers"])
        self.assertDictEqual({"repo10": "admin", "repo11": "admin"}, team["repos"])

        team = wg_team["teams"]["wg-wg2-name-bots"]
        self.assertListEqual(["execution-lead-wg2", "technical-lead-wg2"], team["maintainers"])
        self.assertListEqual([], team["members"])
        self.assertDictEqual({"repo10": "write", "repo11": "write"}, team["repos"])

        team = wg_team["teams"]["wg-wg2-name-area-1-approvers"]
        self.assertListEqual(["execution-lead-wg2", "technical-lead-wg2"], team["maintainers"])
        self.assertListEqual(["approver1-wg2-a1"], team["members"])
        self.assertDictEqual({"repo10": "write", "repo11": "write"}, team["repos"])

        self.assertNotIn("wg-wg2-name-area-1-reviewers", wg_team["teams"])
        self.assertNotIn("wg-wg2-name-area-1-bots", wg_team["teams"])

    def test_generate_wg_teams_multiple_orgs(self):
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        _wg4 = OrgGenerator._yaml_load(wg4_other_org)
        OrgGenerator._validate_wg(_wg4)

        (name, wg_team) = OrgGenerator._generate_wg_teams(_wg4)

        self.assertEqual("wg-wg4-name", name)
        self.assertListEqual(["execution-lead-wg4", "technical-lead-wg4"], wg_team["maintainers"])
        self.assertListEqual(["approver1-wg4-a1", "approver2-wg4-a1-a2", "approver3-wg4-a2"], wg_team["members"])

        team = wg_team["teams"]["wg-wg4-name-area-1-approvers"]
        self.assertListEqual(["execution-lead-wg4", "technical-lead-wg4"], team["maintainers"])
        self.assertListEqual(["approver1-wg4-a1", "approver2-wg4-a1-a2"], team["members"])
        self.assertDictEqual({"repo1": "write", "repo2": "write"}, team["repos"])

        team = wg_team["teams"]["wg-wg4-name-area-2-approvers"]
        self.assertDictEqual({"repo3": "write", "repo4": "write"}, team["repos"])

    def test_generate_toc_team(self):
        _toc = OrgGenerator._yaml_load(toc)
        OrgGenerator._validate_wg(_toc)
        (name, team) = OrgGenerator._generate_toc_team(_toc)

        self.assertEqual("toc", name)
        self.assertListEqual(["toc-member-1", "toc-member-2"], team["maintainers"])
        self.assertNotIn("members", team)
        self.assertNotIn("teams", team)
        self.assertDictEqual({"community": "admin"}, team["repos"])

    def test_generate_wg_leads_team(self):
        _wg1 = OrgGenerator._yaml_load(wg1)
        OrgGenerator._validate_wg(_wg1)
        _wg2 = OrgGenerator._yaml_load(wg2)
        OrgGenerator._validate_wg(_wg2)

        (name, team) = OrgGenerator._generate_wg_leads_team([_wg1, _wg2])

        self.assertEqual("wg-leads", name)
        self.assertNotIn("maintainers", team)
        self.assertListEqual(["execution-lead-wg1", "execution-lead-wg2", "technical-lead-wg1", "technical-lead-wg2"], team["members"])
        self.assertNotIn("teams", team)
        self.assertNotIn("repos", team)

    def test_generate_teams(self):
        o = OrgGenerator(static_org_cfg=org_cfg, contributors=contributors, toc=toc, working_groups=[wg1, wg2])
        o.generate_org_members()
        o.generate_teams()

        self.assertEqual("cloudfoundry", o.toc_org)

        teams = o.org_cfg["orgs"]["cloudfoundry"]["teams"]
        # toc, wg-leads, 2 WGs
        self.assertEqual(2 + 2, len(teams))
        self.assertIn("wg-wg1-name", teams)
        self.assertEqual(2, len(teams["wg-wg1-name"]["maintainers"]))  # wg1 leads
        self.assertEqual(3, len(teams["wg-wg1-name"]["members"]))  # wg1 approvers
        self.assertEqual(6, len(teams["wg-wg1-name"]["teams"]))  # leads, bots, area1 appr, area2 appr, reviewers, bots
        self.assertIn("wg-wg2-name", teams)
        self.assertEqual(2, len(teams["wg-wg2-name"]["maintainers"]))  # wg2 leads
        self.assertEqual(1, len(teams["wg-wg2-name"]["members"]))  # wg2 approvers
        self.assertEqual(3, len(teams["wg-wg2-name"]["teams"]))  # leads, bots, area1 appr

        self.assertIn("toc", teams)
        self.assertEqual(2, len(teams["toc"]["maintainers"]))
        self.assertNotIn("members", teams["toc"])
        self.assertEqual(1, len(teams["wg-leads"]["repos"]))  # community
        self.assertIn("community", teams["toc"]["repos"])

        self.assertIn("wg-leads", teams)
        self.assertEqual(2 + 2, len(teams["wg-leads"]["members"]))  # wg1 and wg2 leads
        self.assertEqual(1, len(teams["wg-leads"]["repos"]))  # community
        self.assertIn("community", teams["wg-leads"]["repos"])

    def test_generate_teams_multiple_orgs(self):
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        o = OrgGenerator(
            static_org_cfg=org_cfg_multiple, contributors=contributors_multiple_orgs, toc=toc, working_groups=[wg1, wg2, wg4_other_org]
        )
        o.generate_org_members()
        o.generate_teams()

        self.assertEqual("cloudfoundry", o.toc_org)

        teams = o.org_cfg["orgs"]["cloudfoundry"]["teams"]
        # toc, wg-leads, 2 WGs, wg-leads-cloudfoundry2
        self.assertEqual(2 + 2 + 1, len(teams))
        self.assertIn("wg-wg1-name", teams)
        self.assertEqual(2, len(teams["wg-wg1-name"]["maintainers"]))  # wg1 leads
        self.assertEqual(3, len(teams["wg-wg1-name"]["members"]))  # wg1 approvers
        self.assertEqual(6, len(teams["wg-wg1-name"]["teams"]))  # leads, bots, area1 appr, area2 appr, reviewers, bots
        self.assertIn("wg-wg2-name", teams)
        self.assertEqual(2, len(teams["wg-wg2-name"]["maintainers"]))  # wg2 leads
        self.assertEqual(1, len(teams["wg-wg2-name"]["members"]))  # wg2 approvers
        self.assertEqual(3, len(teams["wg-wg2-name"]["teams"]))  # leads, bots, area1 appr

        self.assertIn("toc", teams)
        self.assertEqual(2, len(teams["toc"]["maintainers"]))
        self.assertNotIn("members", teams["toc"])
        self.assertEqual(1, len(teams["wg-leads"]["repos"]))  # community
        self.assertIn("community", teams["toc"]["repos"])

        self.assertIn("toc", teams)
        self.assertEqual(2, len(teams["toc"]["maintainers"]))
        self.assertNotIn("members", teams["toc"])
        self.assertEqual(1, len(teams["wg-leads"]["repos"]))  # community
        self.assertIn("community", teams["toc"]["repos"])

        # wg-leads in cloudfoundry
        self.assertIn("wg-leads", teams)
        self.assertEqual(2 + 2, len(teams["wg-leads"]["members"]))  # wg1, wg2
        self.assertEqual(1, len(teams["wg-leads"]["repos"]))  # community
        self.assertIn("community", teams["wg-leads"]["repos"])

        # wg-leads in cloudfoundry2
        self.assertIn("wg-leads-cloudfoundry2", teams)
        self.assertEqual(2, len(teams["wg-leads-cloudfoundry2"]["members"]))  # wg4 leads
        self.assertEqual(1, len(teams["wg-leads-cloudfoundry2"]["repos"]))  # community
        self.assertIn("community", teams["wg-leads-cloudfoundry2"]["repos"])

        teams = o.org_cfg["orgs"]["cloudfoundry2"]["teams"]
        # wg-leads, 1 WG
        self.assertEqual(1 + 1, len(teams))
        self.assertIn("wg-wg4-name", teams)
        self.assertEqual(2, len(teams["wg-wg4-name"]["maintainers"]))  # wg4 leads
        self.assertEqual(3, len(teams["wg-wg4-name"]["members"]))  # wg4 approvers
        self.assertEqual(6, len(teams["wg-wg4-name"]["teams"]))  # leads, bots, area1 appr, area2 appr, reviewers, bots

        self.assertIn("wg-leads", teams)
        self.assertEqual(2, len(teams["wg-leads"]["members"]))  # wg4 leads
        self.assertNotIn("repos", teams["wg-leads"])  # community repo is in cf org not in cf2

    def test_validate_branch_protection(self):
        OrgGenerator._validate_branch_protection(OrgGenerator._yaml_load(branch_protection))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_branch_protection({})

        # multiple orgs
        with self.assertRaises(ValueError):
            OrgGenerator._validate_branch_protection(OrgGenerator._yaml_load(branch_protection_multiple_orgs))
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        OrgGenerator._validate_branch_protection(OrgGenerator._yaml_load(branch_protection_multiple_orgs))

    def test_get_default_branch(self):
        o = OrgGenerator(static_org_cfg=org_cfg)
        self.assertEqual("main", o._get_default_branch("cloudfoundry", "repo1"))
        self.assertEqual("defbranch", o._get_default_branch("cloudfoundry", "repo3"))
        # trouble ahead: new repos get main as default branch (github config)
        # peribolos assumes master as default branch, at least when reading repo config
        self.assertEqual("master", o._get_default_branch("cloudfoundry", "repo5"))
        self.assertEqual("master", o._get_default_branch("cloudfoundry", "unknown"))

    def test_generate_wg_branch_protection(self):
        o = OrgGenerator(static_org_cfg=org_cfg, branch_protection=branch_protection)
        _wg1 = OrgGenerator._yaml_load(wg1)
        OrgGenerator._validate_wg(_wg1)
        repos_bp = o._generate_wg_branch_protection(_wg1)
        self.assertEqual(4, len(repos_bp))
        self.assertSetEqual({"repo1", "repo2", "repo3", "repo4"}, set(repos_bp.keys()))
        pr_reviews = repos_bp["repo1"]["required_pull_request_reviews"]
        self.assertEqual(0, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg1-name-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])
        self.assertListEqual(["^main$", "^v[0-9]*$"], repos_bp["repo1"]["include"])
        # other default branch
        self.assertListEqual(["^defbranch$", "^v[0-9]*$"], repos_bp["repo3"]["include"])

        _wg3 = OrgGenerator._yaml_load(wg3)
        OrgGenerator._validate_wg(_wg3)
        repos_bp = o._generate_wg_branch_protection(_wg3)
        self.assertEqual(5, len(repos_bp))
        pr_reviews = repos_bp["repo1"]["required_pull_request_reviews"]
        self.assertEqual(0, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg3-name-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])
        pr_reviews = repos_bp["repo2"]["required_pull_request_reviews"]
        self.assertEqual(0, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg3-name-bots", "wg-wg3-name-area-5-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])
        pr_reviews = repos_bp["repo3"]["required_pull_request_reviews"]
        self.assertEqual(1, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg3-name-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])
        pr_reviews = repos_bp["repo4"]["required_pull_request_reviews"]
        self.assertEqual(1, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg3-name-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])
        pr_reviews = repos_bp["repo5"]["required_pull_request_reviews"]
        self.assertEqual(1, pr_reviews["required_approving_review_count"])
        self.assertListEqual(["wg-wg3-name-bots", "wg-wg3-name-area-5-bots"], pr_reviews["bypass_pull_request_allowances"]["teams"])

    def test_generate_branch_protection(self):
        o = OrgGenerator(static_org_cfg=org_cfg, toc=toc, working_groups=[wg1, wg2, wg3], branch_protection=branch_protection)
        o.generate_branch_protection()
        bp_repos = o.branch_protection["branch-protection"]["orgs"]["cloudfoundry"]["repos"]
        # TOC and wg3 opted in, wg1 and wg2 not
        # note: repo1..4 are shared between wg1 (opt out) and wg3 (opt in) - wg3 wins
        self.assertSetEqual({f"repo{i}" for i in range(1, 6)} | {"community"}, set(bp_repos.keys()))
        # repo1 has static config that wins over generated branch protection rules
        self.assertTrue(bp_repos["repo1"]["protect"])
        self.assertNotIn("required_pull_request_reviews", bp_repos["repo1"])

    def test_generate_branch_protection_multiple_orgs(self):
        OrgGenerator._MANAGED_ORGS = ["cloudfoundry", "cloudfoundry2"]
        o = OrgGenerator(
            static_org_cfg=org_cfg_multiple,
            toc=toc,
            working_groups=[wg1, wg2, wg3, wg4_other_org],
            branch_protection=branch_protection_multiple_orgs,
        )
        o.generate_branch_protection()
        bp_repos = o.branch_protection["branch-protection"]["orgs"]["cloudfoundry"]["repos"]
        # TOC and wg3 opted in, wg1 and wg2 not
        # note: repo1..4 are shared between wg1 (opt out) and wg3 (opt in) - wg3 wins
        self.assertSetEqual({f"repo{i}" for i in range(1, 6)} | {"community"}, set(bp_repos.keys()))
        # repo1 has static config that wins over generated branch protection rules
        self.assertTrue(bp_repos["repo1"]["protect"])
        self.assertNotIn("required_pull_request_reviews", bp_repos["repo1"])

        bp_repos = o.branch_protection["branch-protection"]["orgs"]["cloudfoundry2"]["repos"]
        # wg4 opted in, repo5 is ignored because of wrong org
        self.assertSetEqual({f"repo{i}" for i in range(1, 5)}, set(bp_repos.keys()))
        # repo1 has static config that wins over generated branch protection rules
        self.assertTrue(bp_repos["repo1"]["protect"])
        self.assertNotIn("required_pull_request_reviews", bp_repos["repo1"])


# integration test, depends on data in this repo which may change
class TestOrgGeneratorIntegrationTest(unittest.TestCase):
    def test_cf_org(self):
        self.assertEqual(["cloudfoundry"], OrgGenerator._MANAGED_ORGS)

        o = OrgGenerator()
        o.load_from_project()
        self.assertEqual(1, len(o.org_cfg["orgs"]))
        self.assertEqual("cloudfoundry", o.toc_org)
        self.assertEqual("Technical Oversight Committee", o.toc["name"])
        self.assertGreater(len(o.contributors["cloudfoundry"]), 100)
        cf_wgs = o.working_groups["cloudfoundry"]
        self.assertGreater(len(cf_wgs), 5)
        self.assertEqual(1, len([wg for wg in cf_wgs if "Admin" in wg["name"]]))
        self.assertEqual(1, len([wg for wg in cf_wgs if "Deployments" in wg["name"]]))
        # packeto WG charter has no yaml block
        self.assertEqual(0, len([wg for wg in cf_wgs if "packeto" in wg["name"].lower()]))
        # no WGs without execution leads
        self.assertEqual(0, len([wg for wg in cf_wgs if len(wg["execution_leads"]) == 0]))
        # branch protection
        self.assertIn("cloudfoundry", o.branch_protection["branch-protection"]["orgs"])

        self.assertTrue(o.validate_repo_ownership())

        o.generate_org_members()
        members = o.org_cfg["orgs"]["cloudfoundry"]["members"]
        admins = o.org_cfg["orgs"]["cloudfoundry"]["admins"]
        self.assertGreater(len(members), 100)
        self.assertGreater(len(admins), 7)  # 5 toc members + CFF technical staff
        self.assertIn("cf-bosh-ci-bot", members)

        o.generate_teams()
        teams = o.org_cfg["orgs"]["cloudfoundry"]["teams"]
        self.assertIn("wg-app-runtime-deployments", teams)
        self.assertIn(
            "cf-deployment", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-cf-deployment-approvers"]["repos"]
        )
        self.assertIn("cf-deployment", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-bots"]["repos"])
        self.assertIn("ard-wg-gitbot", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-bots"]["members"])
        self.assertIn("toc", teams)
        self.assertEqual(5, len(teams["toc"]["maintainers"]))
        self.assertIn("community", teams["toc"]["repos"])
        self.assertIn("wg-leads", teams)
        self.assertIn("community", teams["wg-leads"]["repos"])

        o.generate_branch_protection()
        bp_repos = o.branch_protection["branch-protection"]["orgs"]["cloudfoundry"]["repos"]
        self.assertGreaterEqual(len(bp_repos), 3)
