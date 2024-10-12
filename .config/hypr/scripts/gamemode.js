const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const gamemodeFile = "/tmp/gamemode.txt";

function modDisable() {
    try {
        execSync('hyprctl keyword animations:enabled false');
        execSync('hyprctl keyword decoration:blur:enabled false');
        execSync('hyprctl keyword decoration:active_opacity 1.0');
        execSync('hyprctl keyword decoration:inactive_opacity 1.0');
        execSync('hyprctl keyword decoration:rounding 0');
        execSync('hyprctl keyword decoration:blur:noise 0');
        execSync('hyprctl keyword general:col.active_border 0');
        execSync('hyprctl keyword general:col.inactive_border 0');
        execSync('hyprctl keyword general:gaps_in 0');
        execSync('hyprctl keyword general:gaps_out 0');
        execSync('hyprctl keyword general:border_size 0');
        execSync('pkill swww');
        execSync('pkill wlsunset');
        execSync('pkill -f ~/.config/hypr/scripts/song.sh');
        execSync('pkill -f ~/.config/hypr/scripts/brightnes.sh');
    } catch (error) {
        console.error(`Error disabling game mode: ${error.message}`);
    }
}

function modEnable() {
    try {
        execSync('hyprctl keyword animations:enabled true');
        execSync('hyprctl keyword decoration:blur:enabled true');
        execSync('hyprctl keyword decoration:active_opacity 0.6');
        execSync('hyprctl keyword decoration:inactive_opacity 0.5');
        execSync('hyprctl keyword decoration:rounding 12');
        execSync('hyprctl keyword decoration:blur:size 3');
        execSync('hyprctl keyword decoration:blur:noise 0.2');
        execSync('hyprctl keyword general:gaps_in 5');
        execSync('hyprctl keyword general:gaps_out 20');
        execSync('hyprctl keyword general:border_size 2');
        execSync('swww-daemon --format xrgb');
        execSync('~/.config/hypr/scripts/song.sh &');
        execSync('~/.config/hypr/scripts/brightnes.sh &');
    } catch (error) {
        console.error(`Error enabling game mode: ${error.message}`);
    }
}

function toggleGameMode() {
    let gamemode = "false";
    try {
        gamemode = execSync(`cat ${gamemodeFile}`).toString().trim();
    } catch (error) {
  }

    if (gamemode === "true") {
        modDisable();
        execSync(`echo "false" > ${gamemodeFile}`);
    } else {
        modEnable();
        execSync(`echo "true" > ${gamemodeFile}`);
    }
}

toggleGameMode();
