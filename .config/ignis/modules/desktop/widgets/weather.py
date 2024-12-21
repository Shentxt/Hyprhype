from ignis.widgets import Widget
import subprocess, json
from services.weather import main

def weather_widget():
    data = main()  
    temperature = data.get("temp", "N/A")
    icon = data.get("icon", "")  

    return Widget.Box(
        child=[
            Widget.Label(label=icon),  
            Widget.Label(label=f"  {temperature}")  
        ],
        css_classes=["weather"],  
    )
