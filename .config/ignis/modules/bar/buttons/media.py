from ignis.widgets import Widget
from ignis.app import IgnisApp
import subprocess
import threading
import time

app = IgnisApp.get_default()

def get_player_info():
    try:
        result = subprocess.run(  
            ["/home/shen/.config/ignis/scripts/mpris.py", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_player_icon():
    try:
        result = subprocess.run(  
            ["/home/shen/.config/ignis/scripts/mpris.py", "icon"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""  

def media(monitor):
    window: Widget.Window = app.get_window("ignis_MEDIA")

    def on_click(x):
        if window.monitor == monitor:
            window.visible = not window.visible
        else:
            window.set_monitor(monitor)
            window.visible = True

    player_info_label = Widget.Label(
        label=get_player_info(),
        max_width_chars=10,
        ellipsize="end",
        halign="start",
        css_classes=["font"],
    )

    player_icon_label = Widget.Label(
        label=get_player_icon(),  
        halign="start",
        valign="start",
        css_classes=["icon"],
    )
    
    button = Widget.Button(
        child=Widget.Box(
            child=[player_icon_label, player_info_label]
        ),
        css_classes=["widgets", "unset"],
        on_click=on_click,
    ) 

    def update_music_info():
        previous_info = ""
        while True:
            player_info = get_player_info()
            player_icon = get_player_icon()

            if player_info != previous_info:
                player_info_label.label = player_info
                player_icon_label.label = player_icon
                previous_info = player_info

            time.sleep(1)  

    threading.Thread(target=update_music_info, daemon=True).start()

    return button
