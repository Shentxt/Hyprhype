from ..qs_button import QSButton
from ignis.utils import Utils
import os
from scripts.gamemode import gamemode_file


def get_gamemode_status():
    if os.path.exists(gamemode_file):
        with open(gamemode_file, 'r') as f:
            gamemode = f.read().strip()
        return gamemode == "true" 
    return False  

def run_gamemode():
    Utils.exec_sh_async("python ~/.config/ignis/scripts/gamemode.py")

def gamemode_button() -> QSButton:
    return QSButton(
        label="Gamemode",
        icon_name="game-symbolic",
        on_activate=lambda btn: run_gamemode(),
        on_deactivate=lambda btn: run_gamemode(),
        active=get_gamemode_status(),
    ) 
