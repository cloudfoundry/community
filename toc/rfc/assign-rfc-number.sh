#!/usr/bin/env bash

set -eo pipefail

script="$0"

####
# CONFIG
#

MAIN_BRANCH=${MAIN_BRANCH:-main}
OWNER=${OWNER:-cloudfoundry}
REPO=community

REPOBASENAME=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\4\/\5/p')
REPOOWNER=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\4/p')
REPONAME=$(git config --get remote.origin.url | sed -nr 's/^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$$/\5/p')
ISAFORK=$(curl -s https://api.github.com/repos/${REPOOWNER}/${REPONAME} | jq '.fork')
UPSTREAMSET=$(git remote -v | grep upstream)

####
# FUNCTIONS
#

generate_id() {
  id="$(find toc/rfc -maxdepth 2 -type f | sed 's/[^0-9]*//' | sed -E 's|^([[:digit:]]{4})-.*$|\1|' | sort | tail -n 1  |  sed 's/^0*//')"
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


if [ "$ISAFORK" = true ] ; then
        if [ -z "$UPSTREAMSET" ] ; then
            git remote add upstream https://github.com/${OWNER}/${REPO}.git
        fi
    git fetch upstream
    git checkout ${MAIN_BRANCH}
    git merge upstream/${MAIN_BRANCH}
fi


echo "> Pulling latest changes...."
git pull origin ${MAIN_BRANCH} --rebase

RFC_ID=$(generate_id)
echo "> Generated RFC number: ${RFC_ID}"


SOURCE_DOC=$(find toc/rfc/ -maxdepth 2 -type f -name 'rfc-draft-*')
TARGET_DOC=${SOURCE_DOC//rfc-draft/rfc-${RFC_ID}}
SOURCE_DIR=$(find toc/rfc/ -maxdepth 2 -type d -name 'rfc-draft-*')
TARGET_DIR=${SOURCE_DIR//rfc-draft/rfc-${RFC_ID}}
PR_NUMBER=$(git ls-remote origin 'pull/*/head' | grep -F -f <(git rev-parse HEAD) | awk -F'/' '{print $3}')

echo "> Updating document: ${SOURCE_DOC}"
SEDOPTION="-i"
if [[ "$OSTYPE" == "darwin"* ]]; then
  SEDOPTION="-i ''"
fi
sed $SEDOPTION "s|- RFC Pull Request:.*|- RFC Pull Request: [${REPO}#${PR_NUMBER}](https://github.com/${OWNER}/${REPO}/pull/${PR_NUMBER})|" "${SOURCE_DOC}"
sed $SEDOPTION "s|- Status:.*|- Status: Accepted|" "${SOURCE_DOC}"
sed $SEDOPTION "s|rfc-draft-|rfc-${RFC_ID}-|" "${SOURCE_DOC}"

echo "> Moving ${SOURCE_DOC} to ${TARGET_DOC}..."
git mv "${SOURCE_DOC}" "${TARGET_DOC}"
git add "${TARGET_DOC}"
if [ ! -z "$SOURCE_DIR" ] ; then
  git mv "${SOURCE_DIR}" "${TARGET_DIR}"
  git add "${TARGET_DIR}"
fi


echo "> Committing..."
git commit -m "Assigning RFC ${RFC_ID}"

echo "> Pushing..."
git push
