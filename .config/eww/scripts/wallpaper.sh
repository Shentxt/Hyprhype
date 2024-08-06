#!/bin/bash

# Directorio de imágenes
wall_dir="${HOME}/.config/hypr/assets/walls"
list_file="${HOME}/.cache/wallpapers_list.txt"

# Función para generar la lista de imágenes
dir_wallpaper() {
    find "$wall_dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) -exec basename {} \; | sort > "$list_file"
}

# Función para establecer el wallpaper
set_wallpaper() {
    local image="$1"
    swww img -t any --transition-bezier 0.0,0.0,1.0,1.0 --transition-duration 1 --transition-step 255 --transition-fps 60 "${wall_dir}/${image}"
}

# Verificar argumentos
case "$1" in
    --set)
        image_name="$2"
        set_wallpaper "$image_name"
        ;;
    --dir)
        dir_wallpaper
        ;;
    *)
        echo "Usage: $0 --set <image_name> | --reload"
        exit 1
        ;;
esac
