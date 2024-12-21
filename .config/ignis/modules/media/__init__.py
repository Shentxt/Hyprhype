from ignis.widgets import Widget
from ignis.app import IgnisApp
from .media import media
from scripts.mpris  import get_player_info, get_player_icon_script 
import threading
import time

app = IgnisApp.get_default()

def media_center() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["media-center"],
        child=[
            Widget.Box(
                visible=lambda: get_player_info() != "",
                vertical=True,
                css_classes=["media-widget"],
                child=[
                  media(),
                ],
            ),
        ],
    )

def media_window() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_down",
        child=media_center(),
        transition_duration=300,
        reveal_child=True,
    )
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_MEDIA"),
            ),
            revealer,
        ],
    )
    return Widget.RevealerWindow(
        visible=False,
        popup=True,
        kb_mode="on_demand",
        layer="top",
        css_classes=["unset"],
        anchor=["top"],
        namespace="ignis_MEDIA",
        child=box,
        revealer=revealer,
    )

def update_music_info(): 
    while True: 
        player_info = get_player_info() 
        media_widget.visible = player_info != "" 
        time.sleep(1) 

threading.Thread(target=update_music_info, daemon=True).start()
