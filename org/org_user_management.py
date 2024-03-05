import requests
import argparse
import datetime
import yaml
import os
import uuid

from org_management import OrgGenerator

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


class InactiveUserHandler:
    def __init__(
        self,
        github_org: [str],
        github_org_id: [str],
        activity_date: [str],
        github_token: [str],
    ):
        self.github_org = github_org
        self.github_org_id = github_org_id
        self.activity_date = activity_date
        self.github_token = github_token

    def _get_request_headrs(self):
        return {"Authorization": f"Bearer {self.github_token}"}

    def _process_request_result(self, request):
        if request.status_code == 200 or request.status_code == 201:
            return request.json()
        else:
            raise Exception(f"Request execution failed with status code of {request.status_code}. {request.status_code}")

    def _execute_query(self, query):
        request = requests.post("https://api.github.com/graphql", json={"query": query}, headers=self._get_request_headrs())
        return self._process_request_result(request)

    def _build_query(self, after_cursor_value=None):
        after_cursor = '"{}"'.format(after_cursor_value) if after_cursor_value else "null"
        query = """
        {
            organization(login: \"%s\") {
                membersWithRole(first: 50, after:%s) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        login
                        contributionsCollection(organizationID: \"%s\", from: \"%s\") {
                            hasAnyContributions
                        }
                    }
                }
            }
        }
        """ % (
            self.github_org,
            after_cursor,
            self.github_org_id,
            self.activity_date,
        )
        return query

    def get_inactive_users(self):
        inactive_users = set()
        has_next_page = True
        after_cursor_value = None
        while has_next_page:
            result = self._execute_query(self._build_query(after_cursor_value))
            for user_node in result["data"]["organization"]["membersWithRole"]["nodes"]:
                user = user_node["login"]
                activity = user_node["contributionsCollection"]["hasAnyContributions"]
                print(f"The user '{user}' has activity value {activity} contributions")
                if not activity:
                    print(f"Adding user '{user}' as inactive")
                    inactive_users.add(user)

            has_next_page = result["data"]["organization"]["membersWithRole"]["pageInfo"]["hasNextPage"]
            after_cursor_value = result["data"]["organization"]["membersWithRole"]["pageInfo"]["endCursor"]

        return inactive_users

    def _load_yaml_file(self, path):
        with open(path, "r") as stream:
            return yaml.safe_load(stream)

    def _write_yaml_file(self, path, data):
        with open(path, "w") as f:
            yaml.dump(data, f)

    def delete_inactive_contributors(self, users_to_delete):
        path = f"{_SCRIPT_PATH}/contributors.yml"
        contributors_yaml = self._load_yaml_file(path)
        users_to_delete_lower = [user.lower() for user in users_to_delete]
        contributors_yaml["contributors"] = [c for c in contributors_yaml["contributors"] if c.lower() not in users_to_delete_lower]
        self._write_yaml_file(path, contributors_yaml)

    def get_inactive_users_msg(self, users_to_delete, tagusers):
        rfc = (
            "https://github.com/cloudfoundry/community/blob/main/toc/rfc/"
            "rfc-0025-define-criteria-and-removal-process-for-inactive-members.md"
        )
        rfc_revocation_rules = (
            "https://github.com/cloudfoundry/community/blob/main/toc/rfc/rfc-0025-define-"
            "criteria-and-removal-process-for-inactive-members.md#remove-the-membership-to-the-cloud-foundry-github-organization"
        )
        user_tagging_prefix = "@" if tagusers else ""
        users_as_list = "\n".join(str(user_tagging_prefix + s) for s in users_to_delete)
        return (
            f"According to the rules for inactivity defined in [RFC-0025]({rfc}) following users will be deleted:\n"
            f"{users_as_list}\nAccording to the [revocation policy in the RFC]({rfc_revocation_rules}), users have"
            " two weeks to refute this revocation, if they wish."
        )

    @staticmethod
    def _get_bool_env_var(env_var_name, default):
        return os.getenv(env_var_name, default).lower() == "true"


if __name__ == "__main__":
    one_year_back = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

    parser = argparse.ArgumentParser(description="Cloud Foundry Org Inactive User Handler")
    parser.add_argument("-goid", "--githuborgid", default="O_kgDOAAl8sg", help="Cloud Foundry Github org ID")
    parser.add_argument("-go", "--githuborg", default="cloudfoundry", help="Cloud Foundry Github org name")
    parser.add_argument("-sd", "--sincedate", default=one_year_back, help="Since when to analyze in format 'Y-m-dTH:M:SZ'")
    parser.add_argument(
        "-gt", "--githubtoken", default=os.environ.get("GH_TOKEN"), help="Github API access token. Supported also as env var 'GH_TOKEN'"
    )
    parser.add_argument(
        "-dr",
        "--dryrun",
        action="store_true",
        help="Dry run execution. Supported also as env var 'INACTIVE_USER_MANAGEMENT_DRY_RUN'",
    )
    parser.add_argument(
        "-tu",
        "--tagusers",
        action="store_true",
        help="Tag users to be notified. Supported also as env var 'INACTIVE_USER_MANAGEMENT_TAG_USERS'",
    )
    args = parser.parse_args()

    print("Get information about community users")
    generator = OrgGenerator()
    generator.load_from_project()
    community_members_with_role = generator.get_community_members_with_role()

    print("Analyzing Cloud Foundry org user activity.")
    userHandler = InactiveUserHandler(args.githuborg, args.githuborgid, args.sincedate, args.githubtoken)
    inactive_users = userHandler.get_inactive_users()

    print(f"Inactive users length is {len(inactive_users)} and inactive users are {inactive_users}")
    users_to_delete = inactive_users - community_members_with_role
    tagusers = args.tagusers or InactiveUserHandler._get_bool_env_var("INACTIVE_USER_MANAGEMENT_TAG_USERS", "False")
    inactive_users_msg = userHandler.get_inactive_users_msg(users_to_delete, tagusers)
    if args.dryrun or InactiveUserHandler._get_bool_env_var("INACTIVE_USER_MANAGEMENT_DRY_RUN", "False"):
        print(f"Dry-run mode.\nInactive_users_msg is: {inactive_users_msg}")
        print(f"Following users will be deleted: {inactive_users}")
    elif users_to_delete:
        userHandler.delete_inactive_contributors(users_to_delete)
        with open(os.environ["GITHUB_OUTPUT"], "a") as env:
            separator = uuid.uuid1()
            step_output_name = "inactive_users_pr_description"
            print(f"{step_output_name}<<{separator}\n{inactive_users_msg}\n{separator}", file=env)

    inactive_users_with_role = community_members_with_role.intersection(inactive_users)
    print(f"Inactive users with role length is {len(inactive_users_with_role)} and users are {inactive_users_with_role}")
