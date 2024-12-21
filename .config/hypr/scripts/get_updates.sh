#!/usr/bin/env bash

# -----------------------------------------------------------------------------------
#
# ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
# ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
# ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
#  ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

get_total_updates() {
    local total_updates=$(($(checkupdates 2> /dev/null | wc -l || echo 0) + $(paru -Qua 2> /dev/null | wc -l || echo 0)))
    echo "${total_updates:-0}"
}

get_list_updates() {
    echo -e "\033[1m\033[34mRegular updates:\033[0m"
    checkupdates | sed 's/->/\x1b[32;1m\x1b[0m/g'
}

get_list_aur_updates() {
    echo -e "\n\033[1m\033[34mAur updates available:\033[0m"
    paru -Qua | sed 's/->/\x1b[32;1m\x1b[0m/g'
}

print_updates() {
    while true; do
        notify-send "Akihiko" "reading you can improve your <span color='yellow'>academy</span>." -i ~/.config/hypr/assets/icons/persona/akihiko.png
        echo "1. Search file"
        echo "2. Search pack"
        echo "3. Exit"
        read -p "Please enter your choice (1, 2 or 3): " choice

        case "$choice" in
            1) file ;;
            2) pack ;;
            3) pkill -f "kitty --title Float";;
            *) echo "Invalid option." ;;
        esac
    done
}

file() {
    sudo -v
    selected_file=$(sudo find / -type f ! -path "/root/*" ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" ! -path "/tmp/*" ! -path "/mnt/*" ! -path "/media/*" | fzf --preview 'cat {}')
    if [[ ! -z "$selected_file" ]]; then
      alacritty -e nvim "$selected_file"
    fi
}

pack() {
    while true; do
        selected=$(yay -Qe | awk '{print $1 " - " $2}' | fzf --multi --preview 'yay -Si {1}')
        
        if [[ ! -z "$selected" ]]; then
            package=$(echo "$selected" | awk '{print $1}')
            echo "Removing $package..."
            yay -Rns "$package"
            echo "Removal completed. You can continue to select packages."
        else
            echo -e "\033[1m\033[32mNo more packages to remove!\033[0m"
            break
        fi
    done
}

update_system() {
 while true; do
        notify-send "Akihiko" "Updating and install your equipment improves <span color='yellow'>performance</span>." -i ~/.config/hypr/assets/icons/persona/akihiko.png
        echo "1. Update"
        echo "2. Exit"
        read -p "Please enter your choice (1 or 2): " choice

        case "$choice" in
            1) update ;;
            2) pkill -f "kitty --title Float";;
            *) echo "Invalid option." ;;
        esac
    done
}

update() {
    echo2() { echo "$@" >&2; }
    printf2() { printf "$@" >&2; }
    DIE() { echo2 "Error: $1"; exit 1; }

    SetHelper() {
        for helper in "$@" yay paru pacman; do
            which "${helper%% *}" &>/dev/null && return 0
        done
        echo2 "Warning: AUR helper not found. Defaulting to pacman."
        helper=pacman
    }

    Cmd() {
        echo2 "==> $@"
        "$@" || DIE "'$*' failed."
    }

    ResetKeyrings() {
        Cmd sudo mv /etc/pacman.d/gnupg /root/pacman-key.bak.$(date +%Y%m%d-%H%M)
        Cmd sudo pacman-key --init
        Cmd sudo pacman-key --populate archlinux
        Cmd sudo pacman -Syy --noconfirm archlinux-keyring
        Cmd sudo pacman -Syu
        echo2 "Keyrings reset."
        exit 0
    }

    ClearDatabases() {
        Cmd sudo rm /var/lib/pacman/sync/*
        echo2 "Package databases cleared."
        exit 0
    }

    HandleConflicts() {
        echo2 "Attempting to resolve package conflicts..."
        conflict_pkg=$(pacman -Qoq /usr/lib/libhyprgraphics.so 2>/dev/null)
        if [ -n "$conflict_pkg" ]; then
            echo2 "Removing conflicting package: $conflict_pkg"
            Cmd sudo pacman -Rdd --noconfirm "$conflict_pkg"
        else
            echo2 "No specific conflicting package identified."
        fi
    }

    DiskSpace() {
        local available=$(findmnt / -nbo avail)
        local min=$((1000 * 1000 * 1000))

        if [ $available -lt $min ]; then
            echo2 "Warning: Low disk space on root partition. Only $available bytes available."
            echo2 "Consider cleaning package cache with 'sudo paccache -rk1'."
        fi
    }

    Main() {
        local lock=/var/lib/pacman/db.lck
        local rmopt=f

        echo2 "Starting package update..."

        DiskSpace

        if [ -e $lock ] && fuser $lock &>/dev/null; then
            rmopt=i
        fi

        SetHelper "$1"

        if [ "$helper" = "pacman" ]; then
            echo2 "Updating native packages..."
            sudo bash -c "rm -$rmopt $lock; [ ! -e $lock ] && pacman -Syyu --noconfirm" || HandleConflicts
        else
            echo2 "Updating native and AUR packages..."
            sudo bash -c "rm -$rmopt $lock; [ ! -e $lock ] && pacman -Syyu --noconfirm && $helper -Sua --noconfirm" || HandleConflicts
        fi
    }

    case "$1" in
        --keyrings-reset)
            ResetKeyrings
            ;;
        --clear-databases)
            ClearDatabases
            ;;
        *)
            Main "$1"
            ;;
    esac
}

case "$1" in
    --get-updates)get_total_updates ;;
    --print-updates)print_updates ;;
    --update-system)update_system ;;
    --help|*)echo -e "Updates [options]

Options:
	--get-updates		Get the number of updates available.
	--print-updates		Print the number of available package to update.
	--update-system		Update your system including the AUR packages.\n"
esac
