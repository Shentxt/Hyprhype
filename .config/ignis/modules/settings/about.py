from .elements import SettingsPage, SettingsRow, SettingsEntry
from ignis.utils import Utils
from ignis.widgets import Widget
from services.material import MaterialService
from ignis.services.fetch import FetchService

fetch = FetchService.get_default()
material = MaterialService.get_default()


def about_entry(active_page):
    about_page = SettingsPage(
        name="About",
        groups=[
            Widget.Separator(css_classes=["settings-separator"]),
            Widget.Box(
                child=[
                    Widget.Box(
                        child=[
                            SettingsRow(label="OS 󰟀", sublabel=fetch.os_name),
                            SettingsRow(label="Ignis version ", sublabel=Utils.get_ignis_version()),
                            SettingsRow(label="Session ", sublabel=fetch.session_type),
                            SettingsRow(label="Compositor ", sublabel=fetch.current_desktop),
                            SettingsRow(label="Kernel ", sublabel=fetch.kernel),
                        ],
                        orientation="vertical",  
                        halign="start",  
                    ),
                    Widget.Picture(
                       # image=material.bind(
                       #     "dark_mode",
                       #     transform=lambda value: fetch.os_logo_text_dark
                       #     if value
                       #     else fetch.os_logo_text,
                       # ),
                        image="/home/shen/.config/ignis/assets/linux.png", 
                        width=350,
                        height=200,
                    ),
                ],
                orientation="horizontal",  
                halign="center",
                width_request=300,
                height_request=100,
            ), 
            Widget.Separator(css_classes=["settings-separator"]),
            SettingsRow(label="Developer", sublabel="-> Shen", halign="center"),
        ], 
    )
    return SettingsEntry(
        label="About",
        icon="help-about-symbolic",
        active_page=active_page,
        page=about_page,
    )
