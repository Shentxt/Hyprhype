import psutil
from gi.repository import GLib, Gtk
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.widgets.overlay import Overlay
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.revealer import Revealer
from fabric.widgets.eventbox import EventBox
import utils.icons as icons

class Metrics(Box):
    ICONS = {
        "RAM": icons.memory,
        "CPU": icons.cpu,
        "Swap": icons.swap,
        "Disk": icons.disk,
        "Temp": icons.temp,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hover_counter = 0
        self.hide_timer = None

        self.progress_bars = {
            system: CircularProgressBar(
                name="metric-circle",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )
            for system in self.ICONS
        }

        self.revealer = Revealer(transition_type="slide-right", transition_duration=250)

        self.main_box = Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8, name="metrics")

        self.ram_and_button_box = Box(
            orientation=Gtk.Orientation.HORIZONTAL, 
            spacing=8, 
        )

        self.memory_overlay = Overlay(
            child=self.progress_bars["RAM"],  
            overlays=[Label(markup=self.ICONS["RAM"])], 
        )

        self.ram_and_button_box.add(self.memory_overlay) 

        self.revealer_box = Box(spacing=8)

        for system, icon_name in self.ICONS.items():
            if system == "RAM":
                continue
            overlay = Overlay(
                child=self.progress_bars[system],
                overlays=[Label(markup=icon_name)], 
            )
            self.revealer_box.add(overlay)

        self.revealer.add(self.revealer_box)

        self.main_box.add(self.ram_and_button_box)
        self.main_box.add(self.revealer)

        self.event_box = EventBox(events=["enter-notify-event", "leave-notify-event"])
        self.event_box.connect("enter-notify-event", self._on_mouse_enter)
        self.event_box.connect("leave-notify-event", self._on_mouse_leave)
        self.event_box.add(self.main_box)

        self.add(self.event_box)

        GLib.timeout_add_seconds(1, self._update_system_info)

    def _on_mouse_enter(self, *args):
        self.hover_counter += 1
        if self.hide_timer:
            GLib.source_remove(self.hide_timer)
            self.hide_timer = None
        self.revealer.set_reveal_child(True)
        return False

    def _on_mouse_leave(self, *args):
        self.hover_counter -= 1
        if self.hover_counter <= 0:
            self.hide_timer = GLib.timeout_add(500, self._hide_revealer)
        return False

    def _hide_revealer(self):
        self.revealer.set_reveal_child(False)
        self.hover_counter = 0
        self.hide_timer = None
        return False

    def _update_system_info(self):
        usages = {
            "CPU": psutil.cpu_percent(interval=0),
            "RAM": psutil.virtual_memory().percent,
            "Swap": psutil.swap_memory().percent,
            "Disk": psutil.disk_usage("/").percent,
            "Temp": self._get_device_temperature() or 0,
        }

        for system, usage in usages.items():
            self.progress_bars[system].value = usage / 100.0
            self.progress_bars[system].set_tooltip_text(f"{system} {usage:.1f}%")

        return True

    @staticmethod
    def _get_device_temperature():
        try:
            temps = psutil.sensors_temperatures()
            for key in ("coretemp", "cpu_thermal"):
                if key in temps and temps[key]:
                    return round(temps[key][0].current, 1)
        except Exception:
            pass
        return None
