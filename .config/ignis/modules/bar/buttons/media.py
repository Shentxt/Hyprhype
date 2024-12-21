from ignis.widgets import Widget
from ignis.app import IgnisApp
from scripts.mpris  import get_player_info, get_player_icon_script 
import threading
import time

app = IgnisApp.get_default()

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
        max_width_chars=20,
        ellipsize="end",
        halign="start",
        css_classes=["font"],
    )

    player_icon_label = Widget.Label(
        label=get_player_icon_script(),
        halign="start",
        valign="start",
        css_classes=["icon", "widgets"],
    )
    
    button = Widget.Button(
        visible=lambda: get_player_info() != "",
        child=Widget.Box(
            child=[
                Widget.Separator(css_classes=["separator"]),
                player_icon_label, 
                player_info_label
            ]
        ),
        css_classes=["unset"],
        on_click=on_click,
    ) 

    def update_music_info():
        while True:
            player_info = get_player_info()
            player_icon = get_player_icon_script()

            player_info_label.label = player_info
            player_icon_label.label = player_icon

            button.visible = player_info != ""

            time.sleep(1)  

    threading.Thread(target=update_music_info, daemon=True).start()

    return button
