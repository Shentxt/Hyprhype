from ignis.widgets import Widget
import subprocess

def get_keybindings() -> Widget.Box:
    command = """
        awk '
        BEGIN {
            FS = "[ ]*=[ ]*";  
            max_columns = 2;  
            column_count = 0;
        }

        /^bind/ || /^bindm/ {
            keybinding = $2;
            action = $3;
            
            gsub(/SUPER,/, "SUPER+", keybinding);
            gsub(/SHIFT,/, "SHIFT+", keybinding);
            gsub(/0x002d/, "11", keybinding);
            gsub(/0x003d/, "12", keybinding);

            gsub(/,/, " ", keybinding);
            gsub(/,/, " ", action);
            gsub(/_/, "+", keybinding);
            gsub(/_/, "+", action);

            printf  "%6s %6s", keybinding, action;
            column_count++;

            if (column_count == max_columns) {
               print "";
               column_count = 0;
            }
        } 
        ' /home/shen/.config/hypr/rules/keybinds.conf
    """

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    lines = output.split("\n")
    children = []

    for line in lines:
        if line.strip() != "":
            label = Widget.Label(label=line)
            separator = Widget.Separator(css_classes=["separator-mp"])
            children.extend([label, separator])
    
    return Widget.Box(
        vertical=True,
        css_classes=["awk"],
        child=children
    )
