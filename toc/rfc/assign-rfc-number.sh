#!/usr/bin/env bash

set -e
set -u
set -o pipefail

script_dir="$(cd $(dirname "$BASH_SOURCE[0]") && pwd)"

####
# CONFIG
#

DEBUG=${DEBUG:-}

if [[ "${DEBUG}" ]] ; then
  set -x
fi

OWNER=${OWNER:-cloudfoundry}
REPO=${REPO:-community}
MAIN_BRANCH=${MAIN_BRANCH:-main}
RFC_MERGE_COMMITISH=${RFC_MERGE_COMMITISH:-HEAD}
NOPUSH=${NOPUSH:-}

####
# FUNCTIONS
#

generate_id() {
  id="$(find "$script_dir" -maxdepth 2 -type f | sed 's/[^0-9]*//' | sed -E 's|^([[:digit:]]{4})-.*$|\1|' | sort | tail -n 1  |  sed 's/^0*//')"
  ((id++))
  printf "%04d" "${id}"
}

require_command() {
    if ! [ -x "$(command -v ${1})" ]; then
        echo "Error: '${1}' is not installed." >&2
        exit 1
    fi
}

####
# DEPENDENCIES
#

require_command git
require_command awk
require_command grep
require_command sed
require_command jq
require_command curl

####
# TASK
#


REPOBASENAME=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\4\/\5/p')
REPOOWNER=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\4/p')
REPONAME=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\5/p')
ISAFORK=$(curl -s https://api.github.com/repos/${REPOOWNER}/${REPONAME} | jq '.fork')
UPSTREAMSET=$((git remote -v | grep upstream) || echo "")

if [[ "$ISAFORK" = true ]] ; then
        if [[ -z "$UPSTREAMSET" ]] ; then
            git remote add upstream https://github.com/${OWNER}/${REPO}.git
        fi
    git fetch upstream
    git checkout ${MAIN_BRANCH}
    git merge upstream/${MAIN_BRANCH}
fi

echo "> Pulling latest changes...."
git pull origin ${MAIN_BRANCH} --rebase

# check that the identified merge commit is a 2-parent merge commit
num_parents=$(git cat-file commit "${RFC_MERGE_COMMITISH}" | grep ^parent | wc -l)

if [[ "$num_parents" -ne 2 ]]; then
  commit_sha=$(git rev-parse "${RFC_MERGE_COMMITISH}")
  >&2 echo "Error: commit-ish '${RFC_MERGE_COMMITISH}' selected as RFC merge commit (with SHA ${commit_sha}) has $num_parents parents, not 2"
  exit 2
fi

PR_NUMBER=$(git ls-remote origin 'pull/*/head' | grep -F -f <(git rev-parse "${RFC_MERGE_COMMITISH}^2") | awk -F'/' '{print $3}')

RFC_ID=$(generate_id)
echo "> Generated RFC number: ${RFC_ID}"


SOURCE_DOC=$(find "${script_dir}" -maxdepth 2 -type f -name 'rfc-draft-*')
TARGET_DOC=${SOURCE_DOC//rfc-draft/rfc-${RFC_ID}}
SOURCE_DIR=$(find "${script_dir}" -maxdepth 2 -type d -name 'rfc-draft-*')
TARGET_DIR=${SOURCE_DIR//rfc-draft/rfc-${RFC_ID}}

echo "> Transforming '${SOURCE_DOC}' into '${TARGET_DOC}'"
sed \
  -e "s|- RFC Pull Request:.*|- RFC Pull Request: [${REPO}#${PR_NUMBER}](https://github.com/${OWNER}/${REPO}/pull/${PR_NUMBER})|" \
  -e "s|- Status:.*|- Status: Accepted|" \
  -e "s|rfc-draft-|rfc-${RFC_ID}-|" \
  "${SOURCE_DOC}" \
  > "${TARGET_DOC}"

echo "> Adding '${TARGET_DOC}'..."
git add "${TARGET_DOC}"

echo "> Removing '${SOURCE_DOC}'..."
git rm "${SOURCE_DOC}"

if [[ "$SOURCE_DIR" ]] ; then
  echo "> Moving ${SOURCE_DIR} to ${TARGET_DIR}..."
  git mv "${SOURCE_DIR}" "${TARGET_DIR}"
fi

echo "> Committing to '${MAIN_BRANCH}'..."
git commit -m "Assigning number ${RFC_ID} to RFC from PR #${PR_NUMBER}"

if [[ -n "${NOPUSH}" ]] ; then
  echo "> *NOT* pushing to '${MAIN_BRANCH}' automatically!"
  echo "> *** Push to '${MAIN_BRANCH}' after verifying RFC number and status changes ***"
else
  echo "> Pushing to '${MAIN_BRANCH}'..."
  git push
fi
