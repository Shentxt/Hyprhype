import subprocess

def set_border_colors():
    active_border = "rgb(FE2EC8) rgb(8000FF) rgb(00FFFF) 270deg"
    inactive_border = "rgb(2E2E2E) rgb(F2F2F2) rgb(585858) 270deg"

    commands = [
        f"hyprctl keyword general:col.active_border '{active_border}'",
        f"hyprctl keyword general:col.inactive_border '{inactive_border}'",
    ]
    
    for command in commands:
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error sending command: {e.stderr.decode('utf-8')}")

    print(f"Border colors changed: \n"
          f"Active: {active_border}\n"
          f"Inactive: {inactive_border}")

set_border_colors()
