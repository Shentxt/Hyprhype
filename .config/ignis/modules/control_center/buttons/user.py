import os
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.app import IgnisApp
from ignis.services.fetch import FetchService
from ...settings import settings_window
from options import avatar_opt

fetch = FetchService.get_default()
app = IgnisApp.get_default()


def format_uptime(value):
    days, hours, minutes, seconds = value
    if days:
        return f"up {days:02}:{hours:02}:{minutes:02}"
    else:
        return f"up {hours:02}:{minutes:02}"


def user_image() -> Widget.Picture:
    return Widget.Picture(
        image=avatar_opt.bind(
            "value",
            lambda value: "user-info" if not os.path.exists(value) else value,
        ),
        width=54,
        height=54,
        content_fit="cover",
        style="border-radius: 0.50rem;",
    )


def username() -> Widget.Box:
    return Widget.Box(
        child=[
            Widget.Label(
                label=os.getenv("USER"), css_classes=["user-name"], halign="start"
            ),
            Widget.Label(
                label=Utils.Poll(
                    timeout=60 * 1000, callback=lambda x: fetch.uptime
                ).bind("output", lambda value: format_uptime(value)),
                halign="start",
                css_classes=["user-name-secondary"],
            ),
        ],
        vertical=True,
        css_classes=["user-name-box"],
    )


def settings_button() -> Widget.Button:
    return Widget.Button(
        child=Widget.Icon(image="emblem-system-symbolic", pixel_size=20),
        halign="end",
        hexpand=True,
        css_classes=["user-settings", "unset"],
        on_click=lambda x: settings_window(),
    )

def user() -> Widget.Box:
    return Widget.Box(
        child=[user_image(), username(), settings_button()],
        css_classes=["user"],
    )
