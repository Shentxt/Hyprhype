#!/bin/bash

# -------------------------------------------------------------------------
#
# ██╗      ██████╗  ██████╗██╗  ██╗
# ██║     ██╔═══██╗██╔════╝██║ ██╔╝
# ██║     ██║   ██║██║     █████╔╝ 
# ██║     ██║   ██║██║     ██╔═██╗ 
# ███████╗╚██████╔╝╚██████╗██║  ██╗
# ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Lockscreen
#
# just block, there is not much science behind this
#
# required to function
# --------------------
# rofi: launcher
# kitty: terminal
# notify-send: really?
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

lock_screen() {
    notify-send 'Mitsuru' 'The screen will <span color=yellow>lock in 10 seconds</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png
    sleep 30
    hyprlock -c ~/.config/hypr/rules/hyprlock.conf
}

unlock_screen() {
    notify-send 'Mitsuru' 'The screen <span color=yellow>has been unlocked</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png
}

wayland-pipewire-idle-inhibit -w -d 30
    "$(lock_screen)" \
    "$(unlock_screen)"
