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
        "NetUp": icons.up_arrow,
        "NetDown": icons.down_arrow,
        "RAM": icons.memory,
        "CPU": icons.cpu,
        "Disk": icons.disk,
        "Temp": icons.temp,
    }

    ALERT_LIMITS = {
        "CPU": 80,
        "RAM": 80,
        "NetUp": 80,
        "NetDown": 80,
        "Disk": 80,
        "Temp": 75,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_name("metrics")
        self.hover_counter = 0
        self.hide_timer = None
        self.last_net_up = 0
        self.last_net_down = 0
        self.last_time = GLib.get_monotonic_time()
        self.progress_bars = {}
        self.icon_labels = {}
        self.metric_buttons = {}

        for system in ["NetUp", "NetDown"] + [k for k in self.ICONS.keys() if k not in ["NetUp", "NetDown"]]:
            self.progress_bars[system] = CircularProgressBar(
                name=f"metric-circle-{system.lower()}",
                line_style="round",
                line_width=2,
                size=28,
                start_angle=150,
                end_angle=390,
            )
            self.icon_labels[system] = Label(
                markup=f'<span size="large">{self.ICONS[system]}</span>',
                name=f"metric-icon-{system.lower()}",
            )
            self.metric_buttons[system] = EventBox(
                name=f"metric-button-{system.lower()}",
                child=Overlay(
                    child=self.progress_bars[system],
                    overlays=[self.icon_labels[system]],
                )
            )
            self.metric_buttons[system].connect("enter-notify-event", self._on_mouse_enter)
            self.metric_buttons[system].connect("leave-notify-event", self._on_mouse_leave)

        self.net_container = Box(spacing=4, children=[self.metric_buttons["NetUp"], self.metric_buttons["NetDown"]])
        self.revealer_box = Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        for system in ["RAM", "CPU", "Disk", "Temp"]:
            self.revealer_box.add(self.metric_buttons[system])

        self.revealer = Revealer(
            transition_type="slide-right",
            transition_duration=250,
            child=self.revealer_box,
            child_revealed=False,
        )

        self.main_container = Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.main_container.add(self.net_container)
        self.main_container.add(self.revealer)

        self.event_box = EventBox(events=["enter-notify-event", "leave-notify-event"])
        self.event_box.add(self.main_container)
        self.event_box.connect("enter-notify-event", self._on_mouse_enter)
        self.event_box.connect("leave-notify-event", self._on_mouse_leave)

        self.add(self.event_box)
        GLib.timeout_add_seconds(1, self._update_system_info)

    def _on_mouse_enter(self, widget, event):
        self.hover_counter += 1
        if self.hide_timer:
            GLib.source_remove(self.hide_timer)
            self.hide_timer = None
        self.revealer.set_reveal_child(True)
        return False

    def _on_mouse_leave(self, widget, event):
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
        now = GLib.get_monotonic_time()
        elapsed = (now - self.last_time) / 1e6
        net = psutil.net_io_counters()
        up_speed_mbps = (net.bytes_sent - self.last_net_up) / elapsed / 125000
        down_speed_mbps = (net.bytes_recv - self.last_net_down) / elapsed / 125000
        total_up_mb = net.bytes_sent / (1024 * 1024)
        total_down_mb = net.bytes_recv / (1024 * 1024)

        self.last_net_up, self.last_net_down, self.last_time = net.bytes_sent, net.bytes_recv, now

        usages = {
            "NetUp": min(up_speed_mbps / self.ALERT_LIMITS["NetUp"] * 100, 100),
            "NetDown": min(down_speed_mbps / self.ALERT_LIMITS["NetDown"] * 100, 100),
            "CPU": psutil.cpu_percent(interval=0),
            "RAM": psutil.virtual_memory().percent,
            "Disk": psutil.disk_usage("/").percent,
            "Temp": self._get_device_temperature() or 0,
        }

        for system, usage in usages.items():
            bar = self.progress_bars[system]
            icon = self.icon_labels[system]
            bar.value = usage / 100.0
            icon.set_markup(f'<span size="large">{self.ICONS[system]}</span>')

            if system == "NetUp":
                self.metric_buttons[system].set_tooltip_text(f"Up: {total_up_mb:.2f} MB")
            elif system == "NetDown":
                self.metric_buttons[system].set_tooltip_text(f"Down: {total_down_mb:.2f} MB")
            else:
                self.metric_buttons[system].set_tooltip_text(f"{system} {usage:.1f}%")

            if usage >= self.ALERT_LIMITS[system]:
                bar.add_style_class("alert")
                icon.add_style_class("alert")
                self.metric_buttons[system].add_style_class("alert")
            else:
                bar.remove_style_class("alert")
                icon.remove_style_class("alert")
                self.metric_buttons[system].remove_style_class("alert")

        return True

    @staticmethod
    def _get_device_temperature():
        try:
            temps = psutil.sensors_temperatures()
            for key in ("coretemp", "cpu_thermal", "k10temp"):
                if key in temps and temps[key]:
                    return round(temps[key][0].current, 1)
        except Exception:
            pass
        return None
