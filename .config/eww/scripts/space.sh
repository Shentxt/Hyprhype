#!/bin/bash

active_window_id=$(hyprctl activewindow 2>/dev/null)
if [ "$active_window_id" != "0" ] && [ -n "$active_window_id" ]; then
  window_class=$(hyprctl clients | grep "$active_window_id" | awk '{print $2}' | tr -d ' "')
else
    window_class=""
fi

ICON=""

case $window_class in
    *firefox*)
        ICON=""
        ;;
    *org.wezfurlong.wezterm*)
        ICON=""
        ;;
    *thunar*)
        ICON=""
        ;;
    *copyq*)
        ICON="󱓥"
        ;;
    *stalonetray*)
        ICON="󱊖"
        ;;
    *blueberry.py*)
        ICON=""
        ;;
    *pavucontrol*)
        ICON="󱡫"
        ;;
    *YouTube*)
        ICON="󰗃"
        ;;
    *code-oss*)
        ICON="󰨞"
        ;;
    *Wezterm*)
        ICON=""
        ;;
    *alacritty*)
        ICON=""
        ;;
    *Alacritty*)
        ICON=""
        ;;
    *kitty*)
        ICON=""
        ;;
    *gimp-2.10*)
        ICON="󱋆"
        ;;
    *Mugshot*)
        ICON="󰚼"
        ;;
    *xfce4-about*)
        ICON="󱋅"
        ;;
    *audacity*)
        ICON=""
        ;;
    *qt5ct*)
        ICON=""
        ;;
    *cmake-gui*)
        ICON=""
        ;;
    *amberol*)
        ICON="󱍙"
        ;;
    *ark*)
        ICON=""
        ;;
    *BleachBit*)
        ICON=""
        ;;
    *clamtk*)
        ICON=""
        ;;
    *nm-connection-editor*)
        ICON="󰤤"
        ;;
    *avahi-discover*)
        ICON="󰤤"
        ;;
    *corectrl*)
        ICON=""
        ;;
    *soffice*)
        ICON="󰏆"
        ;;
    *libreoffice*)
        ICON=""
        ;;
    *atril*)
        ICON="󱔘"
        ;;
    *lxappearance*)
        ICON="󱕷"
        ;;
    *kvantummanager*)
        ICON="󱕷"
        ;;
    *steam*)
        ICON="󰓓"
        ;;
    *zenity*)
        ICON="󰓓"
        ;;
    *retroarch*)
        ICON="󰺵"
        ;;
    *heroic*)
        ICON="󰡶"
        ;;
    *geany*)
        ICON=""
        ;;
    *Godot*)
        ICON=""
        ;;
    *gpartedbin*)
        ICON="󱊞"
        ;;
    *electron*)
        ICON="󱀤"
        ;;
    *)
        ICON="󰋜"
        ;;
esac

echo $ICON