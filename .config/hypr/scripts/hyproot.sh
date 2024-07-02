#!/bin/bash

APPS=("bleachbit" "thunar")

APP=$(printf '%s\n' "${APPS[@]}" | rofi -dmenu -theme ~/.config/rofi/themes/default.rasi -p "Select an application to run as root:")

[ -z "$APP" ] && exit 1

run_with_pkexec() {
    pkexec "$APP" 2>/tmp/pkexec_error.log
    return $?
}

run_with_xwayland() {
     Xwayland :1 &
     XWAYLAND_PID=$!
     DISPLAY=:1 "$APP" &
     APP_PID=$!
     wait $APP_PID
     kill $XWAYLAND_PID
}

run_with_pkexec
PKEXEC_EXIT_CODE=$?

if grep -q "No such file or directory: 'xhost'" /tmp/pkexec_error.log; then
    run_with_xwayland
else
    exit $PKEXEC_EXIT_CODE
fi
