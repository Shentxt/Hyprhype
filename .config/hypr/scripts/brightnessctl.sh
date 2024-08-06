#!/bin/bash

# requieres brightnessctl

case $1 in
--up)
  brightnessctl -n >/dev/null
  brightnessctl s 5%+ >/dev/null
  ;;
--down)
  brightnessctl -n >/dev/null
  brightnessctl s 5%- >/dev/null
  ;;
--toggle)
  brightnessctl -n >/dev/null
  ;;
esac

