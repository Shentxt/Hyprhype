#!/usr/bin/env bash

# -------------------------------------------------------------
#
# ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗██╗   ██╗███████╗
# ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝
# ██╔████╔██║███████║██████╔╝█████╔╝ █████╗   ╚████╔╝ ███████╗
# ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═██╗ ██╔══╝    ╚██╔╝  ╚════██║
# ██║ ╚═╝ ██║██║  ██║██║     ██║  ██╗███████╗   ██║   ███████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝
#
# ----- Author: Shen - url: https://github.com/Shentxt ----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Mapkeys
#
# a simple mapkeys of Wm script
#
# required to function
# --------------------
# awk: organizer 
# rofi: ui
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

awk '/^[a-z]/ && last {print $0,"\t",last} {last=""} /^#/{last=$0}' ~/.config/hypr/rules/keybinds.conf |
column -t -s $'\t' | 
awk '{$1=$1; print}' |
rofi -dmenu -i -markup-rows -no-show-icons -width 1000 -lines 15 -yoffset 40 -theme $HOME/.config/rofi/themes/default1.rasi
