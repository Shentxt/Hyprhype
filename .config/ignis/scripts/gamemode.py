import subprocess
import os
import sys

gamemode_file = "/tmp/gamemode.txt"
error_file = "/tmp/gamemode_error.txt"

def mod_enable():
    try:
        with open(error_file, 'w') as err_file:
            subprocess.run([
                'pkexec', 'bash', '-c', 'sync; echo 3 | tee /proc/sys/vm/drop_caches; sysctl -w vm.vfs_cache_pressure=200; systemctl stop systemd-journald; systemctl stop waydroid-container'
            ], check=True, stderr=err_file)

            subprocess.run(["hyprpm", "disable", "hyprbars"], check=True, stderr=err_file)
            subprocess.run(["hyprpm", "disable", "borders-plus-plus"], check=True, stderr=err_file)
            
            subprocess.run(["hyprctl", "keyword", "animations:enabled", "false"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:blur:enabled", "false"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:blur:noise", "false"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:active_opacity", "1.0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:inactive_opacity", "1.0"], check=True, stderr=err_file) 
            subprocess.run(["hyprctl", "keyword", "decoration:rounding", "0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:col.active_border", "0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:col.inactive_border", "0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:gaps_in", "0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:gaps_out", "0"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:border_size", "0"], check=True, stderr=err_file)

            os.system("ignis close ignis_DESKTOP_0")

            with open(gamemode_file, 'w') as f:
                f.write("true")

            print("Gamemode enabled")
            
    except subprocess.CalledProcessError as e:
        with open(error_file, 'a') as err_file:
            err_file.write(f"Error: {str(e)}")
        print("Error enabling gamemode")

def mod_disable():
    try:
        with open(error_file, 'w') as err_file:
            subprocess.run([
                'pkexec', 'bash', '-c', 'sysctl -w vm.vfs_cache_pressure=100; systemctl start systemd-journald; systemctl start waydroid-container'
            ], check=True, stderr=err_file)
 
            subprocess.run(["hyprpm", "enable", "hyprbars"], check=True, stderr=err_file)
            subprocess.run(["hyprpm", "enable", "borders-plus-plus"], check=True, stderr=err_file)
          
               
            subprocess.run(["hyprctl", "keyword", "animations:enabled", "true"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:blur:enabled", "true"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:blur:noise", "true"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:active_opacity", "0.6"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "decoration:inactive_opacity", "0.5"], check=True, stderr=err_file) 
            subprocess.run(["hyprctl", "keyword", "decoration:rounding", "12"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:col.active_border", "3"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:col.inactive_border", "3"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:gaps_in", "5"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:gaps_out", "20"], check=True, stderr=err_file)
            subprocess.run(["hyprctl", "keyword", "general:border_size", "2"], check=True, stderr=err_file)
        
            os.system("ignis open ignis_DESKTOP_0")

            with open(gamemode_file, 'w') as f:
                f.write("false")

            print("Gamemode disabled")
            
    except subprocess.CalledProcessError as e:
        with open(error_file, 'a') as err_file:
            err_file.write(f"Error: {str(e)}")
        print("Error disabling gamemode")

def main():
    if os.path.exists(gamemode_file):
        with open(gamemode_file, 'r') as f:
            gamemode = f.read().strip()
    else:
        gamemode = "false"

    if gamemode == "true":
        mod_disable()
    else:
        mod_enable()

if __name__ == "__main__":
    main()
