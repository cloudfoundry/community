import requests
import argparse
import datetime
import json

from org_management import OrgGenerator


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
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(f"Query execution failed with status code of {request.status_code}. {request.status_code}")

    def _execute_query(self, query):
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=self._get_request_headrs())
        return self._process_request_result(request)

    def _build_query(self, after_cursor_value=None):
        after_cursor = "null"
        if after_cursor_value:
            after_cursor = '"{}"'.format(after_cursor_value)
        else:
            after_cursor = "null"

        query = """
        {
            organization(login: \"""" + self.github_org + """\") {
                membersWithRole(first: 50, after:""" + after_cursor + """) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        login
                        contributionsCollection(organizationID: \"""" + self.github_org_id + """\", from: \"""" + self.activity_date +"""\") {
                            hasAnyContributions
                        }
                    }
                }
            }
        }
        """
        return query

    def get_inactive_users(self):
        inactive_users = set()
        has_next_page = True
        afeter_cursor_value = None
        while has_next_page:
            result = self._execute_query(self._build_query(afeter_cursor_value))
            print( f"Result is '{result}'")
            for user_node in result["data"]["organization"]["membersWithRole"]["nodes"]:
                user = user_node["login"]
                activity_value = user_node["contributionsCollection"]["hasAnyContributions"]
                print( f"The user '{user}' has activity value {activity_value} contirbutions")
                if not user_node["contributionsCollection"]["hasAnyContributions"]:
                    print( f"Adding user '{user}' as inactive")
                    inactive_users.add(user)


            has_next_page = result["data"]["organization"]["membersWithRole"]["pageInfo"]["hasNextPage"]
            afeter_cursor_value = result["data"]["organization"]["membersWithRole"]["pageInfo"]["endCursor"]

        return inactive_users


if __name__ == "__main__":
    one_years_before = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

    parser = argparse.ArgumentParser(description="Cloud Foundry Org Inactive User Handler")
    parser.add_argument("-goid", "--githuborgid", default="O_kgDOAAl8sg", help="Cloud Foundry Github org ID")
    parser.add_argument("-go", "--githuborg", default="cloudfoundry", help="Cloud Foundry Github org name")
    parser.add_argument("-sd", "--sincedate", default=one_years_before, help="Since when the activity should be analyze. Date forma in '%Y-%m-%dT%H:%M:%SZ'")
    parser.add_argument("-gt", "--githubtoken", default="", help="Github API access token")
    args = parser.parse_args()

    print("Analyzing Cloud Foundry org user activity.")
    # Get all users who are not part of any WG here

    print("Generating cloudfoundry org configuration.")
    generator = OrgGenerator()
    generator.load_from_project()
    contributors = generator.get_contributors()
    community_members_with_role = generator.get_community_members_with_role()

    users_to_analyze = contributors - community_members_with_role


    userHandler = InactiveUserHandler(args.githuborg, args.githuborgid, args.sincedate, args.githubtoken)
    inactive_users = userHandler.get_inactive_users()

    print(f"Inactive users length is {len(inactive_users)} and inactive users are {inactive_users}")
    users_to_delete = inactive_users - community_members_with_role
    inactive_users_with_role = community_members_with_role.intersection(inactive_users)

    print(f"Users to delete length is {len(users_to_delete)} and users are {users_to_delete}")
    print(f"Inactive users with role length is {len(inactive_users_with_role)} and users are {inactive_users_with_role}")

    # Create an issue wiht inactive users
