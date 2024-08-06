#!/bin/bash

brightnessctl g | awk '{print int(($1 / 255) * 100)}'

udevadm monitor --udev | grep --line-buffered "backlight" | while read -r _; do
  brightnessctl g | awk '{print int(($1 / 255) * 100)}'
done

