#!/bin/bash

gamemode_file="/tmp/gamemode.txt"
error_file="/tmp/gamemode_error.txt"

mod_enable () {
    > "$error_file"
    
    {
if ! pgrep -x "pkexec" > /dev/null; then
        pkexec bash -c '
        sync; echo 3 | tee /proc/sys/vm/drop_caches
        sysctl -w vm.vfs_cache_pressure=200
        systemctl stop systemd-journald
        systemctl stop waydroid-container
        '
        
        if [ $? -ne 0 ]; then
            echo "pkexec cancel o failed." >> "$error_file"
            return  
        fi
    fi

    hyprpm disable hyprbars 
    hyprpm disable borders-plus-plus  
    
    hyprctl keyword animations:enabled false
    hyprctl keyword decoration:blur:enabled false
    hyprctl keyword decoration:active_opacity 1.0
    hyprctl keyword decoration:inactive_opacity 1.0
    hyprctl keyword decoration:rounding 0
    hyprctl keyword decoration:blur:noise 0
    hyprctl keyword general:col.active_border 0
    hyprctl keyword general:col.inactive_border 0
    hyprctl keyword general:gaps_in 0
    hyprctl keyword general:gaps_out 0
    hyprctl keyword general:border_size 0
    
    pkill -f swww

for script in \
    ~/.config/hypr/scripts/song.sh \
    ~/.config/hypr/scripts/processingpng.js; do
    pgrep -f "$script" > /dev/null && pkill -f "$script"
done

    } 2> "$error_file"

    echo "true" > "$gamemode_file"
    if [ -s "$error_file" ]; then
        notify-send "Error in Gamemode Enable" "$(cat $error_file)" -i ~/.config/hypr/assets/icons/persona/jumpei.png
  fi
}

mod_disable () {
     > "$error_file"
    
    {
if ! pgrep -x "pkexec" > /dev/null; then
        pkexec bash -c '
        sysctl -w vm.vfs_cache_pressure=100
        systemctl start systemd-journald
        systemctl start waydroid-container
        '
        
        if [ $? -ne 0 ]; then
            echo "pkexec fue cancel o failed." >> "$error_file"
            return  
        fi
    fi

    hyprpm enable hyprbars 
    hyprpm enable borders-plus-plus

    hyprctl keyword animations:enabled true
    hyprctl keyword decoration:blur:enabled true
    hyprctl keyword decoration:active_opacity 0.6
    hyprctl keyword decoration:inactive_opacity 0.5
    hyprctl keyword decoration:rounding 12
    hyprctl keyword decoration:blur:size 3
    hyprctl keyword decoration:blur:noise 0.2
    hyprctl keyword general:gaps_in 5
    hyprctl keyword general:gaps_out 20
    hyprctl keyword general:border_size 2 

    ags -q; ags 
    swww-daemon --format xrgb &
    ~/.config/hypr/scripts/song.sh &
    setsid node ~/.config/hypr/scripts/processingpng.js > ~/.cache/output.log 2>&1 &
    } 2> "$error_file"

    echo "false" > "$gamemode_file"
    if [ -s "$error_file" ]; then
        notify-send "Error in Gamemode disable" "$(cat $error_file)" -i ~/.config/hypr/assets/icons/persona/jumpei.png
  fi
}

if [ -f "$gamemode_file" ]; then
    gamemode=$(cat "$gamemode_file")
else
    gamemode="false"
fi

if [ "$gamemode" = "true" ]; then
    mod_disable
else
    mod_enable
fi
