#!/bin/sh


# -------------------------------------------------------------
#
# ██╗    ██╗ █████╗ ██╗     ██╗     
# ██║    ██║██╔══██╗██║     ██║     
# ██║ █╗ ██║███████║██║     ██║     
# ██║███╗██║██╔══██║██║     ██║     
# ╚███╔███╔╝██║  ██║███████╗███████╗
#  ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Wallpaper
#
# a simple wallpaper script
#
# use of swww = swww --help more informations
# There is also simple,
# which simply fades into the new image, any, which starts at a random point with either center of outer transitions,
# and random, which selects a transition effect at random.
#
# required to function
# --------------------
# rofi: launcher
# swww: wallpaper
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Check if swww and imagemagick are installed
if ! command -v swww >/dev/null 2>&1; then
	dunstify "Missing package" "Please install the swww package to continue" -u critical
	exit 1
elif ! command -v convert >/dev/null 2>&1; then
	dunstify "Missing package" "Please install the imagemagick package to continue" -u critical
	exit 1
fi

# Set some variables
wall_dir="${HOME}/.config/hypr/assets/walls"
cacheDir="${HOME}/.cache"
rofi_command="rofi -dmenu -theme ${HOME}/.config/rofi/themes/WallSelect.rasi -theme-str ${rofi_override}"

# Create cache dir if not exists
if [ ! -d "${cacheDir}" ]; then
	mkdir -p "${cacheDir}"
fi

# Convert images in directory and save to cache dir
for imagen in "$wall_dir"/*.{jpg,jpeg,png,webp}; do
	if [ -f "$imagen" ]; then
		nombre_archivo=$(basename "$imagen")
		if [ ! -f "${cacheDir}/${nombre_archivo}" ]; then
			convert -strip "$imagen" -thumbnail 500x500^ -gravity center -extent 500x500 "${cacheDir}/${nombre_archivo}"
		fi
	fi
done

# Launch rofi
wall_selection=$(find "${wall_dir}" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) -exec basename {} \; | sort | while read -r A; do echo -en "$A\x00icon\x1f""${cacheDir}"/"$A\n"; done | $rofi_command)

# Set wallpaper
[[ -n "$wall_selection" ]] || exit 1
swww img -t any --transition-bezier 0.0,0.0,1.0,1.0 --transition-duration 1 --transition-step 255 --transition-fps 60 "${wall_dir}"/"${wall_selection}"
exit 0

