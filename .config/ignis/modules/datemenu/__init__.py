from ignis.widgets import Widget
from ignis.app import IgnisApp
from .notification_center import notification_center

app = IgnisApp.get_default()

def date_center() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["date-center"],
        child=[
            Widget.Box(
                vertical=True,
                css_classes=["date-widget"],
                child=[
                ],
            ),
            notification_center(),
        ],
    )

def date_window() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_down",
        child=date_center(),
        transition_duration=300,
        reveal_child=True,
    )
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_DATE"),
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
        anchor=["top", "right", "bottom", "left"],
        namespace="ignis_DATE",
        child=box,
        revealer=revealer,
    )
