from ignis.widgets import Icon, Button
from ignis.services.recorder import RecorderService
from ignis.utils import Utils

recorder = RecorderService.get_default()

def recorder_icon():
    def check_state(icon: Icon) -> None:
        if recorder.is_paused:
            icon.remove_css_class("active")
        else:
            icon.add_css_class("active")

    icon = Icon(
        image="media-record-symbolic",
        visible=recorder.bind("active"),
    )

    icon.add_css_class("record-indicator")

    recorder.connect("notify::is-paused", lambda x, y: check_state(icon))

    button = Button(
        child=icon,
        on_click=lambda self: Utils.exec_sh_async("~/.config/ignis/scripts/recording.py stop"),
        visible=recorder.bind("active"),
        css_classes=["kb-layout", "unset"],
    )

    return button
