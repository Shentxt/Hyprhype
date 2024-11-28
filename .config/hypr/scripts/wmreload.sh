#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# ██╗    ██╗███╗   ███╗██████╗ ███████╗██╗      ██████╗  █████╗ ██████╗
# ██║    ██║████╗ ████║██╔══██╗██╔════╝██║     ██╔═══██╗██╔══██╗██╔══██╗
# ██║ █╗ ██║██╔████╔██║██████╔╝█████╗  ██║     ██║   ██║███████║██║  ██║
# ██║███╗██║██║╚██╔╝██║██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██║██║  ██║
# ╚███╔███╔╝██║ ╚═╝ ██║██║  ██║███████╗███████╗╚██████╔╝██║  ██║██████╔╝
#  ╚══╝╚══╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝
#
# Autor = Shen Blaskowitz
# Follow Me = https://github.com/Shentxt
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Windos Manager Reload
#
# a simple WM reload script
#
# required to function (only hyprland)
# --------------------
# hyprctl: wmreload
# notify-send: notify
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
sleep 1 && hyprctl reload && ignis reload
systemctl --user restart wireplumber pipewire pipewire-pulse

name=$(whoami)

notify-send "Morgana" "hey, ${name} we need to do an <span color='yellow'> emergency reboot </span>" -i ~/.config/hypr/assets/icons/persona/morgana.png
