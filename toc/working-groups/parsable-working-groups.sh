#!/bin/bash

set -eu -o pipefail

repo_root=$(dirname $(cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd))

pushd $repo_root/toc/working-groups >/dev/null

for working_group in $(ls *.md | grep -v -e WORKING-GROUPS -e paketo -e vulnerability); do
    cat ${working_group} | awk '/^```yaml$/{flag=1;next}/^```$/{flag=0}flag' | spruce json | jq '[.]' | bosh int -
done
