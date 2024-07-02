#!/bin/bash

# -----------------------------------------------------------------------------------
#
# ██╗   ██╗████████╗███╗   ███╗██████╗ ██████╗ 
# ╚██╗ ██╔╝╚══██╔══╝████╗ ████║██╔══██╗╚════██╗
#  ╚████╔╝    ██║   ██╔████╔██║██████╔╝ █████╔╝
#   ╚██╔╝     ██║   ██║╚██╔╝██║██╔═══╝  ╚═══██╗
#    ██║      ██║   ██║ ╚═╝ ██║██║     ██████╔╝
#    ╚═╝      ╚═╝   ╚═╝     ╚═╝╚═╝     ╚═════╝ 
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# music folder
if [[ -d "${XDG_MUSIC_DIR:-$HOME/Music}" ]]; then
    MUSIC_DIR="${XDG_MUSIC_DIR:-$HOME/Music}"
elif [[ -d "$HOME/Música" ]]; then
    MUSIC_DIR="$HOME/Música"
else
     notify-send "Haru" "The necessary <span color='yellow'>files</span> have not been found." -i ~/.config/hypr/assets/icons/persona/haru.png
    exit 1
fi

# Menu
function mostrar_menu {
    echo "1) Download Music"
    echo "2) Exit"
}

# while
while true; do
    mostrar_menu
    read -p "Choose an option: " opcion
    case $opcion in
        1)
            read -p "Enter the url of YT: " url
            if yt-dlp -x --audio-format mp3 --audio-quality 0 -P "$MUSIC_DIR" -o "%(title)s.%(ext)s" "$url"; then
                notify-send "Ren" "new <span color='yellow'>soundtrack</span>? amazing it's time to try it." -i ~/.config/hypr/assets/icons/persona/ren.png
            else
                notify-send "Futaba" "Oops! It seems there was a problem with the <span color='yellow'>Url</span> you entered. Please try again." -i ~/.config/hypr/assets/icons/persona/futaba.png
            fi
            ;;
        2)
            pkill kitty --title "Float"
            ;;
        *)
            echo "invalid option"
            ;;
    esac
done
