#!/bin/bash

toggle(){
  STATUS="$(bluetoothctl show | grep Powered | awk '{print $2}')"
  if [ "$STATUS" == "yes" ]; then
  bluetoothctl power off
  echo '{"status": "off"}'
  notify-send "Futaba" " The <span color='yellow'>Bluetooth is Disconnected</span>" -i ~/.config/hypr/assets/icons/persona/futaba.png
  else
  bluetoothctl power on
  echo '{"status": "on"}'
  notify-send "Futaba" " The <span color='yellow'>Bluetooth is Connected</span>" -i ~/.config/hypr/assets/icons/persona/futaba.png
  fi
}

icon() {
        # not connected
        if [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -eq 0 ]; then
                echo "󰂲"
        else
                # on
                if [ $(echo info | bluetoothctl | grep 'Device' | wc -c) -eq 0 ]; then
                        echo "󰂲"
                else
                        echo ""
                fi
        fi
}

status() {
    # not connected
    if [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -eq 0 ]; then
        echo "Disconnected"
    else
        # on
        if [ $(echo info | bluetoothctl | grep 'Device' | wc -c) -eq 0 ]; then
            echo "Disconnected"
        else
            # get device alias
            DEVICE=$(echo info | bluetoothctl | grep 'Alias:' | awk -F:  '{ print $2 }')
            # Get the device path dynamically
            DEVICE_PATH=$(upower -e | grep -E 'headset|headphones')
            # Get the battery level
            BATTERY=$(upower -i $DEVICE_PATH | grep percentage | cut -b 26-28)
            if [ -z "$DEVICE" ] || [ -z "$BATTERY" ]; then
                echo "Connected"
            else
                echo "$DEVICE - $BATTERY"
            fi
        fi
    fi
}


if [[ $1 == "--status" ]]; then
        status
elif [[ $1 == "--icon" ]]; then
        icon
elif [[ $1 == "--toggle" ]]; then
        toggle
fi
