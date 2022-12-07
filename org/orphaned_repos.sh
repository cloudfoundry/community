#!/bin/bash

set -eu -o pipefail

comm -3 <(cat org/cloudfoundry.yml | spruce json \
           | jq -r '.orgs.cloudfoundry.repos | with_entries(select(.value.archived != true)) | keys | map("cloudfoundry/\(.)") | sort | unique | .[]') \
     <(./toc/working-groups/parsable-working-groups.sh \
           | jq -s -r 'map(map(.areas[].repositories)) | flatten | map(select(contains("cloudfoundry"))) | sort | unique | .[]')
