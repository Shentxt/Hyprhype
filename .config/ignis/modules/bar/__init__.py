from ignis.widgets import Widget
from .curved import curved
from .buttons.workspaces import workspaces
from .buttons.powermenu import power_button
from .buttons.kb_layout import kb_layout
from .buttons.notificount import notificount
from .buttons.indicator import indicator
from .buttons.launch_apps import launcher_box 
from .buttons.tray import tray
from .buttons.battery import battery_widget
from .buttons.media import media
from .buttons.clock import clock
from .buttons.recorder import recorder_icon

def bar(monitor: int) -> Widget.Window:
    return Widget.Window(
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        monitor=monitor,
        namespace=f"ignis_BAR_{monitor}",
        layer="bottom",
        kb_mode="none",
        child=Widget.Box(
            vertical=True,  
            child=[
                Widget.CenterBox(
                    css_classes=["bar-widget"],
                    start_widget=Widget.Box(child=[launcher_box(), workspaces()]),
                    center_widget=Widget.Box(child=[notificount(), clock(monitor), media(monitor)]),
                    end_widget=Widget.Box(child=[tray(),kb_layout(),recorder_icon(), battery_widget(), indicator(monitor),power_button()]),
                ),
                curved(),
            ],
        ),
        css_classes=["unset"], 
    )
