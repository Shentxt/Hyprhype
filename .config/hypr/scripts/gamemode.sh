#!/bin/bash

source ~/.config/hypr/scripts/borderandom.sh

gamemode_file="/tmp/gamemode.txt"

mod_disable () {
    hyprctl keyword animations:enabled false
    hyprctl keyword decoration:blur:enabled false
    hyprctl keyword decoration:active_opacity 1.0
    hyprctl keyword decoration:inactive_opacity 1.0
    hyprctl keyword decoration:rounding 0
    hyprctl keyword decoration:blur:noise 0
    hyprctl keyword general:col.active_border 0
    hyprctl keyword general:col.inactive_border 0
    hyprctl keyword general:gaps_in 0
    hyprctl keyword general:gaps_out 0
    hyprctl keyword general:border_size 0
    ~/.config/eww/scripts/notifications.sh togglednd
    eww close bar
    eww close dock
    eww close bg_widgets
}

mod_enable () {
    hyprctl keyword animations:enabled true
    hyprctl keyword decoration:blur:enabled true
    hyprctl keyword decoration:active_opacity 0.6
    hyprctl keyword decoration:inactive_opacity 0.5
    hyprctl keyword decoration:rounding 12
    hyprctl keyword decoration:blur:size 3
    hyprctl keyword decoration:blur:noise 0.2
    hyprctl keyword general:col.active_border $(random_hex) $(random_hex) $(random_hex) 270deg
    hyprctl keyword general:col.inactive_border $(random_hex) $(random_hex) $(random_hex) 270deg
    hyprctl keyword general:gaps_in 5
    hyprctl keyword general:gaps_out 20
    hyprctl keyword general:border_size 2
    ~/.config/eww/scripts/notifications.sh togglednd
    eww open bar
    eww open dock
    eww open bg_widgets
}

if [ -f "$gamemode_file" ]; then
    gamemode=$(cat "$gamemode_file")
else
    gamemode="false"
fi

if [ "$gamemode" = "true" ]; then
    mod_disable
    echo "false" > "$gamemode_file"
else
    mod_enable
    echo "true" > "$gamemode_file"
fi
