from .notes import notes  
from ignis.widgets import Widget
from ignis.app import IgnisApp

app = IgnisApp.get_default()

def notes_center() -> Widget.Box:
    return Widget.Box(
        vertical=True, 
        css_classes=["keybindings"], 
        child=[
            notes(),  
        ],
    )

def notes_window() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_right",
        child=notes_center(), 
        transition_duration=300,
        reveal_child=True,
    )
    
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_NOTES"),
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
        namespace="ignis_NOTES", 
        child=box,
        revealer=revealer,  
    )
