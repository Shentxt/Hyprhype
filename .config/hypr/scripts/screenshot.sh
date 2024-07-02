#!/usr/bin/env bash

# -------------------------------------------------------------
#
# ███████╗ ██████╗██████╗ ███████╗███████╗███╗   ██╗███████╗██╗  ██╗ ██████╗ ████████╗
# ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║██╔════╝██║  ██║██╔═══██╗╚══██╔══╝
# ███████╗██║     ██████╔╝█████╗  █████╗  ██╔██╗ ██║███████╗███████║██║   ██║   ██║   
# ╚════██║██║     ██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║╚════██║██╔══██║██║   ██║   ██║   
# ███████║╚██████╗██║  ██║███████╗███████╗██║ ╚████║███████║██║  ██║╚██████╔╝   ██║   
# ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Screenshot
#
# a simple screenshot script
#
# required to function
# --------------------
# grimblast: screenshot
# viewnior: show screen
# notify-send: notify
# wl-copy: copy img
# rofi: launch script
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Import
DIR="$HOME/.config/hypr"
STYLE="default"
RASI="/home/shen/.config/rofi/themes/default.rasi"


# Theme Elements
prompt='Screenshot'
mesg="Directory :: $(xdg-user-dir PICTURES)/Screenshots"

# Options
layout=$(cat ${RASI} | grep 'USE_ICON' | cut -d'=' -f2)
if [[ "$layout" == 'NO' ]]; then
	options=("Capture Desktop" "Capture Area" "Capture Window" "Capture in 5s" "Capture in 10s")
else
	options=("󰹑  Capture Desktop" "󰋫  Capture Area" "  Capture Window" "󱑍  Capture in 5s" "󱑍  Capture in 10s")
fi

# Rofi CMD
rofi_cmd() {
    rofi -dmenu -p "$prompt" -mesg "$mesg" 
}

# Screenshot
time=$(date +%Y-%m-%d-%H-%M-%S)
geometry=$(xrandr | grep 'current' | head -n1 | cut -d',' -f2 | tr -d '[:blank:],current')
dir="$(xdg-user-dir PICTURES)/Screenshots"
file="Screenshot_${time}_${geometry}.png"

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
		-p "$prompt" \
		-mesg "$mesg" \
		-markup-rows \
		-theme ${RASI}
}

# Directory
if [[ ! -d "$dir" ]]; then
	mkdir -p "$dir"
fi

# notify and view screenshot
notify_view() {
	viewnior "${dir}/${file}"
  if [[ -e "${dir}/${file}" ]]; then
    wl-copy < "${dir}/${file}"
    wl-paste > /tmp/image.png
    notify-send "Makoto" "Screenshot <span color='yellow'>Saved</span>." -i /tmp/image.png
else
    notify-send "Makoto" "Screenshot <span color='yellow'>Deleted</span>." -i ~/.config/hypr/assets/icons/persona/makoto.png
fi	
}

# countdown
countdown() {
	for sec in $(seq "$1" -1 1); do
		notify-send "Makoto" "Taking shot in :<span color='yellow'>$sec</span>" -i ~/.config/hypr/assets/icons/persona/makoto.png
		sleep 1
	done
}

# take shots
shotnow() {
	sleep 1 && cd "${dir}" && sleep 0.15 && grimblast save output "${file}" | copy_shot
	notify_view
}

shot5() {
	countdown '5'
	sleep 2 && cd "${dir}" && grimblast save output "${file}" | copy_shot
	notify_view
}

shot10() {
	countdown '10'
	sleep 2 && cd "${dir}" && grimblast save output "${file}" | copy_shot
	notify_view
}

shotwin() {
	sleep 1 && cd "${dir}" && grimblast save active "${file}" | copy_shot
	notify_view
}

shotarea() {
	sleep 1 && cd "${dir}" && grimblast save area "${file}" | copy_shot
	notify_view
}

# Execute Command
run_cmd() {
	case "$1" in
	"${options[0]}")
		shotnow
		;;
	"${options[1]}")
		shotarea
		;;
	"${options[2]}")
		shotwin
		;;
	"${options[3]}")
		shot5
		;;
	"${options[4]}")
		shot10
		;;
	esac
}

# Actions
chosen="$(printf '%s\n' "${options[@]}" | rofi_cmd)"
run_cmd "$chosen"
