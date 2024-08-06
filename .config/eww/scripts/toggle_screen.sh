#!/bin/bash

state=$(eww get open_screen_menu)

open_screen_menu() {
    if [[ -z $(eww list-windows | grep '*screen_menu') ]]; then
        eww open screen_menu
    fi
    eww update open_screen_menu=true
}

close_screen_menu() {
    eww update open_screen_menu=false
}

case $1 in
    close)
        close_screen_menu
        exit 0;;
esac

case $state in
    true)
        close_screen_menu;;
    false)
        open_screen_menu;;
esac
