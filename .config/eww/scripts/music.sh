#!/bin/bash

current_position=$(playerctl position)

if [ "$1" == "--up" ]; then
    new_position=$(echo "$current_position + 10" | bc)
elif [ "$1" == "--down" ]; then
    new_position=$(echo "$current_position - 10" | bc)
else
    echo "Uso: $0 --up | --down"
    exit 1
fi

playerctl position $new_position
