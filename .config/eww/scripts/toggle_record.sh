#!/bin/bash

state=$(eww get open_recorder_menu)

open_recorder_menu() {
    if [[ -z $(eww list-windows | grep '*recorder_menu') ]]; then
        eww open recorder_menu
    fi
    eww update open_recorder_menu=true
}

close_recorder_menu() {
    eww update open_recorder_menu=false
}

case $1 in
    close)
        close_recorder_menu
        exit 0;;
esac

case $state in
    true)
        close_recorder_menu;;
    false)
        open_recorder_menu;;
esac

