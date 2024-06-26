#!/bin/bash

state=$(eww get open_notifications)

open_notifications() {
    if [[ -z $(eww list-windows | grep '*notifications') ]]; then
        eww open notifications
    fi
    eww update open_notifications=true
}

close_notifications() {
    eww update open_notifications=false
}

case $1 in
    --toggle)
        if [[ $state == "true" ]]; then
            close_notifications
        else
            open_notifications
        fi
        exit 0;;
esac
