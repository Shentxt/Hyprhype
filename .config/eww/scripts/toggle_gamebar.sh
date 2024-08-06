#!/bin/bash

state=$(eww get open_gamebar)

open_gamebar() {
    if [[ -z $(eww list-windows | grep '*gamebar') ]]; then
        eww open gamebar
    fi
    eww update open_gamebar=true
}

close_gamebar() {
    eww update open_gamebar=false
}

case $1 in
    close)
        close_gamebar
        exit 0;;
esac

case $state in
    true)
        close_gamebar;;
    false)
        open_gamebar;;
esac
