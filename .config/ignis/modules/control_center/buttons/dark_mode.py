from services.material import MaterialService
from ..qs_button import QSButton

material = MaterialService.get_default()

def dark_mode_button() -> QSButton:
    return QSButton(
        label=material.bind("dark-mode", lambda value: "Dark" if value else "Light"),
        icon_name=material.bind(
            "dark-mode",
            transform=lambda value: "night-light-symbolic" if value else "weather-clear-symbolic",
        ),
        on_activate=lambda x: material.set_dark_mode(not material.dark_mode),
        on_deactivate=lambda x: material.set_dark_mode(not material.dark_mode),
        active=material.bind("dark-mode"),
    )
