import PopupWindow from "widget/PopupWindow";
import { sh } from "lib/utils";
import icons from "lib/icons"

function CommandOutput() {
const commandOutput = Utils.exec(`
awk '
    BEGIN {
        FS = " = "; 
        max_columns = 2;  
        column_count = 0;
    }

    /^bind/ || /^bindm/ {
        gsub(/\$/, "", $0);

        keybinding = $2;
        action = $3;
        gsub(/^bind/, "", keybinding);
        gsub(/SUPER,/, "SUPER+", keybinding);  
        gsub(/SHIFT,/, "SHIFT+", keybinding);

        gsub(/,/, " ", keybinding);  
        gsub(/,/, " ", action);    
    
        gsub(/_/, "+", keybinding);  
        gsub(/_/, "+", action);    

        printf "%-30s %-40s", keybinding, action;
        column_count++; 
 
        if (column_count == max_columns) {
            print "";
            column_count = 0;
        }
    }

    END {
        if (column_count > 0) {
            print "";  
        }
    }
' /home/shen/.config/hypr/rules/keybinds.conf
`);

  return Widget.Box({
    className: 'key',
    vertical: true,
    spacing: 6,
    children: commandOutput.split("\n").map(line => Widget.Label({ label: line })),
  });
}

export default () => PopupWindow({
  name: "Mapkey",
  layout: "center",
  child: Widget.Box({
    className: 'mapkey',
    vertical: false,
    children: [
      Widget.Box({
        vertical: true, 
        children: [
          Widget.Box({
            vertical: false,
            children: [
              Widget.Icon({
                icon: icons.hypr.hypr,  
                css: 'margin-right: 5px;',     
              }),
              Widget.Label({
                label: "Keymap Hyprland",
                className: 'title',
                css: 'font-size: 15px;',
              }),
            ],
          }),
          CommandOutput(),
        ],
      }),
    ],
  }),
});
