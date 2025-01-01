from ignis.widgets import Widget
from ignis.app import IgnisApp
from .buttons.volume import volume_control
from .quick_settings import quick_settings
from .buttons.user import user
from .buttons.brightness import brightness_slider

app = IgnisApp.get_default()

active_box = "box1"
main_container = Widget.Box()

def switch_box(new_box: str):
    global active_box
    active_box = new_box
    redraw_container()

def redraw_container(): 
    if active_box == "box1":
        main_container.child = [box1()]  
    else:
        main_container.child = [box2()]

    main_container.queue_draw()  


def box1() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            quick_settings(),
            Widget.ToggleButton(
                css_classes=["box_button"],
                label="Switch to Box2",
                on_toggled=lambda x, active: switch_box("box2"),
            ),
        ],
    )

def box2() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            quick_settings(),
            Widget.ToggleButton(
                css_classes=["box_button"],
                label="Switch to Box1",
                on_toggled=lambda x, active: switch_box("box1"),
            ),
        ],
    )

def control_center_widget() -> Widget.Box:
    global main_container
    main_container = Widget.Box(
        vertical=True,
        child=[box1()],  
    )
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            user_buttons(),
            main_container,
            slider(),
        ],
    )

def user_buttons() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center-widget"],
        child=[user()],
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
