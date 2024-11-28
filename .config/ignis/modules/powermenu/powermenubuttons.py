from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.app import IgnisApp
from typing import Callable

app = IgnisApp.get_default()

class PowermenuButton(Widget.Box):
    def __init__(self, label: str, icon_name: str, on_click: Callable) -> None:
        super().__init__(
            child=[
                Widget.Button(
                    child=Widget.Icon(image=icon_name, pixel_size=36),
                    on_click=on_click,
                    css_classes=["powermenu-button", "unset"],
                ),
                Widget.Label(label=label, css_classes=["powermenu-button-label"]),
            ],
            vertical=True,
            css_classes=["powermenu-button-box"],
        )

def poweroff(*args) -> None:
    Utils.exec_sh_async("poweroff")


def reboot(*args) -> None:
    Utils.exec_sh_async("reboot")


def suspend(*args) -> None:
    app.close_window("ignis_POWERMENU")
    Utils.exec_sh_async("systemctl suspend && hyprlock")


def hypr_exit(*args) -> None:
    Utils.exec_sh_async("hyprctl dispatch exit 0")
