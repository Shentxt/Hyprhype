#!/bin/bash

update_icons() {
    box1_status=$(eww get box1)
    box2_status=$(eww get box2)

    icon1=""
    icon2=""
    
    if [ "$box1_status" = "true" ]; then
        icon1=""
    elif [ "$box2_status" = "true" ]; then
        icon2=""
    fi

    echo "$icon1" "$icon2"
}

box1(){
    eww update box1=true
    eww update box2=false
    update_icons
}

box2(){
    eww update box1=false
    eww update box2=true
    update_icons
}

if [ $# -ne 1 ]; then
    echo "Use: $0 <function_name>"
    exit 1
fi

case "$1" in
    box1)
        box1
        ;;
    box2)
        box2
        ;;
    icons)
        update_icons
        ;;
    *)
        echo "Function '$1' unknown."
        exit 1
        ;;
esac
