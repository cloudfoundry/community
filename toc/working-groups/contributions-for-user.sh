#!/bin/bash

set -e -o pipefail

repo_root=$(dirname "$(cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd)")

pushd "${repo_root}/toc/working-groups" >/dev/null

USERNAME=$1
shift || true
WORKING_GROUP="$*"

echo "Parsing working group metadata..."
TOC_JSON=$(${repo_root}/toc/working-groups/parsable-working-groups.sh)

declare -a WORKING_GROUPS
IFS=$'\n'
WORKING_GROUPS=($(echo "${TOC_JSON}" | yq -oj -I=0 -r '.[].name'))

list_working_groups() {
  for wg in "${WORKING_GROUPS[@]}"; do
    echo "- ${wg}"
  done
}

usage_checks() {
  if [[ ! -e $(which gh) ]]; then
    echo 'The `gh` cli is required for this script' >&2
    exit 1
  fi

  if [[ ! -e $(which yq) ]]; then
    echo 'The `yq` cli (https://github.com/mikefarah/yq) is required for this script' >&2
    exit 1
  fi

  # Extract version, remove the leading 'v' if present and check the installed version
  installed_yq_version=$(yq --version 2>&1 | awk '{print $NF}' | sed 's/^v//')
  # yq v4.7 is required for the script, though the `@uri` feature is available from v4.31.1 onwards
  required_version="4.31.1"

  if [ "$(printf '%s\n' "${required_version}" "${installed_yq_version}" | sort -V | head -n1)" != "$required_version" ]; then
    echo "yq version ${installed_yq_version} is installed, but version ${required_version} or higher is required." >&2
    exit 1
  fi

  if gist_url=$(echo "test" | gh gist create -d test -f test - 2>/dev/null); then
    gh gist delete "${gist_url}" --yes >/dev/null 2>&1
  else
    echo 'Please login to GitHub with the `gh` cli using credentials with permissions to create gists' >&2
    exit 1
  fi

  if [[ -z "${USERNAME}" ]]; then
    echo "Usage: contributions-for-user.sh <github-username> <working group name>" >&2
    echo "Where working group name is one of:" >&2
    list_working_groups >&2
    exit 1
  fi

  for wg in "${WORKING_GROUPS[@]}"; do
    if [[ "${wg}" == "${WORKING_GROUP}" ]]; then
      match=1
      break
    fi
  done
  if [[ "${match}" != 1 ]]; then
    echo "Working group name must be one of:" >&2
    list_working_groups >&2
    exit 1
  fi
}

find_commits_grouped_by_pr_for_repo() {
  local user=$1
  local repo=$2

  if ! prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+author:${user}+is:merged&per_page=100" 2>/dev/null); then
    return
  fi

  local merged_pr_count
  merged_pr_count=$(echo "${prs}" | yq -oj -r '.items | length')

  while IFS= read -r pr_json; do
    [[ -z "${pr_json}" ]] && continue
    local pr_number pr_title pr_url pr_date
    pr_number=$(echo "${pr_json}" | yq -oj -r '.number')
    pr_title=$(echo "${pr_json}"  | yq -oj -r '.title')
    pr_url=$(echo "${pr_json}"    | yq -oj -r '.html_url')
    pr_date=$(echo "${pr_json}"   | yq -oj -r '.created_at')

    echo "- ${pr_date}: [${pr_title}](${pr_url})"

    if pr_commits=$(gh api --paginate "repos/${repo}/pulls/${pr_number}/commits?per_page=100" 2>/dev/null); then
      local pr_commit_count
      pr_commit_count=$(echo "${pr_commits}" | yq -oj -r '. | length')
      if [[ "${pr_commit_count}" -gt 1 ]]; then
        echo "${pr_commits}" | yq -oj -I=0 -r '
          .[] |
          "  - " + .commit.author.date + ": [" + ((.commit.message | split("\n"))[0]) + "](" + .html_url + ")"
        '
      fi
    fi
  done < <(echo "${prs}" | yq -oj -I=0 -r '.items[]')

  # Fallback for very recent merged PRs that might not be searchable yet.
  if [[ "${merged_pr_count}" -gt 0 ]]; then
    return
  fi

  while IFS= read -r pr_json; do
    [[ -z "${pr_json}" ]] && continue
    local pr_title pr_url pr_date pr_number
    pr_title=$(echo "${pr_json}" | yq -oj -r '.payload.pull_request.title')
    pr_url=$(echo "${pr_json}"   | yq -oj -r '.payload.pull_request.html_url')
    pr_date=$(echo "${pr_json}"  | yq -oj -r '.payload.pull_request.created_at')
    pr_number=$(echo "${pr_json}"| yq -oj -r '.payload.number')

    echo "- ${pr_date}: [${pr_title}](${pr_url})"

    if pr_commits=$(gh api --paginate "repos/${repo}/pulls/${pr_number}/commits?per_page=100" 2>/dev/null); then
      local pr_commit_count
      pr_commit_count=$(echo "${pr_commits}" | yq -oj -r '. | length')
      if [[ "${pr_commit_count}" -gt 1 ]]; then
        echo "${pr_commits}" | yq -oj -I=0 -r '
          .[] |
          "  - " + .commit.author.date + ": [" + ((.commit.message | split("\n"))[0]) + "](" + .html_url + ")"
        '
      fi
    fi
  done < <(echo "${EVENTS_JSON}" | user="${user}" repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestEvent")
    | select(.repo.name == strenv(repository))
    | select(.payload.action == "closed")
    | select(.payload.pull_request.user.login == strenv(user))
    | select(.payload.pull_request.merged == true)
  ')
}

find_prs_for_repo() {
  local user=$1
  local repo=$2

  # Use GitHub Search API to find PRs reviewed by the user
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+reviewed-by:${user}&per_page=100" 2>/dev/null); then
    echo "${prs}" | interactions=$(yq -oj -I=0 -r '
      .items[]
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi

  # Also check for PRs with review comments
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+commenter:${user}&per_page=100" 2>/dev/null); then
    echo "${prs}" | interactions=$(user="${user}" yq -oj -I=0 -r '
      .items[]
      | select(.user.login != strenv(user))
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi

  # Fallback to events for recent activity
  echo "${EVENTS_JSON}" | interactions=$(repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestReviewEvent")
    | select(.repo.name == strenv(repository))
    | "- " + .payload.pull_request.created_at + ": [" + .payload.pull_request.title + "](" + .payload.pull_request.html_url + ")"
  ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'

  echo "${EVENTS_JSON}" | interactions=$(user="${user}" repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestReviewCommentEvent")
    | select(.repo.name == strenv(repository))
    | select(.payload.pull_request.user.login != strenv(user))
    | "- " + .payload.pull_request.created_at + ": [" + .payload.pull_request.title + "](" + .payload.pull_request.html_url + ")"
  ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
}

find_issues_for_repo() {
  local user=$1
  local repo=$2

  if issues=$(gh api --paginate "repos/${repo}/issues?creator=${user}&state=all" 2>/dev/null); then
    echo "${issues}" | interactions=$(yq -oj -I=0 -r '
      .[]
      | select(.pull_request == null)
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi
  if issues=$(gh api --paginate "repos/${repo}/issues?mentioned=${user}&state=all" 2>/dev/null); then
    echo "${issues}" | interactions=$(yq -oj -I=0 -r '
      .[]
      | select(.pull_request == null)
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi

  echo "${EVENTS_JSON}" |  interactions=$(user="${user}" repo="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "IssueCommentEvent")
    | select(.repo.name == strenv(repo))
    | select(.payload.issue.pull_request == null)
    | select(.payload.issue.user.login != strenv(user))
    | "- " + .payload.issue.created_at + ": [" + .payload.issue.title + "](" + .payload.issue.html_url + ")"
  ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
}

usage_checks
set -u

echo "Gathering GH events..."
EVENTS_JSON=$(gh api --paginate "users/${USERNAME}/events?per_page=100")

declare -a areas
areas=($(echo "${TOC_JSON}" | wg_name="${WORKING_GROUP}" yq -oj -r -I=0 -r "
  .[]
  | select(.name == strenv(wg_name))
  | .areas[].name
"))

for area in "${areas[@]}"; do
  echo "Gathering contributions for the '${WORKING_GROUP}: ${area}' area..."
  uri_safe_file=$(echo "${WORKING_GROUP} - ${area}.md" | yq -oj -I=0 -r '@uri' | sed -E 's/\%20|\+|\%28/\ /g' | sed -E 's/\%0A|\%29//g' | sed 's/%2F/and/g')
  gist_url=$(
    (
      echo "# ${WORKING_GROUP}: ${area} Contributions"
      declare -a repos
      repos=($(echo "${TOC_JSON}" | wg_name="${WORKING_GROUP}" area="${area}" yq -oj -I=0 -r '
        .[]
        | select(.name == strenv(wg_name))
        | .areas[]
        | select(.name == strenv(area))
        | .repositories[]
      '))

      echo "### PRs Commented on/Reviewed:"
      for repo in "${repos[@]}"; do
        find_prs_for_repo "${USERNAME}" "${repo}"
      done | sort -u

      echo "### Issues that may be relevant:"
      for repo in "${repos[@]}"; do
        find_issues_for_repo  "${USERNAME}" "${repo}"
      done | sort -u

      echo "### Code contributions:"
      for repo in "${repos[@]}"; do
        find_commits_grouped_by_pr_for_repo "${USERNAME}" "${repo}"
      done
      echo
    ) | gh gist create -d "${USERNAME}'s Possible Contributions to ${WORKING_GROUP} - ${area}" -f "${uri_safe_file}" - 2>/dev/null
  )
  echo "Contributions have been summarized at ${gist_url}"
done