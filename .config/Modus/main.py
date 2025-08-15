import os
import tempfile
import setproctitle
import subprocess

from fabric import Application
from fabric.utils import get_relative_path, monitor_file, exec_shell_command
from loguru import logger

from modules.bar.bar import Bar, ScreenCorners
from modules.launcher.launcher import Launcher
from modules.bar.bottom import Bottom
from modules.notification_popup import NotificationPopup

from modules.osd import OSD

from services import sc

from utils.qess import cache_compiled_qss

from pathlib import Path

qss_dir = Path.home() / ".config/Modus/styles"
scss_path = Path.home() / ".cache/material/colors.scss"
cache_dir = Path.home() / ".cache/material/cached_colors"

cache_compiled_qss(qss_dir, scss_path, cache_dir)

for log in [
    "fabric.hyprland.widgets",
    "fabric.audio.service",
    "fabric.bluetooth.service",
]:
    logger.disable(log)

config_path = os.path.expanduser("~/Modus/json/config.json")

def update_main_css():
    colors_css_path = f"/home/{os.getlogin()}/.cache/material/colors.css"
    main_css_path = get_relative_path("styles/main.css")

    if os.path.exists(colors_css_path):
        with open(main_css_path, "r+") as css_file:
            content = css_file.read()
            updated_content = content.replace("@COLORS_CSS_PATH", colors_css_path)
            css_file.seek(0)
            css_file.write(updated_content)
            css_file.truncate()
    else:
        logger.warning(f"[Main] colors.css not found at {colors_css_path}")


def apply_style(app: Application):
    logger.info("[Main] Applying CSS")
    app.set_stylesheet_from_file(get_relative_path("styles/main.css"))    

def on_styles_changed(app):
    logger.info("[Main] Styles changed, recompiling QSS and applying CSS")
    cache_compiled_qss(qss_dir, scss_path, cache_dir)  
    apply_style(app)

if __name__ == "__main__":
    update_main_css()  
    sc = sc
    bar = Bar()
    bottom = Bottom ()
    corners = ScreenCorners()
    osd = OSD()
    notif = NotificationPopup()
    launcher = Launcher()

    app = Application(
        "modus",
        bar,
        bottom,
        launcher,
        osd,
    )
    setproctitle.setproctitle("modus")  

    # Monitor CSS files for changes
    css_file = monitor_file(get_relative_path("styles"))
    _ = css_file.connect("changed", lambda *_: apply_style(app))  

    for qss_file in qss_dir.glob("*.qss"):
        file_monitor = monitor_file(str(qss_file))
        file_monitor.connect("changed", lambda *_: on_styles_changed(app))

    color_css_file = monitor_file(f"/home/{os.getlogin()}/.cache/material/colors.css")
    _ = color_css_file.connect("changed", lambda *_: apply_style(app)) 

    # Apply the styles and run the application
    cache_compiled_qss(qss_dir, scss_path, cache_dir)
    apply_style(app)
    app.run()
    Utils.exec_sh("hyprctl reload")
