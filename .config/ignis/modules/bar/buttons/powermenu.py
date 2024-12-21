from ignis.widgets import Widget
from ignis.app import IgnisApp

app = IgnisApp.get_default()

def power_button() -> Widget.Button:
    return Widget.Button(
        child=Widget.Icon(image="system-shutdown-symbolic", pixel_size=20),
        halign="end",
        css_classes=["launch", "unset"],
        on_click=lambda x: app.toggle_window("ignis_POWERMENU"),
    )

