from ignis.widgets import Widget

def curved():
    return Widget.Box(
        css_classes=["curved"],  
        vexpand=False,  
        hexpand=True,  
    )
