from ..qs_button import QSButton
from ignis.utils import Utils

def run_update_system():
    Utils.exec_sh_async("kitty --title 'Float' -e ~/.config/hypr/scripts/get_updates.sh --update-system")

def run_print_updates():
    Utils.exec_sh_async("kitty --title 'Float' -e ~/.config/hypr/scripts/get_updates.sh --print-updates")

def update_button() -> QSButton:
    return QSButton(
        label="Update",
        icon_name="system-software-update-symbolic",
        on_activate=lambda btn: run_update_system(),
        on_right_click=lambda btn: run_print_updates(),
    )
