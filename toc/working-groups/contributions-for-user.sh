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

find_commits_for_repo() {
  local user=$1
  local repo=$2

  if commits=$(gh api --paginate "repos/${repo}/commits?author=${user}&per_page=100" 2>/dev/null); then
    echo "${commits}" | interactions=$(yq -oj -I=0 -r '
      .[] |
      "- " + .commit.author.date + ": [" + (.commit.message | split("\n")[0]) + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi
  if commits=$(gh api --paginate "repos/${repo}/commits?committer=${user}&per_page=100" 2>/dev/null); then
    echo "${commits}" | interactions=$(yq -oj -I=0 -r '
      .[] |
      "- " + .commit.committer.date + ": [" + (.commit.message | split("\n")[0]) + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi
}

find_prs_for_repo() {
  local user=$1
  local repo=$2

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
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi
  if issues=$(gh api --paginate "repos/${repo}/issues?mentioned=${user}&state=all" 2>/dev/null); then
    echo "${issues}" | interactions=$(yq -oj -I=0 -r '
      .[]
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    ') yq -oj -r '(select(strenv(interactions) == "- ") | . = "") // strenv(interactions)'
  fi

  echo "${EVENTS_JSON}" |  interactions=$(user="${user}" repo="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "IssueCommentEvent")
    | select(.repo.name == strenv(repo))
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
  uri_safe_file=$(echo "${wg} - ${area}.md" | yq -oj -I=0 -r '@uri' | sed -E 's/\%20|\+|\%28/\ /g' | sed -E 's/\%0A|\%29//g' | sed 's/%2F/and/g')
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
        find_commits_for_repo "${USERNAME}" "${repo}"
      done | sort -u
      echo
    ) | gh gist create -d "${USERNAME}'s Possible Contributions to ${WORKING_GROUP} - ${area}" -f "${uri_safe_file}" - 2>/dev/null
  )
  echo "Contributions have been summarized at ${gist_url}"
done