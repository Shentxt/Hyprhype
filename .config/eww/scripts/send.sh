#!/bin/bash

name=$(whoami)

notify-send "Jumpei" "${name}, look what i <span color='yellow'>send</span> you." -i ~/.config/hypr/assets/icons/persona/jumpei.png

# Function to transfer files or folders
transfer() {
    echo "Enter the path of the file or folder you want to transfer:"
    read path
    path="${path/#\~/$HOME}"
    qrcp send "$path"
}

# Function to receive files or folders
receive() {
    echo "Enter the path where you want to save the received file or folder:"
    read path
    path="${path/#\~/$HOME}"
    qrcp receive --output="$path"
}

# Main menu
while true; do
    echo "1. Transfer a file or folder"
    echo "2. Receive a file or folder"
    echo "3. Exit"
    read -p "Select an option: " option

    case $option in
        1) transfer ;;
        2) receive ;;
        3) pkill kitty --title "Float";; 
        *) echo "Invalid option" ;;
    esac
done
