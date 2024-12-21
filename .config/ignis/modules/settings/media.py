from ignis.services.recorder import RecorderService
from services.screenshot import ScreenshotService  
from .elements import (
    SpinRow,
    SettingsPage,
    SettingsGroup,
    EntryRow,
    FileRow,
    SettingsEntry,
)
from ignis.widgets import Widget

recorder = RecorderService.get_default()
screenshot_service = ScreenshotService()

def media_entry(active_page):
    recorder_page = SettingsPage(
        name="Media",
        groups=[
            SettingsGroup(
                name="Recorder",
                rows=[
                    Widget.Separator(css_classes=["settings-separator"]),
                    SpinRow(
                        label="Recording bitrate",
                        sublabel="Affects the recording quality",
                        value=recorder.bind("bitrate"),
                        max=640000,
                        width=150,
                        on_change=lambda x, value: recorder.set_bitrate(int(value)),
                        step=1000,
                    ),
                    FileRow(
                        label="Recording path",
                        button_label=recorder.bind("default_file_location"),
                        dialog=Widget.FileDialog(
                            on_file_set=lambda x, file: recorder.set_default_file_location(file.get_path()),
                            select_folder=True,
                            initial_path=recorder.default_file_location,
                        ),
                    ),
                    EntryRow(
                        label="Recording filename",
                        sublabel="Support time formatting",
                        text=recorder.bind("default_filename"),
                        on_change=lambda x: recorder.set_default_filename(x.text),
                        width=200,
                    ),
                ],
            ),
            Widget.Separator(css_classes=["separator-mp"]),
            SettingsGroup(
                name="Screenshot",
                rows=[
                    Widget.Separator(css_classes=["settings-separator"]),
                     FileRow(
                        label="Screenshot path",
                        button_label=screenshot_service.default_file_location,
                        dialog=Widget.FileDialog(
                            on_file_set=lambda x, file: screenshot_service.set_default_file_location(file.get_path()),
                            select_folder=True,
                            initial_path=screenshot_service.default_file_location,
                        ),
                    ),
                    EntryRow(
                        label="Screenshot filename",
                        sublabel="Support time formatting",
                        text=screenshot_service.default_filename,
                        on_change=lambda x: screenshot_service.set_default_filename(x.text),
                        width=200,
                    ),
                ],
            ),
        ],
    )

    return SettingsEntry(
        label="Media",
        icon="media-record-symbolic",
        active_page=active_page,
        page=recorder_page,
    )
