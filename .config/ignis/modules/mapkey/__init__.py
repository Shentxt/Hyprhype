from ignis.widgets import Widget
from ignis.app import IgnisApp
from .mapkey import get_keybindings 

app = IgnisApp.get_default()

def map_center() -> Widget.Box:
    return Widget.Box(
        vertical=False, 
        css_classes=["keybindings"],
        child=[
        get_keybindings(),
        ], 
    )

def map_window() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_right",
        child=map_center(),
        transition_duration=300,
        reveal_child=True,
    )
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_MAP"),
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
        anchor=["center"],
        namespace="ignis_MAP",
        child=box,
        revealer=revealer,
    )
