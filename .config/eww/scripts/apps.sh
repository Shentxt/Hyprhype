#!/bin/bash

# config variables desktop
export XDG_EMAIL_CLIENT=thunderbird
export XDG_AUDIO_PLAYER=mpv
export XDG_VIDEO_PLAYER=mpv
export XDG_WEB_BROWSER=brave
export XDG_FILE_MANAGER=thunar  
export XDG_TERMINAL=kitty

open_default_browser() {
    if command -v "$XDG_WEB_BROWSER" &> /dev/null; then
        "$XDG_WEB_BROWSER" "https://alljavi.github.io/tartarus-startpage/" &
    else
        xdg-open "https://alljavi.github.io/tartarus-startpage/"
    fi
}

open_default_terminal() {
    if command -v "$XDG_TERMINAL" &> /dev/null; then
        "$XDG_TERMINAL" &
    else
        x-terminal-emulator &
    fi
}

open_default_file_manager() {
    if command -v "$XDG_FILE_MANAGER" &> /dev/null; then
        "$XDG_FILE_MANAGER" &
    else
        xdg-open . &
    fi
}

number_trash(){
    trash_count=$(ls -1 ~/.local/share/Trash/files | wc -l)
   echo "$trash_count"
}

open_default_trash() {
  "$XDG_FILE_MANAGER" "trash:///" & 
}

case "$1" in
    --browser)
        open_default_browser
        ;;
    --terminal)
        open_default_terminal
        ;;
    --file-manager)
        open_default_file_manager
        ;;
    --trash)
        open_default_trash
        ;;
    --ntrash)
       number_trash
       ;;
    *)
esac
