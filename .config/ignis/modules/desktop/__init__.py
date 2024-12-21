from ignis.widgets import Widget
from .widgets.weather import weather_widget
from .widgets.quotes import quotes_widget

def desktop(monitor: int) -> Widget.Window:
    return Widget.Window(
        anchor=["left", "top", "right", "bottom"],  
        exclusivity="exclusive",
        monitor=monitor,
        namespace=f"ignis_DESKTOP_{monitor}",
        layer="background",
        kb_mode="none",  
        child=Widget.Box(
            vertical=True,  
            child=[
                Widget.CenterBox(
                    start_widget=Widget.Box(child=[]),
                    center_widget=Widget.Box(
                        vertical=True, 
                        child=[
                            weather_widget(),
                            Widget.Separator(css_classes=["separator"]),
                            quotes_widget(),
                        ]
                    ),
                    end_widget=Widget.Box(child=[]),
                ),
            ],
        ),
       css_classes=["desktop"],
    )
