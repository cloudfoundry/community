#!/usr/bin/env bash

set -e -o pipefail

# Requires bash 4+ for associative arrays. macOS ships bash 3.2 at /bin/bash —
# install a modern bash (e.g. via Homebrew) so that `env bash` resolves to 4+.
if (( BASH_VERSINFO[0] < 4 )); then
  echo "This script requires bash 4 or newer (found ${BASH_VERSION})." >&2
  echo "On macOS: brew install bash, then re-run." >&2
  exit 1
fi

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

emit_pr_with_commits() {
  local repo=$1 pr_number=$2 pr_title=$3 pr_url=$4 pr_date=$5
  echo "- ${pr_date}: [${pr_title}](${pr_url})"
  local pr_commits
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
}

find_commits_grouped_by_pr_for_repo() {
  local user=$1
  local repo=$2
  local -A seen=()

  # Primary: GitHub search API for merged PRs authored by user
  local prs
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+author:${user}+is:merged&per_page=100" 2>/dev/null); then
    while IFS= read -r pr_json; do
      [[ -z "${pr_json}" ]] && continue
      local pr_number pr_title pr_url pr_date
      pr_number=$(echo "${pr_json}" | yq -oj -r '.number')
      pr_title=$(echo "${pr_json}"  | yq -oj -r '.title')
      pr_url=$(echo "${pr_json}"    | yq -oj -r '.html_url')
      pr_date=$(echo "${pr_json}"   | yq -oj -r '.created_at')
      seen[${pr_number}]=1
      emit_pr_with_commits "${repo}" "${pr_number}" "${pr_title}" "${pr_url}" "${pr_date}"
    done < <(echo "${prs}" | yq -oj -I=0 -r '.items[]')
  fi

  # Supplement: events fallback for very recent merged PRs the search index hasn't picked up yet.
  # Only emit one event per PR number (events can contain many actions for the same PR).
  while IFS= read -r pr_json; do
    [[ -z "${pr_json}" ]] && continue
    local pr_number pr_title pr_url pr_date
    pr_number=$(echo "${pr_json}" | yq -oj -r '.payload.number')
    [[ -n "${seen[${pr_number}]+x}" ]] && continue
    pr_title=$(echo "${pr_json}" | yq -oj -r '.payload.pull_request.title')
    pr_url=$(echo "${pr_json}"   | yq -oj -r '.payload.pull_request.html_url')
    pr_date=$(echo "${pr_json}"  | yq -oj -r '.payload.pull_request.created_at')
    seen[${pr_number}]=1
    emit_pr_with_commits "${repo}" "${pr_number}" "${pr_title}" "${pr_url}" "${pr_date}"
  done < <(echo "${EVENTS_JSON}" | user="${user}" repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestEvent")
    | select(.repo.name == strenv(repository))
    | select(.payload.action == "closed")
    | select(.payload.pull_request.user.login == strenv(user))
    | select(.payload.pull_request.merged == true)
  ')
}

find_authored_prs_for_repo() {
  local user=$1
  local repo=$2
  local -A seen=()

  # Primary: GitHub search API
  local prs
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+author:${user}&per_page=100" 2>/dev/null); then
    while IFS= read -r pr_json; do
      [[ -z "${pr_json}" ]] && continue
      local num title url date state
      num=$(echo "${pr_json}"   | yq -oj -r '.number')
      title=$(echo "${pr_json}" | yq -oj -r '.title')
      url=$(echo "${pr_json}"   | yq -oj -r '.html_url')
      date=$(echo "${pr_json}"  | yq -oj -r '.created_at')
      state=$(echo "${pr_json}" | yq -oj -r '.state')
      seen[${num}]=1
      echo "- ${date}: [${title}](${url}) (${state})"
    done < <(echo "${prs}" | yq -oj -I=0 -r '.items[]')
  fi

  # Supplement: targeted single-PR lookup for any PRs visible in events that search missed.
  # Filter to action=="opened" so we hit the API at most once per PR, not once per event.
  while IFS= read -r pr_json; do
    [[ -z "${pr_json}" ]] && continue
    local num title url date state
    num=$(echo "${pr_json}" | yq -oj -r '.payload.number')
    [[ -n "${seen[${num}]+x}" ]] && continue
    local pr_detail
    if pr_detail=$(gh api "repos/${repo}/pulls/${num}" 2>/dev/null); then
      title=$(echo "${pr_detail}" | yq -oj -r '.title')
      url=$(echo "${pr_detail}"   | yq -oj -r '.html_url')
      date=$(echo "${pr_detail}"  | yq -oj -r '.created_at')
      state=$(echo "${pr_detail}" | yq -oj -r '.state')
      seen[${num}]=1
      echo "- ${date}: [${title}](${url}) (${state})"
    fi
  done < <(echo "${EVENTS_JSON}" | user="${user}" repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestEvent")
    | select(.payload.action == "opened")
    | select(.repo.name == strenv(repository))
    | select(.payload.pull_request.user.login == strenv(user))
  ')
}

find_prs_for_repo() {
  local user=$1
  local repo=$2

  # PRs reviewed by the user (excluding own)
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+reviewed-by:${user}&per_page=100" 2>/dev/null); then
    echo "${prs}" | user="${user}" yq -oj -I=0 -r '
      .items[]
      | select(.user.login != strenv(user))
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    '
  fi

  # PRs commented on by the user (excluding own PRs)
  if prs=$(gh api --paginate "search/issues?q=repo:${repo}+type:pr+commenter:${user}&per_page=100" 2>/dev/null); then
    echo "${prs}" | user="${user}" yq -oj -I=0 -r '
      .items[]
      | select(.user.login != strenv(user))
      | "- " + .created_at + ": [" + .title + "](" + .html_url + ")"
    '
  fi

  # Fallback to events for recent activity (covers the 90-day window)
  echo "${EVENTS_JSON}" | repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestReviewEvent")
    | select(.repo.name == strenv(repository))
    | "- " + .payload.pull_request.created_at + ": [" + .payload.pull_request.title + "](" + .payload.pull_request.html_url + ")"
  '

  echo "${EVENTS_JSON}" | user="${user}" repository="${repo}" yq -oj -I=0 -r '
    .[]
    | select(.type == "PullRequestReviewCommentEvent")
    | select(.repo.name == strenv(repository))
    | select(.payload.pull_request.user.login != strenv(user))
    | "- " + .payload.pull_request.created_at + ": [" + .payload.pull_request.title + "](" + .payload.pull_request.html_url + ")"
  '
}

find_commits_on_others_prs_for_repo() {
  local user=$1
  local repo=$2

  # Find commits authored by user in this repo, then check if each landed in a PR
  # authored by someone else (i.e. the user pushed to a collaborator's branch)
  local commits
  if ! commits=$(gh api --paginate \
      "search/commits?q=author:${user}+repo:${repo}&per_page=100" 2>/dev/null); then
    return
  fi

  local -A seen=()

  while IFS= read -r sha; do
    [[ -z "${sha}" ]] && continue
    local prs_for_commit
    if ! prs_for_commit=$(gh api "repos/${repo}/commits/${sha}/pulls" 2>/dev/null); then
      continue
    fi
    while IFS= read -r pr_json; do
      [[ -z "${pr_json}" ]] && continue
      local pr_author pr_number pr_title pr_url pr_date
      pr_author=$(echo "${pr_json}" | yq -oj -r '.user.login')
      pr_number=$(echo "${pr_json}" | yq -oj -r '.number')
      # Only include PRs authored by someone else
      [[ "${pr_author}" == "${user}" ]] && continue
      [[ -n "${seen[${pr_number}]+x}" ]] && continue
      pr_title=$(echo "${pr_json}" | yq -oj -r '.title')
      pr_url=$(echo "${pr_json}"   | yq -oj -r '.html_url')
      pr_date=$(echo "${pr_json}"  | yq -oj -r '.created_at')
      seen[${pr_number}]=1
      echo "- ${pr_date}: [${pr_title}](${pr_url}) (by ${pr_author})"
    done < <(echo "${prs_for_commit}" | yq -oj -I=0 -r '.[]')
  done < <(echo "${commits}" | yq -oj -I=0 -r '.items[].sha')
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

# Normalize to the canonical GitHub login (search API is case-sensitive for author:/reviewed-by:)
USERNAME=$(gh api "users/${USERNAME}" --jq '.login' 2>/dev/null || echo "${USERNAME}")

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

  declare -a repos
  repos=($(echo "${TOC_JSON}" | wg_name="${WORKING_GROUP}" area="${area}" yq -oj -I=0 -r '
    .[]
    | select(.name == strenv(wg_name))
    | .areas[]
    | select(.name == strenv(area))
    | .repositories[]
  '))

  authored_prs=$(
    for repo in "${repos[@]}"; do
      find_authored_prs_for_repo "${USERNAME}" "${repo}"
    done | sort -u
  )

  reviewed_prs=$(
    for repo in "${repos[@]}"; do
      find_prs_for_repo "${USERNAME}" "${repo}"
    done | sort -u
  )

  issues_content=$(
    for repo in "${repos[@]}"; do
      find_issues_for_repo "${USERNAME}" "${repo}"
    done | sort -u
  )

  commits_content=$(
    for repo in "${repos[@]}"; do
      find_commits_grouped_by_pr_for_repo "${USERNAME}" "${repo}"
    done
  )

  commits_on_others=$(
    for repo in "${repos[@]}"; do
      find_commits_on_others_prs_for_repo "${USERNAME}" "${repo}"
    done | sort -u
  )

  # Skip areas with no contributions at all
  if [[ -z "${authored_prs}" && -z "${reviewed_prs}" && -z "${issues_content}" && -z "${commits_content}" && -z "${commits_on_others}" ]]; then
    echo "  No contributions found for '${WORKING_GROUP}: ${area}', skipping."
    continue
  fi

  gist_url=$(
    (
      echo "# ${WORKING_GROUP}: ${area} Contributions"
      echo
      echo "### PRs Authored:"
      echo "${authored_prs:-(none found)}"
      echo
      echo "### PRs Reviewed/Commented on:"
      echo "${reviewed_prs:-(none found)}"
      echo
      echo "### Commits on others' PRs:"
      echo "${commits_on_others:-(none found)}"
      echo
      echo "### Issues that may be relevant:"
      echo "${issues_content:-(none found)}"
      echo
      echo "### Code contributions (merged PRs):"
      echo "${commits_content:-(none found)}"
      echo
    ) | gh gist create -d "${USERNAME}'s Possible Contributions to ${WORKING_GROUP} - ${area}" -f "${uri_safe_file}" - 2>/dev/null
  )
  echo "Contributions have been summarized at ${gist_url}"
done