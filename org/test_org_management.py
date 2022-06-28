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
"""

wg1 = """
name: WG1 Name
execution_leads:
- name: Execution Lead WG1
  github: execution-lead-1
technical_leads:
- name: Technical Lead WG1
  github: technical-lead-1
bots:
- name: WG1 CI Bot
  github: bot1
areas:
- name: Area 1
  approvers:
  - github: user1
    name: User 1
  - github: user2
    name: User 2
  repositories:
  - cloudfoundry/repo1
  - cloudfoundry/repo2
- name: Area 2
  approvers:
  - github: user2
    name: User 2
  - github: user3
    name: User 3
  repositories:
  - cloudfoundry/repo3
  - cloudfoundry/repo4
"""

wg2 = """
name: WG2 Name
execution_leads:
- name: Execution Lead WG2
  github: execution-lead-2
technical_leads:
- name: Technical Lead WG2
  github: technical-lead-2
bots: []
areas:
- name: Area 1
  approvers:
  - github: user10
    name: User 10
  repositories:
  - cloudfoundry/repo10
  - cloudfoundry/repo11
  - non-cloudfoundry/repo12
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
    github: user-toc
  repositories:
  - cloudfoundry/community
config:
  github_project_sync:
    mapping:
      cloudfoundry: 31
"""

contributors = """
contributors:
- contributor1
- Contributor2
"""


class TestOrgGenerator(unittest.TestCase):
    def test_empty_org(self):
        o = OrgGenerator()
        o.generate_org_members()
        self.assertListEqual([], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_contributors(self):
        o = OrgGenerator(contributors=contributors)
        o.generate_org_members()
        self.assertListEqual(["Contributor2", "contributor1"], o.org_cfg["orgs"]["cloudfoundry"]["members"])

    def test_contributors_wg(self):
        o = OrgGenerator(working_groups=[wg1, wg2])
        o.generate_org_members()
        members = o.org_cfg["orgs"]["cloudfoundry"]["members"]
        self.assertEqual(6 + 3, len(members))
        self.assertIn("execution-lead-1", members)
        self.assertIn("user1", members)
        self.assertIn("user10", members)

    def test_org_admins_cannot_be_org_members(self):
        contributors = """
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

    def test_extract_wg_config(self):
        self.assertIsNone(OrgGenerator._extract_wg_config(""))
        wg = OrgGenerator._extract_wg_config(f"bla bla ```yaml {wg1} ```")
        assert wg is not None
        self.assertEqual("WG1 Name", wg["name"])

    def test_wg_github_users(self):
        wg = yaml.safe_load(wg1)
        users = OrgGenerator._wg_github_users(wg)
        self.assertEqual(6, len(users))
        self.assertIn("execution-lead-1", users)
        self.assertIn("technical-lead-1", users)
        self.assertIn("user1", users)
        self.assertIn("bot1", users)

    def test_wg_github_users_leads(self):
        wg = yaml.safe_load(wg1)
        users = OrgGenerator._wg_github_users_leads(wg)
        self.assertSetEqual({"execution-lead-1", "technical-lead-1"}, users)

    def test_validate_contributors(self):
        OrgGenerator._validate_contributors({"contributors": []})
        OrgGenerator._validate_contributors(yaml.safe_load(contributors))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_contributors({})
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_contributors({"contributors": 1})

    def test_validate_wg(self):
        OrgGenerator._validate_wg(OrgGenerator._empty_wg_config("wg"))
        OrgGenerator._validate_wg(yaml.safe_load(wg1))
        OrgGenerator._validate_wg(yaml.safe_load(wg2))
        OrgGenerator._validate_wg(yaml.safe_load(toc))
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
            OrgGenerator._validate_wg(yaml.safe_load(wg))
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
            OrgGenerator._validate_wg(yaml.safe_load(wg))

    def test_validate_github_org_cfg(self):
        OrgGenerator._validate_github_org_cfg(yaml.safe_load(org_cfg))
        with self.assertRaises(jsonschema.ValidationError):
            OrgGenerator._validate_github_org_cfg({})

    def test_kebab_case(self):
        self.assertEqual("", OrgGenerator._kebab_case(""))
        self.assertEqual("wg-a-b-c-d-e", OrgGenerator._kebab_case("wg-a b_c-d  e"))
        self.assertEqual("wg-a-b-c", OrgGenerator._kebab_case(":wg-a (b)/?=c "))
        self.assertEqual("wg-app-runtime-deployments", OrgGenerator._kebab_case("wg-App Runtime Deployments"))
        self.assertEqual("wg-app-runtime-deployments-cf-deployments", OrgGenerator._kebab_case("wg-App Runtime Deployments-CF Deployments"))
        self.assertEqual(
            "wg-foundational-infrastructure-integrated-databases-mysql-postgres",
            OrgGenerator._kebab_case("wg-Foundational Infrastructure-Integrated Databases (Mysql / Postgres)"),
        )

    def test_generate_wg_teams(self):
        _wg1 = yaml.safe_load(wg1)
        (name, wg_team) = OrgGenerator._generate_wg_teams(_wg1)

        self.assertEqual("wg-wg1-name", name)
        self.assertListEqual(["execution-lead-1", "technical-lead-1"], wg_team["maintainers"])
        self.assertListEqual(["user1", "user2", "user3"], wg_team["members"])

        team = wg_team["teams"]["wg-wg1-name-leads"]
        self.assertListEqual(["execution-lead-1", "technical-lead-1"], team["maintainers"])
        self.assertDictEqual({f"repo{i}": "admin" for i in range(1, 5)}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-bots"]
        self.assertListEqual(["execution-lead-1", "technical-lead-1"], team["maintainers"])
        self.assertListEqual(["bot1"], team["members"])
        self.assertDictEqual({f"repo{i}": "write" for i in range(1, 5)}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-area-1"]
        self.assertListEqual(["execution-lead-1", "technical-lead-1"], team["maintainers"])
        self.assertListEqual(["user1", "user2"], team["members"])
        self.assertDictEqual({"repo1": "write", "repo2": "write"}, team["repos"])

        team = wg_team["teams"]["wg-wg1-name-area-2"]
        self.assertListEqual(["execution-lead-1", "technical-lead-1"], team["maintainers"])
        self.assertListEqual(["user2", "user3"], team["members"])
        self.assertDictEqual({"repo3": "write", "repo4": "write"}, team["repos"])

    def test_generate_wg_teams_exclude_non_cf_repos(self):
        _wg2 = yaml.safe_load(wg2)
        (name, wg_team) = OrgGenerator._generate_wg_teams(_wg2)

        self.assertEqual("wg-wg2-name", name)
        self.assertListEqual(["execution-lead-2", "technical-lead-2"], wg_team["maintainers"])
        self.assertListEqual(["user10"], wg_team["members"])

        team = wg_team["teams"]["wg-wg2-name-leads"]
        self.assertListEqual(["execution-lead-2", "technical-lead-2"], team["maintainers"])
        self.assertDictEqual({"repo10": "admin", "repo11": "admin"}, team["repos"])

        team = wg_team["teams"]["wg-wg2-name-bots"]
        self.assertListEqual(["execution-lead-2", "technical-lead-2"], team["maintainers"])
        self.assertListEqual([], team["members"])
        self.assertDictEqual({"repo10": "write", "repo11": "write"}, team["repos"])

        team = wg_team["teams"]["wg-wg2-name-area-1"]
        self.assertListEqual(["execution-lead-2", "technical-lead-2"], team["maintainers"])
        self.assertListEqual(["user10"], team["members"])
        self.assertDictEqual({"repo10": "write", "repo11": "write"}, team["repos"])

    def test_generate_toc_team(self):
        _toc = yaml.safe_load(toc)
        (name, team) = OrgGenerator._generate_toc_team(_toc)

        self.assertEqual("toc", name)
        self.assertListEqual(["toc-member-1", "toc-member-2"], team["maintainers"])
        self.assertNotIn("members", team)
        self.assertNotIn("teams", team)
        self.assertDictEqual({"community": "admin"}, team["repos"])

    def test_generate_wg_leads_team(self):
        _wg1 = yaml.safe_load(wg1)
        _wg2 = yaml.safe_load(wg2)

        (name, team) = OrgGenerator._generate_wg_leads_team([_wg1, _wg2])

        self.assertEqual("wg-leads", name)
        self.assertNotIn("maintainers", team)
        self.assertListEqual(["execution-lead-1", "execution-lead-2", "technical-lead-1", "technical-lead-2"], team["members"])
        self.assertNotIn("teams", team)
        self.assertDictEqual({"community": "write"}, team["repos"])

    # test depends on data in this repo which may change
    def test_cf_org(self):
        o = OrgGenerator()
        o.load_from_project()
        o.generate_org_members()
        o.generate_teams()
        members = o.org_cfg["orgs"]["cloudfoundry"]["members"]
        self.assertGreater(len(members), 100)
        self.assertIn("cf-bosh-ci-bot", members)
        teams = o.org_cfg["orgs"]["cloudfoundry"]["teams"]
        self.assertIn("wg-app-runtime-deployments", teams)
        self.assertIn("cf-deployment", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-cf-deployment"]["repos"])
        self.assertIn("cf-deployment", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-bots"]["repos"])
        self.assertIn("cf-gitbot", teams["wg-app-runtime-deployments"]["teams"]["wg-app-runtime-deployments-bots"]["members"])
        self.assertIn("toc", teams)
        self.assertIn("community", teams["toc"]["repos"])
        self.assertIn("wg-leads", teams)
