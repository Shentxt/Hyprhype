#!/bin/bash

state=$(eww get open_musiccenter)

open_musiccenter() {
    if [[ -z $(eww list-windows | grep '*musiccenter') ]]; then
        eww open musiccenter
    fi
    eww update open_musiccenter=true
}

close_musiccenter() {
    eww close musiccenter
    eww update open_musiccenter=false
}

case $1 in
    close)
        close_musiccenter
        exit 0;;
    open)
        open_musiccenter
        exit 0;;
esac

case $state in
    true)
        close_musiccenter
        exit 0;;
    false)
        open_musiccenter
        exit 0;;
esac
