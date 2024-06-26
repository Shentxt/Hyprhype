#!/usr/bin/env bash

# -------------------------------------------------------------
#
#  ██████╗ ██████╗ ██╗      ██████╗ ██████╗ 
# ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗
# ██║     ██║   ██║██║     ██║   ██║██████╔╝
# ██║     ██║   ██║██║     ██║   ██║██╔══██╗
# ╚██████╗╚██████╔╝███████╗╚██████╔╝██║  ██║
#  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Colorpicker
#
# a simple colorpicker script
#
# required to function
# --------------------
# hyprpicker: colorpicker
# hyprctl: notify
# wl-paste: past color
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

color=$(hyprpicker)

# Check if color is null or empty
if [[ -z "$color" ]]; then
	notify-send "Ann" "Seems like the color selection was canceled or no color was detected. Don't worry, we'll find the perfect color next time!" -i ~/.config/hypr/assets/icons/persona/ann.png
	exit 1
fi

image=/tmp/${color}.png

main() {
	# copy color code to clipboard
	echo $color | tr -d "\n" | wl-copy 
	# generate preview
	convert -size 48x48 xc:"$color" ${image}
	# notify about it
	dunstify -u low -h string:x-dunst-stack-tag:obcolorpicker -i ${image} "Ann" "That $color is so elegant"
}

# run the script
main
