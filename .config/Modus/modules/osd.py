from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from gi.repository import GLib
from fabric.widgets.centerbox import CenterBox
from services import brightness, audio
import utils.icons as icons

def create_progress_bar(percentage, width=150):
    container = Box(orientation="h", name="progress-container")
    progress = Box(name="progress-fill", style=f"min-width: {percentage * width / 100}px;")
    background = Box(name="progress-background", style=f"min-width: {width}px;")
    background.children = [progress]
    container.children = [background]
    return container


def update_progress_bar(progress_bar, percentage, width=150):
    progress_fill = progress_bar.children[0].children[0]
    progress_fill.set_style(f"min-width: {percentage * width / 100}px;")

def create_labeled_progress(icon, value_text, percentage):
    icon_label = Label(name="osd-icon", markup=icon)
    value = Label(name="osd-value", markup=value_text)
    header = CenterBox(orientation="h", start_children=[icon_label], end_children=[value])
    progress = create_progress_bar(percentage)
    return Box(
        name="control-section", orientation="v", spacing=5, children=[header, progress]
    )

def get_brightness():
    try:
        if hasattr(brightness, 'screen_brightness') and brightness.screen_brightness is not None:
            return round((brightness.screen_brightness / brightness.max_screen) * 100)
        return 0 
    except Exception as e:
        print(f"Error: {e}")
        return 0  


def get_volume():
    return round(audio.speaker.volume) if audio.speaker else 0

class OSD(Window):
    def __init__(self):
        super().__init__(
            name="osd-menu",
            layer="overlay",
            anchor="top center",
            keyboard_mode="on-demand",
            visible=False,
            style_classes="osd-panel",
        )

        self.last_volume = get_volume()
        self.last_brightness = get_brightness()
        self.last_muted = audio.speaker.muted if audio.speaker else False

        self.volume_container = create_labeled_progress(
            self._get_volume_icon(self.last_volume, self.last_muted),
            f"{self.last_volume}%",
            self.last_volume
        )

        if self.last_brightness > 0:
            self.brightness_container = create_labeled_progress(
                self._get_brightness_icon(self.last_brightness),
                f"{self.last_brightness}%",
                self.last_brightness
            )
            self.children = Box(
                orientation="v",
                spacing=10,
                children=[self.brightness_container, self.volume_container],
            )
        else:
            self.children = Box(
                orientation="v",
                spacing=10,
                children=[self.volume_container],
            )

        self.hide_timeout_id = None
        self._connect_signals()
        GLib.timeout_add(100, self._check_changes)

    def _connect_signals(self):
        audio.connect("notify::speaker", self._update_volume)
        if hasattr(brightness, 'connect'):
            brightness.connect("screen", self._update_brightness)

    def _get_volume_icon(self, volume, muted):
        if muted:
            return icons.vol_off
        elif volume == 0:
            return icons.vol_mute
        elif volume < 50:
            return icons.vol_medium
        else:
            return icons.vol_high

    def _get_brightness_icon(self, brightness_level):
        if brightness_level < 30:
            return icons.brightness_low
        elif brightness_level < 70:
            return icons.brightness_medium
        else:
            return icons.brightness_high

    def _update_volume(self, *_):
        volume = get_volume()
        muted = audio.speaker.muted if audio.speaker else False

        icon = self._get_volume_icon(volume, muted)
        self.volume_container.children[0].start_children[0].set_markup(icon)
        self.volume_container.children[0].end_children[0].set_markup(f"{volume}%")
        update_progress_bar(self.volume_container.children[1], volume)

        self.show_all()
        self._reset_timeout()

    def _update_brightness(self, *_):
        brightness_level = get_brightness()

        if brightness_level > 0:
            icon = self._get_brightness_icon(brightness_level)
            self.brightness_container.children[0].start_children[0].set_markup(icon)
            self.brightness_container.children[0].end_children[0].set_markup(f"{brightness_level}%")
            update_progress_bar(self.brightness_container.children[1], brightness_level)

            self.show_all()
            self._reset_timeout()

    def _reset_timeout(self):
        if self.hide_timeout_id:
            GLib.source_remove(self.hide_timeout_id)
        self.hide_timeout_id = GLib.timeout_add(1500, self._hide_osd)

    def _hide_osd(self):
        self.hide()
        self.hide_timeout_id = None
        return False

    def _check_changes(self):
        volume = get_volume()
        brightness_level = get_brightness()
        muted = audio.speaker.muted if audio.speaker else False

        if (
            volume != self.last_volume or
            brightness_level != self.last_brightness or
            muted != self.last_muted
        ):
            self.last_volume = volume
            self.last_brightness = brightness_level
            self.last_muted = muted

            self._update_volume()
            if brightness_level > 0:
                self._update_brightness()
            self.show_all()

        return True
