from ignis.widgets import Widget
from .buttons.workspaces import workspaces
from .buttons.kb_layout import kb_layout
from .buttons.indicator import indicator
from .buttons.launch_apps import launcher_box 
from .buttons.tray import tray
from .buttons.battery import battery_widget
from .buttons.media import media
from .buttons.clock import clock

def bar(monitor: int) -> Widget.Window:
    return Widget.Window(
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        monitor=monitor,
        namespace=f"ignis_BAR_{monitor}",
        layer="bottom",
        kb_mode="none",
        child=Widget.CenterBox(
            css_classes=["bar-widget"],
            start_widget=Widget.Box(child=[launcher_box(), workspaces()]),
            center_widget=Widget.Box(child=[clock(monitor), media(monitor)]),
            end_widget=Widget.Box(child=[tray(), kb_layout(), battery_widget(), indicator(monitor)]),
        ),
        css_classes=["unset"],
    )
