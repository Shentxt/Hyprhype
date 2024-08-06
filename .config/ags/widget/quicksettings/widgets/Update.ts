import { SimpleToggleButton } from "../ToggleButton"
import icons from "lib/icons"
import { sh } from "lib/utils"
import options from "options"

export const UpdateWidget = () => {
    const handleClick = () => { 
        sh("bash -c 'kitty --title 'Float' -e ~/.config/hypr/scripts/get_updates.sh --update-system &'");
    };

    return SimpleToggleButton({
        icon: icons.arch.normal, 
        label: "Update",   
        toggle: handleClick, 
        connection: [null, () => false] 
    });
}
