from ignis.widgets import Widget
from ignis.utils import Utils
from ..settings import settings_window

def popup_widgets() -> Widget.Box:
    menu = Widget.PopoverMenu(
        items=[
            Widget.MenuItem(
                label="  Hyprland",
                enabled=False,
            ),
            Widget.Separator(),
            Widget.MenuItem(
                label="  Edit",
                on_activate=lambda x: Utils.exec_sh_async("kitty --title 'Float' -e nvim ~/.config/hypr/hyprland.conf")
            ),
            Widget.MenuItem(
                label="  Restart", 
                on_activate=lambda x: Utils.exec_sh_async("~/.config/hypr/scripts/wmreload.sh")
            ),
            Widget.MenuItem(
                label="  Config", 
                on_activate=lambda x: settings_window(),
            ),
        ]
    )

    
    button = Widget.Button(
        child=Widget.Label(label="Hi"),
        on_click=lambda x: menu.popup(),
        css_classes=["popup"],
        halign="center",
    )

    return Widget.Box(
        child=[
            button,  
            menu,    
        ]
    )

def popup(monitor: int) -> Widget.Window:
    return Widget.Window(
        anchor=["left", "top", "right", "bottom"],  
        exclusivity="exclusive",
        monitor=monitor,
        namespace=f"ignis_POPUP_{monitor}",
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
                        popup_widgets(), 
                        ]
                    ),
                    end_widget=Widget.Box(child=[]),
                ),
            ],
        ),
       css_classes=["desktop"],
    )
