from ignis.widgets import Widget
from ignis.services.network import NetworkService
from ignis.services.notifications import NotificationService
from ignis.services.audio import AudioService
from services.update import UpdateService

network = NetworkService.get_default()
notifications = NotificationService.get_default()
audio = AudioService.get_default()

def indicator_icon(**kwargs):
    return Widget.Icon(style="margin-right: 0.5rem;", css_classes=["unset"], **kwargs)


def wifi_icon():
    def check_visible(*args) -> bool:
        if len(network.wifi.devices) > 0:
            if network.ethernet.is_connected:
                if network.wifi.is_connected:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    icon = indicator_icon(image=network.wifi.bind("icon-name"))
    icon.visible = network.wifi.bind("devices", check_visible)
    icon.visible = network.ethernet.bind("is_connected", check_visible)
    icon.visible = network.wifi.bind("is_connected", check_visible)
    return icon


def ethernet_icon():
    def check_visible(*args) -> bool:
        if len(network.ethernet.devices) > 0:
            if network.wifi.is_connected:
                if network.ethernet.is_connected:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    icon = indicator_icon(image=network.ethernet.bind("icon_name"))
    icon.visible = network.ethernet.bind("devices", check_visible)
    icon.visible = network.wifi.bind("is_connected", check_visible)
    icon.visible = network.ethernet.bind("is_connected", check_visible)
    return icon


def dnd_icon():
    return indicator_icon(
        image="notification-disabled-symbolic",
        visible=notifications.bind("dnd"),
    )

def update_icon():
    update_service = UpdateService.get_default()

    widget = Widget.Box(
        visible=False,  
        child=[
            Widget.Label(
                label="0",  
                css_classes=["count"],  
            ),
            Widget.Icon(
                image="aptdaemon-upgrade-symbolic",
                pixel_size=21,
            ),
        ]
    )

    label = widget.child[0]

    def on_update_count(updates_count):
        widget.visible = updates_count > 0
        label.label = str(updates_count)

    update_service.bind(on_update_count)

    return widget

def volume_icon():
    return indicator_icon(
        image=audio.speaker.bind("icon_name"),
    )


def status_icons():
    return Widget.Box(
        child=[wifi_icon(), ethernet_icon(), volume_icon(), dnd_icon(), update_icon()]
    )
