#!/bin/bash

set -eu -o pipefail

repo_root=$(dirname $(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd))

$repo_root/toc/working-groups/parsable-working-groups.sh | \
    jq 'map(select(.config | has("github_project_sync"))) |
      map(
        .name as $name |
        .areas as $areas |
        .config.github_project_sync.mapping | to_entries | map({org: .key, project_id: .value}) |
           map(.org as $org | {
              project: {organization: $org, number: .project_id},
              repositories: $areas | map(
                .name as $area |
                .repositories | map(select(startswith("\($org)/"))) | map({
                  name: .,
                  fields: [
                    {name: "Last Activity", type: "last_activity"},
                    {name: "Status", type: "default_single_select", value: "Inbox"},
                    {name: "Submitter", type: "author"},
                    {name: "Draft", type: "draft"},
                    {name: "Area", type: "single_select", value: $area},
                    {name: "Type", type: "type"},
                    {name: "Changes", type: "changes"}
                  ]
                })
              ) | flatten
           })
      )
    ' | jq -cs 'flatten'
