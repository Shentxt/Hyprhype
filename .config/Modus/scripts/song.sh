#!/bin/bash

CACHE_FILE="/tmp/last_song_notify.txt"
THUMB_DIR="$HOME/.cache/thumbnails"
mkdir -p "$THUMB_DIR"
MUSIC_ART="$THUMB_DIR/music_art.png"

for cmd in playerctl notify-send curl; do
    command -v "$cmd" >/dev/null || { echo "Falta $cmd"; exit 1; }
done

get_metadata() {
    playerctl metadata --format '{{title}}|{{artist}}|{{mpris:artUrl}}' 2>/dev/null
}

get_album_art() {
    local art_url="$1"

    if [[ "$art_url" == file://* ]]; then
        cp -f "${art_url#file://}" "$MUSIC_ART" 2>/dev/null
    elif [[ "$art_url" == http* ]]; then
        curl -sfL "$art_url" -o "$MUSIC_ART"
    else
        cp -f "/usr/share/icons/Adwaita/256x256/actions/media-playback-start.png" "$MUSIC_ART"
    fi

    echo "$MUSIC_ART"
}

send_notification() {
    notify-send -u low "  $1" "$2" -i "$MUSIC_ART"
}

monitor_player() {
    playerctl -F status 2>/dev/null | while read -r status; do
        if [[ "$status" == "Playing" ]]; then
            metadata=$(get_metadata)
            IFS="|" read -r title artist art_url <<< "$metadata"

            [[ -z "$title" || -z "$artist" ]] && continue

            current_hash="$title - $artist - $art_url"
            if [[ "$current_hash" != "$(cat "$CACHE_FILE" 2>/dev/null)" ]]; then
                get_album_art "$art_url"    
                send_notification "$artist" "$title"
                echo "$current_hash" > "$CACHE_FILE"
            fi
        fi
    done
}

case "$1" in
  --song)
    IFS="|" read -r title artist _ <<< "$(get_metadata)"
    echo -e "  $artist\n$title"
    ;;
  --notify)
    monitor_player
    ;;
  *)
    echo "Uso: $0 [--song|--notify]"
    exit 1
    ;;
esac
