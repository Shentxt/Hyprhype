from ..qs_button import QSButton
from ignis.utils import Utils
from scripts.gamemode import mod_enable, mod_disable

def toggle_gamemode():
    Utils.exec_sh_async("python ~/.config/ignis/scripts/gamemode.py")

def gamemode_button() -> QSButton:
    gamemode_active = False  

    button = QSButton(
        label="gamemode",
        icon_name="game-symbolic" if gamemode_active else "budgie-caffeine-cup-full-symbolic",
        on_activate=lambda x: (mod_enable(), toggle_icon(button)),
        on_deactivate=lambda x: (mod_disable(), toggle_icon(button)),
        active=gamemode_active,
    )

    def toggle_icon(button: QSButton):
        button.active = not button.active
        
        new_icon = "game-symbolic" if button.active else "budgie-caffeine-cup-full-symbolic"
        button.get_icon().set_image(new_icon)
        
        if button.active:
            button.add_css_class("active-class")
            button.remove_css_class("inactive-class")
        else:
            button.add_css_class("inactive-class")
            button.remove_css_class("active-class")

    return button
