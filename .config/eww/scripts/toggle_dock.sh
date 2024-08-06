#!/bin/bash

open_dock() {
    if [[ -z $(eww list-windows | grep '*dock') ]]; then
        eww open dock
    fi
    eww update open_dock=true
}

close_dock() {
    eww update open_dock=false
}

while true; do
    workspace_info=$(hyprctl activeworkspace)
    windows=$(echo "$workspace_info" | grep "windows:" | awk '{print $2}')

    if [ "$windows" -eq 0 ]; then
        open_dock
    else
        close_dock
    fi

    while true; do
        new_workspace_info=$(hyprctl activeworkspace)
        new_windows=$(echo "$new_workspace_info" | grep "windows:" | awk '{print $2}')

        if [ "$new_windows" != "$windows" ]; then
            break
        fi

        sleep 1
    done
done
