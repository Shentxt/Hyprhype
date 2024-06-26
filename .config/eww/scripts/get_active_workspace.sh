#!/usr/bin/env bash

while true; do
    workspace_id=$(hyprctl monitors -j | jq '.[] | select(.focused) | .activeWorkspace.id')
    echo $workspace_id
done
