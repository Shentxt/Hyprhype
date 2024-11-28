from ignis.widgets import Widget
from ignis.app import IgnisApp
from .buttons.volume import volume_control
from .buttons.quick_settings import quick_settings
from .buttons.user import user
from .buttons.brightness import brightness_slider
from scripts.manager_box import update_state, get_state

app = IgnisApp.get_default()

def user_buttons() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center-widget"],
        child=[
            user(),
        ],
    )

def slider() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            volume_control(),
            brightness_slider(),
        ],
    )

def control_center_widget() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            user_buttons(),
            Widget.Box(
                vertical=True,
                css_classes=["control-center"],
                child=[
                    quick_settings(),
                ],
            ),
            slider(),
        ],
    )



def control_center() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_left",
        child=control_center_widget(),
        transition_duration=300,
        reveal_child=True,
    )
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_CONTROL_CENTER"),
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
        anchor=["top", "right", "left"],
        namespace="ignis_CONTROL_CENTER",
        child=box,
        revealer=revealer,
    )
