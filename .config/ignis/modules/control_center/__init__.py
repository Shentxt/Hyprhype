from ignis.widgets import Widget
from ignis.app import IgnisApp
from .buttons.volume import volume_control
from .quick_settings import quick_settings
from .buttons.user import user
from .buttons.brightness import brightness_slider
from scripts.manager_box import update_state, get_state  

app = IgnisApp.get_default()

main_container = Widget.Box()

def box1() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            quick_settings(),
            Widget.ToggleButton(
                css_classes=["box_button"],
                label="Switch to Box2",
                on_toggled=lambda x, active: (
                    print(f"Button toggled, active: {active}"),
                    redraw_container("box2") if active else None,
                ),
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
                on_toggled=lambda x, active: (
                    print(f"Button toggled, active: {active}"),
                    redraw_container("box1") if active else None,
                ),
            ),
        ],
    )

def toggle_boxes() -> Widget.Box:
    current_state = get_state()
    print(f"Current state: {current_state['box_visible']}")
    if current_state["box_visible"] == "box1":
        return box1()
    else:
        return box2()

def redraw_container(new_box: str):
    print(f"Redrawing main_container with: {new_box}")
    main_container.set_child(toggle_boxes())  

def control_center_widget() -> Widget.Box:
    global main_container
    main_container = Widget.Box(
        vertical=True,
        child=[
            toggle_boxes(),
        ],
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
