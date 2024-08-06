#!/bin/bash

state=$(eww get open_wallpaper_menu)

open_wallpaper_menu() {
    if [[ -z $(eww list-windows | grep '*wallpaper_menu') ]]; then
        eww open wallpaper_menu
    fi
    eww update open_wallpaper_menu=true
}

close_wallpaper_menu() {
    eww update open_wallpaper_menu=false
}

case $1 in
    close)
        close_wallpaper_menu
        exit 0;;
esac

case $state in
    true)
        close_wallpaper_menu;;
    false)
        open_wallpaper_menu;;
esac
