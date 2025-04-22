import psutil
from gi.repository import GLib, Gtk

from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.widgets.overlay import Overlay
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.button import Button
from fabric.widgets.revealer import Revealer
import utils.icons as icons
from fabric.utils import bulk_connect

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

        self.main_box = Box(spacing=8)

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

        self.revealer = Revealer(transition_type="slide-right", transition_duration=1000)
        
        self.ram_and_button_box = Box(
            orientation=Gtk.Orientation.HORIZONTAL, 
            spacing=8, 
            name="metrics"
        )

        self.memory_overlay = Overlay(
            child=self.progress_bars["RAM"],  
            overlays=[Label(markup=self.ICONS["RAM"])], 
        )

        self.toggle_button = Button(
            child=Label( markup=icons.chevron_left)
        )

        self.ram_and_button_box.add(self.memory_overlay) 
        separator = Box(orientation=Gtk.Orientation.VERTICAL, v_expand=True, name="dock-separator")
        self.ram_and_button_box.add(separator)
        self.ram_and_button_box.add(self.toggle_button)   

        self.revealer_box = Box(
                spacing=8, 
                name="metrics-revealer"
                )
         #Box(spacing=8)
        for system, icon_name in self.ICONS.items():
            if system == "RAM":
                continue  
            overlay = Overlay(
                child=self.progress_bars[system],
                overlays=[Label(markup=icon_name)], 
            )
            self.revealer_box.add(overlay)

        self.revealer.add(self.revealer_box)

        bulk_connect(
            self.toggle_button,
            {
                "enter-notify-event": self._on_enter,
                "leave-notify-event": self._on_leave,
                "button-press-event": self.toggle_revealer,
            },
        )

        self.add(self.ram_and_button_box)  
        self.add(self.revealer)

        GLib.timeout_add_seconds(1, self._update_system_info)

    def _on_enter(self, *args):
        self.toggle_button.set_cursor("pointer")

    def _on_leave(self, *args):
        self.toggle_button.set_cursor("default")

    def toggle_revealer(self, *args):
        new_state = not self.revealer.get_reveal_child()
        self.revealer.set_reveal_child(new_state)
        
        new_icon = icons.chevron_right if new_state else icons.chevron_left
        self.toggle_button.get_child().set_markup(new_icon)

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
