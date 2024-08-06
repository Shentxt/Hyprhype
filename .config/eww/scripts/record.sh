#!/bin/bash

notify-send "Akechi" "Recording <span color='yellow'>Started</span>." -i ~/.config/hypr/assets/icons/persona/akechi.png

file="$(xdg-user-dir VIDEOS)/$(date '+%F_%T_%:::z.mp4')"

function notify_end_recording {
    notify-send "Akechi" "Recording <span color='yellow'>Finished</span>." -i ~/.config/hypr/assets/icons/persona/akechi.png
}

case $1 in
    no_audio)
        wf-recorder -f $file --codec libx264 --pixel-format yuv420p --force-yuv --bitrate 1000K yuv420p
        notify_end_recording
        ;;
    audio)
        wf-recorder -f $file --codec libx264 --pixel-format yuv420p --force-yuv --bitrate 1000K --audio
        notify_end_recording
        ;;
    region)
        case $2 in
            no_audio)
                wf-recorder -f $file --codec libx264 --pixel-format yuv420p --force-yuv --bitrate 1000K -g "$(slurp)"
                notify_end_recording
                ;;
            audio)
                wf-recorder -f $file --codec libx264 --pixel-format yuv420p --force-yuv --bitrate 1000K --audio -g "$(slurp)"
                notify_end_recording
                ;;
        esac
        ;;
esac
