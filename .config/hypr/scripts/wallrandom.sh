#!/usr/bin/env bash

# -------------------------------------------------------------
#
# ██╗    ██╗ █████╗ ██╗     ██╗     ██████╗  █████╗ ███╗   ██╗██████╗  ██████╗ ███╗   ███╗
# ██║    ██║██╔══██╗██║     ██║     ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔═══██╗████╗ ████║
# ██║ █╗ ██║███████║██║     ██║     ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║██╔████╔██║
# ██║███╗██║██╔══██║██║     ██║     ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██║   ██║██║╚██╔╝██║
# ╚███╔███╔╝██║  ██║███████╗███████╗██║  ██║██║  ██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚═╝ ██║
# ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Wallpaper random Manager
#
# a simple WallRandom reload script
#
# required to function (only hyprland)
# --------------------
# swww: wallpaper
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

wall=$(find ~/.config/hypr/assets/walls -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | shuf -n 1)

swww img -t any --transition-bezier 0.0,0.0,1.0,1.0 --transition-duration 1 --transition-step 255 --transition-fps 60 $wall &
wal -i $wall && reload &
