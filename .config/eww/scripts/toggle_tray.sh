#!/bin/bash

state=$(eww get open_tray)

open_tray() {
    if [[ -z $(eww list-windows | grep '*tray') ]]; then
        eww open tray
    fi
    eww update open_tray=true
}

close_tray() {
    eww update open_tray=false
}

update_tray_status() {
    if [[ $state == "true" ]]; then
        echo " "
    else
        echo " "
    fi
}

case $1 in
    --toggle)
        if [[ $state == "true" ]]; then
            close_tray
        else
            open_tray
        fi
        exit 0;;
    --status)
        update_tray_status
        exit 0;;
esac
