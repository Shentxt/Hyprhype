#!/bin/bash

while true; do
    # Check system updates
    updates=$(checkupdates 2>/dev/null | wc -l)

    # Check AUR updates
    aur_updates=$(yay -Qum 2>/dev/null | wc -l)

    # Add total updates
    total_updates=$((updates + aur_updates))

    # Show notification if updates are available
    if [ "$total_updates" -gt 0 ]; then
        notify-send "Fuuka" "<span color='yellow'>$total_updates</span> updates are available"  -i ~/.config/hypr/assets/icons/persona/fuuka.png
    else
        notify-send "Fuuka" "No <span color='yellow'>updates</span> available" -i ~/.config/hypr/assets/icons/persona/fuuka.png
    fi

    # Wait 6 hours before next check
    sleep 6h
  done
