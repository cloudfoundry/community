import requests
import argparse
import datetime


class InactiveUserHandler:
    def __init__(
        self,
        github_org: [str],
        activity_date: [str],
        github_token: [str],
    ):
        self.github_org = github_org
        self.activity_date = activity_date
        self.github_token = github_token

    def _execute_query(self, query):
        headers = {"Authorization": "Bearer {}".format(self.github_token)}
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query execution failed with status code of {}. {}".format(request.status_code, query))

    def is_user(self, user):
        query = """
        {
            user(login: \"""" + user + """\") {
                contributionsCollection(organizationID: \"""" + self.github_org + """\", from: \"""" + self.activity_date + """\") {
                    hasAnyContributions
                }
            }
        }
        """

        result = self._execute_query(query)
        return result["data"]["user"]["contributionsCollection"]["hasAnyContributions"]


if __name__ == "__main__":
    one_years_before = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')

    parser = argparse.ArgumentParser(description="Cloud Foundry Org Inactive User Handler")
    parser.add_argument("-go", "--githuborg", default="O_kgDOAAl8sg", help="Cloud Foundry Github org ID")
    parser.add_argument("-sd", "--sincedate", default=one_years_before, help="Since when the activity should be analyze. Date forma in '%Y-%m-%dT%H:%M:%SZ'")
    parser.add_argument("-gt", "--githubtoken", default="", help="Github API access token")
    args = parser.parse_args()

    print("Analyzing Cloud Foundry org user activity.")
    # Get all users who are not part of any WG here

    userHandler = InactiveUserHandler(args.githuborg, args.sincedate, args.githubtoken)
    # Iterate over the users here and collect inactive users
    result = userHandler.is_user("<replace-with-github-user>")

    print("Is user inactive result - {}".format(result))
    # Create a pr wiht inactive users
