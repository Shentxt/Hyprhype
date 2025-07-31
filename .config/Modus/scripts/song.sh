#!/bin/bash

print_song() {
  song_title=$(playerctl metadata --format '{{title}}' 2>/dev/null)
  song_artist=$(playerctl metadata --format '{{artist}}' 2>/dev/null)
  echo -e "  $song_artist\n$song_title"
}

send_notify() {
  CACHE_FILE="/tmp/last_song_notify.txt"
  THUMB_DIR="$HOME/.cache/thumbnails"
  mkdir -p "$THUMB_DIR"

  while true; do
    status=$(playerctl status 2>/dev/null)
    if [[ "$status" != "Playing" ]]; then
      sleep 10
      continue
    fi

    song_title=$(playerctl metadata --format '{{title}}' 2>/dev/null)
    song_artist=$(playerctl metadata --format '{{artist}}' 2>/dev/null)
    current_song="${song_title} - ${song_artist}"

    if [[ "$current_song" != "$(cat "$CACHE_FILE" 2>/dev/null)" ]]; then
      song_file=$(playerctl metadata mpris:artUrl 2>/dev/null | sed 's/^file:\/\///')

      if [[ -f "$song_file" ]]; then
        ffmpeg -y -i "$song_file" -an -vcodec copy "$THUMB_DIR/cover.jpg" 2>/dev/null

        if [[ -f "$THUMB_DIR/cover.jpg" ]]; then
          convert "$THUMB_DIR/cover.jpg" -resize 128x128^ -gravity center -extent 128x128 \
            -alpha on -background none \
            \( +clone -alpha extract -draw 'fill black polygon 0,0 0,128 128,128 fill white circle 64,64 64,0' -alpha off \) \
            -compose copy_opacity -composite "$THUMB_DIR/profile.png"
        fi
      fi

      notify-send "  $song_artist" "$song_title" -i "$THUMB_DIR/profile.png"
      echo "$current_song" > "$CACHE_FILE"
    fi
    sleep 10
  done
}

case "$1" in
  --song)
    print_song
    ;;
  --notify)
    send_notify
    ;;
  *)
    echo "Uso: $0 [--song|--notify]"
    exit 1
    ;;
esac
