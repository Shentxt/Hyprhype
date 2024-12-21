from ignis.widgets import Widget

def popup() -> Widget.Box:
    menu = Widget.PopoverMenu(
        items=[
            Widget.MenuItem(
                label="Option 1", 
                on_activate=lambda x: print("Option 1 selected!")
            ),
            Widget.Separator(),
            Widget.MenuItem(
                label="Option 2", 
                on_activate=lambda x: print("Option 2 selected!")
            ),
        ]
    )

    
    button = Widget.Button(
        child=Widget.Label(label="Click Me"),
        on_click=lambda x: menu.popup(),
        css_classes=["popup"],
      #  style="background-color: rgba(0, 0, 0, 0); border: none;"  # Hacerlo invisible
    )

    return Widget.Box(
        child=[
            button,  
            menu,    
        ]
    )
