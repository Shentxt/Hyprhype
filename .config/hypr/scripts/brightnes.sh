#!/bin/bash

# -------------------------------------------------------------------------
#
# ██████╗ ██████╗ ██╗ ██████╗ ██╗  ██╗████████╗███╗   ██╗███████╗███████╗███████╗
# ██╔══██╗██╔══██╗██║██╔════╝ ██║  ██║╚══██╔══╝████╗  ██║██╔════╝██╔════╝██╔════╝
# ██████╔╝██████╔╝██║██║  ███╗███████║   ██║   ██╔██╗ ██║█████╗  ███████╗███████╗
# ██╔══██╗██╔══██╗██║██║   ██║██╔══██║   ██║   ██║╚██╗██║██╔══╝  ╚════██║╚════██║
# ██████╔╝██║  ██║██║╚██████╔╝██║  ██║   ██║   ██║ ╚████║███████╗███████║███████║
# ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Brightness
#
# a simple brightness script
#
# required to function
# --------------------
# wlsunset: brightness
# dunst: notify
# awk: print the message
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
change_brightness() {
    wlsunset -g "$1"
    notify-send "Brightness change a $1"
}

# Programa el cambio de brillo
while true; do
    hour=$(date +%H)
    if (( 6 <= hour && hour < 12 )); then
        change_brightness 1.0
    elif (( 12 <= hour && hour < 18 )); then
        change_brightness 0.6
    else
        change_brightness 1.0
    fi
    sleep 1h
done
