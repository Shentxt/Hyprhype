#!/bin/bash

# -----------------------------------------------------------------------------------
#
# ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
# ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
# ██████╔╝█████╗  ██║     ██║   ██║██████╔╝██║  ██║██║██╔██╗ ██║██║  ███╗
# ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██╗██║  ██║██║██║╚██╗██║██║   ██║
# ██║  ██║███████╗╚██████╗╚██████╔╝██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# Import Current Theme
DIR="$HOME/.config/hypr"
STYLE="default"
RASI="~/.config/rofi/themes/default.rasi"

# Theme Elements
prompt='Screen Recording'
mesg="Directory :: $(xdg-user-dir VIDEOS)/ScreenRecordings"

# Options
layout=$(cat ${RASI} | grep 'USE_ICON' | cut -d'=' -f2)
if [[ "$layout" == 'NO' ]]; then
	option_1="  Start Recording (Sound)"
  option_2="  Start Recording"
	option_3="  Stop Recording"
else
  option_1="  Start Recording (Sound)"
	option_2="  Start Recording"
	option_3="  Stop Recording"
fi

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
		-p "$prompt" \
		-mesg "$mesg" \
		-markup-rows \
		-theme ${RASI}
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e "$option_1\n$option_2\n$option_3" | rofi_cmd
}

# Screen Recording
time=$(date +%Y-%m-%d-%H-%M-%S)
dir="$(xdg-user-dir VIDEOS)/Screenrecordings"
file="Screenrecording_${time}.mp4"

# Directory
if [[ ! -d "$dir" ]]; then
	mkdir -p "$dir"
fi

# Start Recording
start_recording() {
  wf-recorder -f "${dir}/${file}"
  echo $! > /tmp/recording.pid
	notify-send "Akechi" "Recording <span color='yellow'>Started</span>." -i  ~/.config/hypr/assets/icons/persona/akechi.png
	paplay ~/.config/hypr/assets/effects/system.ogg &>/dev/null &
}

# Start Recording with Sound
start_recording_sound() {
	wf-recorder -a -f "${dir}/${file}"
	echo $! > /tmp/recording.pid
	notify-send "Akechi" "Recording <span color='yellow'>(with sound)</span> started." -i  ~/.config/hypr/assets/icons/persona/akechi.png
  paplay ~/.config/hypr/assets/effects/system.ogg &>/dev/null &
}

# Stop Recording
stop_recording() {
	kill $(cat /tmp/recording.pid)
	rm /tmp/recording.pid
	notify-send "Akechi" "Recording <span color='yellow'>Stopped</span>."  -i  ~/.config/hypr/assets/icons/persona/akechi.png
  paplay ~/.config/hypr/assets/effects/system.ogg &>/dev/null &
}

# Execute Command
run_cmd() {
  if [[ "$1" == '--opt1' ]]; then
    start_recording_sound
	elif [[ "$1" == '--opt2' ]]; then
		start_recording
	elif [[ "$1" == '--opt3' ]]; then
		stop_recording
	fi
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
$option_1)
	run_cmd --opt1
	;;
$option_2)
	run_cmd --opt2
	;;
$option_3)
	run_cmd --opt3
	;;
esac
