from ignis.widgets import Widget
from ignis.services.notifications import Notification, NotificationService
from ignis.utils import Utils
from gi.repository import GLib  # type: ignore

notifications = NotificationService.get_default()

def notificount() -> Widget.Box:
    return Widget.Box(
        visible=notifications.bind("notifications", lambda value: len(value) > 0),
        child=[
            Widget.Label(
                label=notifications.bind(
                    "notifications", lambda value: str(len(value))
                ),
                css_classes=["notification-count"],
            ),
            Widget.Icon(
                icon_name="notification-symbolic",  
                pixel_size=24,
            ),
            Widget.Separator(css_classes=["separator"]),
        ]
    )
