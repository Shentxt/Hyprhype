from ignis.widgets import Widget
from ignis.app import IgnisApp
from ignis.services.applications import ApplicationsService

app = IgnisApp.get_default()

def launcher_button():
    return Widget.Button(
        child=Widget.Icon(image="start-here-symbolic", pixel_size=32),
        on_click=lambda x: app.toggle_window("ignis_LAUNCHER"),
        css_classes=["pinned-app", "unset"],
    )

def launcher_box():
    return Widget.Box(
        child=[launcher_button()]
    )
