import os
from services.material import MaterialService
from .elements import SwitchRow, SettingsPage, SettingsGroup, FileRow, SettingsEntry
from ignis.widgets import Widget
from ignis.services.wallpaper import WallpaperService
from options import avatar_opt, replace_face_with_avatar
from services.randomwall import WallpaperManager

randomwall = WallpaperManager()
wallpaper = WallpaperService.get_default()
material = MaterialService.get_default()

def appearance_entry(active_page):
    appearance_page = SettingsPage(
        name="Appearance",
        groups=[
            SettingsGroup(
                name="User",
                style="margin-top: 2rem;",
                rows=[
                    Widget.Separator(css_classes=["settings-separator"]),
                    Widget.Box(
                        halign="start",
                        style="margin-left: 2rem;",
                        child=[
                            Widget.Picture(
                                image=avatar_opt.bind(
                                    "value",
                                    lambda value: "user-info"
                                    if not os.path.exists(value)
                                    else value,
                                ),
                                width=96,
                                height=96,
                                style="border-radius: 0.50rem;",
                            ),
                            Widget.Label(
                                label=os.getenv("USER"), css_classes=["settings-user-name"]
                            ),
                        ],
                    ),
                    FileRow(
                        label="Avatar",
                        dialog=Widget.FileDialog(
                            initial_path=avatar_opt.bind("value"),
                            on_file_set=lambda x, gfile: (avatar_opt.set_value(gfile.get_path()),
                            replace_face_with_avatar(gfile)),
                        ),
                    ),
                ],
            ),
            Widget.Separator(css_classes=["separator-mp"]),
            SettingsGroup(
                name="Wallpaper",
                rows=[
                    Widget.Separator(css_classes=["settings-separator"]),
                    Widget.Button(
                        child=Widget.Icon(image="media-playlist-repeat-symbolic", pixel_size=20),
                        halign="end",
                        css_classes=["launch", "unset"],
                        on_click=lambda x: randomwall.fetch_wallpapers(),
                    ),
                    Widget.ListBoxRow(
                        child=Widget.Picture(
                            image=wallpaper.bind("wallpaper"),
                            width=1920 // 4,
                            height=1080 // 4,
                            halign="center",
                            style="border-radius: 1rem;",
                            content_fit="cover",
                        ),
                        selectable=False,
                        activatable=False,
                    ),
                    FileRow(
                        label="Wallpaper path",
                        button_label=os.path.basename(wallpaper.wallpaper)
                        if wallpaper.wallpaper
                        else None,
                        dialog=Widget.FileDialog(
                            on_file_set=lambda x, file: material.generate_colors(
                                file.get_path()
                            ),
                            initial_path=wallpaper.bind("wallpaper"),
                            filters=[
                                Widget.FileFilter(
                                    mime_types=["image/jpeg", "image/png"],
                                    default=True,
                                    name="Images JPEG/PNG",
                                )
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )
    return SettingsEntry(
        label="Appearance",
        icon="preferences-desktop-wallpaper-symbolic",
        active_page=active_page,
        page=appearance_page,
    )
