#!/bin/bash

file="$(xdg-user-dir PICTURES)/$(date '+%F_%T_%:::z.png')"

# The Span is not in second
countdown() {
    for sec in $(seq "$1" -1 1); do
      notify-send "Makoto" "Taking shot in: $sec Sec." -i ~/.config/hypr/assets/icons/persona/makoto.png
        sleep 1
    done
}

notify_view() {
    if [[ -e "${file}" ]]; then
        wl-copy < "${file}"
        wl-paste > /tmp/image.png
        notify-send "Makoto" "Screenshot <span color='yellow'>Saved</span>." -i /tmp/image.png
    else
        notify-send "Makoto" "Screenshot <span color='yellow'>Deleted</span>." -i ~/.config/hypr/assets/icons/persona/makoto.png
    fi
}

eww update use_timer=false
eww close screen_menu

# Parse parameters
mode=$1
use_timer=$2

if [[ $use_timer == "true" ]]; then
    countdown 5
fi

case $mode in
    now)
        sleep 1 && grimblast save output "${file}" | copy_shot
        notify_view
        ;;
    windows)
        sleep 1 && grimblast save active "${file}" | copy_shot
        notify_view
        ;;
    area)
        sleep 1 && grimblast save area "${file}" | copy_shot
        notify_view
        ;;
    *)
        notify-send "Error" "Invalid mode selected" -i ~/.config/hypr/assets/icons/persona/makoto.png
        ;;
esac
