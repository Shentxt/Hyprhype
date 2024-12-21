import os
from ignis.widgets import Widget
from ignis.app import IgnisApp
from ignis.services.applications import ApplicationsService
from services.icons import icon_options

app = IgnisApp.get_default()

def launcher_button():
    return Widget.Button(
        child = Widget.Icon(image=icon_options["hypr"].bind("value", lambda value: value if os.path.exists(value) else None),pixel_size=26,css_classes=["img"]),
        on_click=lambda x: app.toggle_window("ignis_LAUNCHER"),
        css_classes=["launch", "unset"],
    )

def launcher_box():
    return Widget.Box(
        child=[launcher_button()]
    )
