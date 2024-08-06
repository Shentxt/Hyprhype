#!/bin/bash

no_error() {
    pkill checkbrightness.sh
    ~/.config/eww/scripts/checkbrightness.sh &
}

error() {
    ~/.config/eww/scripts/checkbrightness.sh &
}

no_error || error


case $1 in
--up)
  brightnessctl s +5% >/dev/null
  ;;
--down)
  brightnessctl s -5% >/dev/null
  ;;
--toggle)
  
  BRIGHTNESS_LOW=30
  BRIGHTNESS_HIGH=100

  current_brightness=$(brightnessctl g | awk '{print int(($1 / 255) * 100)}')

  if [ "$current_brightness" -le "$BRIGHTNESS_LOW" ]; then
      brightnessctl s "${BRIGHTNESS_HIGH}%" >/dev/null
  else
      brightnessctl s "${BRIGHTNESS_LOW}%" >/dev/null
  fi
  ;;
esac
