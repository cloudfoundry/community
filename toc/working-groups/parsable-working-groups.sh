#!/bin/bash

set -eu -o pipefail

get_working_group_info_json() {
  local group=$1
  echo $(cat ${group} | awk '/^```yaml$/{flag=1;next}/^```$/{flag=0}flag' | yq -oj '.')
}

repo_root=$(dirname $(cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd))

pushd $repo_root/toc/working-groups >/dev/null

working_group_info="[]"

for group in $(ls ../*.md | grep -v -e ROLES -e CHANGEPLAN -e PRINCIPLES -e GOVERNANCE); do
     working_group_info=$(echo "${working_group_info}" | working_group_information_json="$(get_working_group_info_json $group)" yq -oj -I=0 '. + [env(working_group_information_json)]')
done

for working_group in $(ls *.md | grep -v -e WORKING-GROUPS -e paketo -e vulnerability -e concourse); do
     working_group_info=$(echo "${working_group_info}" | working_group_information_json="$(get_working_group_info_json $working_group)" yq -oj -I=0 '. + [env(working_group_information_json)]')
done

echo $working_group_info
