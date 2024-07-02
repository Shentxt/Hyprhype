#!/bin/bash

prev_title=""

check_and_notify() {
    players=$(playerctl -l)

    for player in $players; do
        state=$(playerctl -p "$player" status)

        if [ "$state" = "Playing" ]; then
            artist=$(playerctl -p "$player" metadata --format '{{ artist }}')
            title=$(playerctl -p "$player" metadata --format '{{ title }}')
            url=$(playerctl -p "$player" metadata --format "{{ mpris:artUrl }}" | sed 's/b273/1e02/') 

            if [[ "$title" != "$prev_title" && -n "$title" ]]; then
                prev_title="$title"

                if [ -z "$artist" ]; then
                    artist="Uknow"
                fi

                if [ -z "$title" ]; then
                    title="Uknow Title"
                fi

                if [ -z "$url" ]; then 
                   img="/home/shen/.config/eww/images/music.jpg"
                else 
                   img="$url"
                fi

                convert "$img" /tmp/cover.jpg
                notify-send "$artist" "$title" -i /tmp/cover.jpg
            fi

            break
        fi
    done
}

while true; do
    check_and_notify
    sleep 1  
done
