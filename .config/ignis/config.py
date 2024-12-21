import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# ------------------------------------------------------------------------------

from check_version import check_version

check_version()

from ignis.utils import Utils  # noqa: E402
from ignis.app import IgnisApp  # noqa: E402
from modules.control_center import control_center  # noqa: E402
from modules.bar import bar  # noqa: E402
from modules.desktop import desktop  # noqa: E402
from modules.notification_popup import notification_popup  # noqa: E402
from modules.osd import OSD  # noqa: E402
from modules.powermenu import powermenu  # noqa: E402
from modules.launcher import launcher  # noqa: E402
from modules.media import media_window #noq E402
from modules.datemenu import date_window #noq E402
from modules.mapkey import map_window #noq E402
from modules.popup import popup #noq E402

Utils.exec_sh("hyprctl reload")
app = IgnisApp.get_default()
app.apply_css(Utils.get_current_dir() + "/style.scss")

from services.hyprland import *

launcher()
media_window()
control_center()
date_window()
map_window()

for monitor in range(Utils.get_n_monitors()):
    bar(monitor)
    desktop(monitor)
for monitor in range(Utils.get_n_monitors()):
    notification_popup(monitor)
    popup(monitor)

powermenu()
OSD()
