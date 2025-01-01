#!/bin/bash

hora=$(date +%H)

if [ "$hora" -eq 20 ]; then
  hyprsunset --temperature 4000
  
  notify-send "Fuuka" "Night filter activated. Temperature set to 4000K" -i ~/.config/hypr/assets/icons/persona/fuuka.png
fi

if [ "$hora" -eq 6 ]; then
  hyprsunset --identity
  
  notify-send "Fuuka" "Night filter disabled. Temperature restored" -i ~/.config/hypr/assets/icons/persona/fuuka.png
fi
