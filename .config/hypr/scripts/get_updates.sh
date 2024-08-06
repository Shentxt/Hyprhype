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
        echo "2. Install"
        echo "3. Exit"
        read -p "Please enter your choice (1, 2 or 3): " choice

        case "$choice" in
            1) update ;;
            2) install ;;
            3) pkill -f "kitty --title Float";;
            *) echo "Invalid option." ;;
        esac
    done
}

update() {
echo2()   { echo "$@" >&2 ; }
printf2() { printf "$@" >&2 ; }
WARN()    { echo2 "==> $progname: warning: $1"; }
DIE()     { echo2 "==> $progname: error: $1"; exit 1;  }

SetHelper() {
    for helper in "$@" "$EOS_AUR_HELPER" "$EOS_AUR_HELPER_OTHER" yay paru pacman ; do
        which "${helper%% *}" &>/dev/null && return 0
    done
    WARN "AUR helper not found"
    helper=pacman
}

Cmd() {                           # Show a command, run it, and exit on issues.
    echo2 "==>" "$@"
    "$@" || DIE "'$*' failed."
}

ResetKeyrings() {
    Cmd sudo mv /etc/pacman.d/gnupg /root/pacman-key.bak.$(date +%Y%m%d-%H%M).by.$progname
    Cmd sudo pacman-key --init
    Cmd sudo pacman-key --populate archlinux endeavouros
    Cmd sudo pacman -Syy --noconfirm archlinux-keyring endeavouros-keyring
    Cmd sudo pacman -Syu
    echo2 "Keyrings reset."
    exit 0
}

ClearDatabases() {
    Cmd sudo rm /var/lib/pacman/sync/*
    echo2 "Package databases cleared."
    exit 0
}


Options() {
    local opts
    local lopts="aur,clear-databases,dump-options,keyrings-reset,nvidia,no-keyring,no-sync,helper:,min-free-bytes:,paru,yay,pacman,help"
    local sopts="h"

    opts="$(/usr/bin/getopt -o=$sopts --longoptions $lopts --name "$progname" -- "$@")" || {
        Options -h
        return 1
    }
    eval set -- "$opts"

    while true ; do
        case "$1" in
            --nvidia)
                IsEndeavourOS && nvidia=yes || WARN "sorry, option $1 works only in EndeavourOS. Option ignored."
                ;;
            --no-keyring)                        keyring=no ;;
            --no-sync)                           sync=":" ;;
            --keyrings-reset)                    ResetKeyrings ;;
            --clear-databases)                   ClearDatabases ;;
            --min-free-bytes)                    min_free_bytes="$2" ; shift ;;
            --helper)                            SetHelper "$2" ; shift ;;
            --aur)                               SetHelper ;;
            --paru | --yay | --pacman)           SetHelper "${1/--/}" ;;
            --dump-options)
                lopts="${lopts//:/}"
                lopts="--${lopts//,/ --}"
                sopts="${sopts//:/}"
                sopts="$(echo "$sopts" | sed -E 's|([a-z])| -\1|g')"
                echo $lopts $sopts
                exit 0
                ;;

            -h | --help)
                cat <<EOF >&2
Package updater for EndeavourOS and Arch
Handles/updates:
- keyrings
- pacman db lock
- disk space check
- sync after update (unless disabled by --no-sync)
and optionally
- AUR with given AUR helper
- Nvidia driver vs. kernel updates (only on EndeavourOS)

Usage: $progname [options]
Options:
  --help, -h         This help.
  --nvidia           Check also nvidia driver vs. kernel updates.
  --clear-databases  Clears package database files.
                     Use this only if package database issues constantly make system update fail.
  --keyrings-reset   Resets Arch and EndeavourOS keyrings.
                     Use this only if keyring issues constantly make system update fail.
  --no-keyring       Do not try to update keyrings first.
  --no-sync          Do not run 'sync' after update.
  --helper           AUR helper name. Supported: yay, paru, pacman.
                     Default: pacman
                     Other AUR helpers supporting option -Sua like yay should work as well.
  --paru             Same as --helper=paru.
  --yay              Same as --helper=yay.
  --aur              Uses the AUR helper configured in /etc/eos-script-lib-yad.conf.
  --pacman           Same as --helper=pacman. Default. (Note: pacman does not support AUR directly).
  --min-free-bytes   Minimal amount of free space (in bytes) that the root partition should have
                     before updating. Otherwise a warning message will be displayed.
                     Default: $min_free_bytes
  --dump-options     Shows all supported options. Used for bash command completion.
EOF
                exit 0
                ;;
            
            --) shift ; break ;;
        esac
        shift
    done
}

IsEndeavourOS() {
    if [ "$isEndeavourOS" = "yes" ] || [ -r /usr/lib/endeavouros-release ] || [ -n "$(grep -iw endeavouros /etc/*-release)" ] ; then
        isEndeavourOS=yes
        return 0
    fi
    isEndeavourOS=no
    return 1
}

DiskSpace() {
    local available=$(findmnt / -nbo avail)
    local min=$min_free_bytes

    if [ $available -lt $min ] ; then
        {
            WARN "your root partition (/) has only $available bytes of free space."
            if [ $(du -b -d0 /var/cache/pacman/pkg | awk '{print $1}') -gt $min ] ; then
                printf "\nFor example, cleaning up the package cache may help.\n"
                printf "Command 'sudo paccache -rk1' would do this:"
                paccache -dk1
                printf "Command 'sudo paccache -ruk0' would do this:"
                paccache -duk0
                echo ""
            fi
        } >&2
    fi
}

echo2blue()  { echo2 "${BLUE}$1${RESET}" ; }
echo2green() { echo2 "${GREEN}$1${RESET}" ; }

Main() {
    local progname="${0##*/}"
    source /usr/share/endeavouros/scripts/eos-script-lib-yad || return 1
    local helper="pacman"
    local min_free_bytes=$((1000 * 1000 * 1000))  # default: 1 GB

    local helper2=":"
    local lock=/var/lib/pacman/db.lck
    local rmopt=f
    local isEndeavourOS=""

    local subopts=()
    local afteropts=()
    local keyring=yes                             # user may disable keyring check with --no-keyring
    local nvidia=no                               # user may enable Nvidia check with --nvidia
    local sync="sync"

    local -r RED=$'\e[0;91m'
    local -r GREEN=$'\e[0;92m'
    local -r BLUE=$'\e[0;94m'
    local -r MAGENTA=$'\e[0;95m'
    local -r RESET=$'\e[0m'

    Options "$@"

    [ $nvidia  = yes ] && subopts+=(--nvidia)
    [ $keyring = yes ] && subopts+=(--keyrings)

    echo2blue "$progname: package updater with additional features"

    DiskSpace

    if [ -e $lock ] && fuser $lock &>/dev/null ; then
        rmopt=i
    fi
    if [ "$helper" = "pacman" ] ; then
        echo2green "Updating native apps..."
        sudo bash -c "rm -$rmopt $lock; [ -e $lock ] || { pacman -Sy && eos-update-extras ${subopts[*]} && pacman -Su && $sync ; }"
    else
        echo2green "Updating native and AUR apps..."
        helper2="/usr/bin/sudo -u $LOGNAME $helper -Sua"
        sudo bash -c "rm -$rmopt $lock; [ -e $lock ] || { pacman -Sy && eos-update-extras ${subopts[*]} && pacman -Su && $helper2 ; $sync ; }"
    fi
}

Main "$@"   
}

install() {
while true; do
    echo "Please enter the name of the package you want to search for:"
    read package
    # Use yay to search for the package and then fzf and awk to select it interactively
    selected=$(yay -Ss $package | awk -F' ' '/^aur\// || /^extra\// {print $1 " - " $NF}' | fzf --multi --preview 'yay -Si {1}')
   
    if [[ ! -z "$selected" ]]; then
        package_to_install=$(echo "$selected" | awk '{print $1}')
        echo "Installing $package_to_install..."
        yay -S --noconfirm "$package_to_install"
        echo "Installation completed. You can continue selecting packages."
    else
        echo -e "\033[1m\033[32mThere are no more packages to install!\033[0m"
        break
    fi
  done
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
