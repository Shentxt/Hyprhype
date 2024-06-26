#!/bin/bash

toggle(){
  STATUS="$(bluetoothctl show | grep Powered | awk '{print $2}')"
  if [ $STATUS == "yes" ]; then
    bluetoothctl power off
    echo '{"status": "off"}'
    notify-send 'Mitsuru' 'The <span color=yellow>Bluetooth is disconnected</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png
  else
    bluetoothctl power on
    echo '{"status": "on"}'
    notify-send 'Mitsuru' 'The <span color=yellow>Bluetooth is connected</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png 
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
        echo "Desconectado"
    else
        # on
        if [ $(echo info | bluetoothctl | grep 'Device' | wc -c) -eq 0 ]; then
            echo "Desconectado"
        else
            # get device alias
            DEVICE=$(echo info | bluetoothctl | grep 'Alias:' | awk -F:  '{ print $2 }')
            # Get the device path dynamically
            # DEVICE_PATH=$(upower -e | grep 'headset')
            DEVICE_PATH=$(upower -e | grep -E 'headset|headphones')
            # Get the battery level
            BATTERY=$(upower -i $DEVICE_PATH | grep percentage | cut -b 26-28)
            echo "$DEVICE - $BATTERY"
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
