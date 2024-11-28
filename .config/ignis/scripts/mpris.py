#!/usr/bin/env python3

import sys
import subprocess

PLAYER_ICONS = {"spotify": "󰓇", "firefox": "󰈹", "chrome": "󰊯", None: ""}

def get_player_icon(player: str) -> str:
    if player == "firefox":
        return PLAYER_ICONS["firefox"]
    elif player == "spotify":
        return PLAYER_ICONS["spotify"]
    elif "chromium" in player or "chrome" in player:
        return PLAYER_ICONS["chrome"]
    return PLAYER_ICONS[None]

def detect_player_status() -> str:
    try:
        result = subprocess.run(
            ["playerctl", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        status = result.stdout.strip()
        if status == "Playing":
            artist = subprocess.run(
                ["playerctl", "metadata", "xesam:artist"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            title = subprocess.run(
                ["playerctl", "metadata", "xesam:title"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            icon = get_player_icon(artist)

            return f"{title} - {artist}"
        else:
            return "No music is currently playing."
    except subprocess.CalledProcessError:
        return "No active players found."

def detect_player_icon() -> str:
    try:
        result = subprocess.run(
            ["playerctl", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        players = result.stdout.strip().splitlines()
        if not players:
            return PLAYER_ICONS[None]

        player_name = players[0]
        return get_player_icon(player_name.lower())
    except subprocess.CalledProcessError:
        return PLAYER_ICONS[None]

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"status", "icon"}:
        sys.exit(1)

    if sys.argv[1] == "status":
        player_info = detect_player_status()
        print(player_info)
    elif sys.argv[1] == "icon":
        player_icon = detect_player_icon()
        print(player_icon)
