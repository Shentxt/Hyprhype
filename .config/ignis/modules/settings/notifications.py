from .elements import SwitchRow, SettingsPage, SettingsGroup, SpinRow, SettingsEntry
from ignis.services.notifications import NotificationService
from ignis.widgets import Widget

import subprocess
import os
import signal

syncthing_process = None

def run_server(state):
    global syncthing_process
    if state:
        if syncthing_process is None or syncthing_process.poll() is not None:
            syncthing_process = subprocess.Popen(
                ["syncthing", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
    else:
        if syncthing_process is not None and syncthing_process.poll() is None:
            os.kill(syncthing_process.pid, signal.SIGINT)
            syncthing_process = None


notifications = NotificationService.get_default()


def notifications_entry(active_page):
    notifications_page = SettingsPage(
        name="Notifications",
        groups=[
            SwitchRow(
                label="Start Server",
                sublabel="You need Syncthing to be able to use it",
                active=(syncthing_process is not None and syncthing_process.poll() is None),
                on_change=lambda x, state: run_server(state),
            ),
            SettingsGroup( 
                name="Notifications",
                rows=[
                    Widget.Separator(css_classes=["settings-separator"]),
                    SpinRow(
                        label="Maximum popups count",
                        sublabel="The first popup will automatically dismiss",
                        value=notifications.bind("max_popups_count"),
                        min=1,
                        on_change=lambda x, value: notifications.set_max_popups_count(
                            value
                        ),
                    ),
                    SpinRow(
                        label="Popup timeout",
                        sublabel="Timeout before popup will be dismissed, in milliseconds.",
                        max=100000,
                        step=100,
                        value=notifications.bind("popup_timeout"),
                        on_change=lambda x, value: notifications.set_popup_timeout(
                            value
                        ),
                    ),
                ],
            )
        ],
    )

    return SettingsEntry(
        label="Notifications",
        icon="notification-symbolic",
        active_page=active_page,
        page=notifications_page,
    )
