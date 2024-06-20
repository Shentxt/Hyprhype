#!/bin/bash

while true; do
    hyprctl workspaces -j | jq -c 'sort_by(.id)'
    sleep 1
done
