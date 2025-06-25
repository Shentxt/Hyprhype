#!/usr/bin/env bash

# Kill
pkill modus
pkill -f "wallpaper"
pkill -f "wl-paste --watch sh -c"

name=$(whoami)

sleep 0.1

python ~/.config/Modus/main.py &
python ~/.config/Modus/config/scripts/wallpaper.py -P &

sleep 1.0

if ! pgrep -x modus > /dev/null; then
    echo "Modus failed to launch. Check for CSS/theme issues." > ~/.cache/error.txt
    hyprctl notify -0 10000 "rgb(ff0000)" "fontsize:14 Error: Modus is not running. Check error.txt"
else
    notify-send "Morgana" "hey, ${name} we need to do an <span color='yellow'> emergency reboot </span>" -i ~/.config/Modus/assets/Icon/fuuka.png
fi
