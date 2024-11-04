import { SimpleToggleButton } from "../ToggleButton";
import icons from "lib/icons";
import apps from "lib/apps";
import { sh } from "lib/utils";
import options from "options";
import { readFileSync } from 'fs';

const isGameModeActive = () => {
    try {
        const content = readFileSync('/tmp/gamemode.txt', 'utf-8').trim();
        return content === 'true'; 
    } catch (error) {
        console.error("/tmp/gamemode.txt:", error);
        return false; 
    }
};

export const GameWidgets = () => {
    const handleClick = () => {
        sh(apps.execs.game.value); 
    };

    return SimpleToggleButton({
        icon: icons.arch.game, 
        label: "Gamemode",
        toggle: handleClick,
        connection: [null, isGameModeActive] 
    });
};
