from ignis.widgets import Widget
import subprocess


def get_keybindings() -> Widget.Box:
    command = """
        awk '
        BEGIN {
            FS = "[ ]*=[ ]*";
        }

        /^bind/ || /^bindm/ {
            keybinding = $2;
            action = $3;

            gsub(/SUPER,/, "SUPER+", keybinding);
            gsub(/SHIFT,/, "SHIFT+", keybinding);
            gsub(/CTRL,/, "CTRL+", keybinding);
            gsub(/0x002d/, "11", keybinding);
            gsub(/0x003d/, "12", keybinding);

            gsub(/,/, " ", keybinding);
            gsub(/,/, " ", action);
            gsub(/_/, "+", keybinding);
            gsub(/_/, "+", action);

            print keybinding, action;
        } 
        ' /home/shen/.config/hypr/rules/keybinds.conf
    """

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    lines = output.split("\n")
    columns = [[], []]

    for idx, line in enumerate(lines):
        if line.strip() != "":
            parts = line.split()
            if len(parts) >= 2:  
                keybinding = parts[0]
                action = " ".join(parts[1:])  
                label = Widget.Label(label=f"{keybinding} {action}")
                separator = Widget.Separator(css_classes=["separator-mp"])

                column_idx = idx % 2
                columns[column_idx].append(label)
                columns[column_idx].append(separator)

    children = []
    for column in columns:
        children.append(Widget.Box(vertical=True, child=column))

    return Widget.Box(
        vertical=False,
        child=children
    )
