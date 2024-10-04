import { SimpleToggleButton } from "../ToggleButton"
import icons from "lib/icons"
import apps from "lib/apps"
import { sh } from "lib/utils"
import options from "options"

export const UpdateWidget = () => {
    const handleClick = () => {
      sh(apps.execs.update.value);
   }; 
 
    return SimpleToggleButton({
        icon: icons.arch.update, 
        label: "Update",   
        toggle: handleClick, 
        connection: [null, () => false] 
    });
}
