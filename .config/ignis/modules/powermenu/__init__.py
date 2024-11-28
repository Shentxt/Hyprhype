from ignis.widgets import Widget
from .powermenubuttons import PowermenuButton, poweroff, reboot, suspend, hypr_exit
from ignis.app import IgnisApp

app = IgnisApp.get_default()

def powermenu():
    return Widget.Window(
        popup=True,
        kb_mode="on_demand",
        namespace="ignis_POWERMENU",
        exclusivity="ignore",
        anchor=["left", "right", "top", "bottom"],
        visible=False,
        child=Widget.Overlay(
            child=Widget.Button(
                vexpand=True,
                hexpand=True,
                can_focus=False,
                css_classes=["unset", "powermenu-overlay"],
                on_click=lambda x: app.close_window("ignis_POWERMENU"),
            ),
            overlays=[
                Widget.Box(
                    vertical=True,
                    valign="center",
                    halign="center",
                    css_classes=["powermenu"],
                    child=[
                        Widget.Box(
                            child=[
                                PowermenuButton(
                                    label="Power off",
                                    icon_name="system-shutdown-symbolic",
                                    on_click=poweroff,
                                ),
                                PowermenuButton(
                                    label="Reboot",
                                    icon_name="system-reboot-symbolic",
                                    on_click=reboot,
                                ),
                            ]
                        ),
                        Widget.Box(
                            child=[
                                PowermenuButton(
                                    label="Suspend",
                                    icon_name="night-light-symbolic",
                                    on_click=suspend,
                                ),
                                PowermenuButton(
                                    label="Sign out",
                                    icon_name="system-log-out-symbolic",
                                    on_click=hypr_exit,
                                ),
                            ]
                        ),
                    ],
                )
            ],
        ),
      css_classes=["unset"],
    )
