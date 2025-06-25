import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, GLib, GdkPixbuf
import os
import sys
import importlib.util
import argparse
import fcntl
import subprocess
import asyncio
import random as _random
import colorsys
import json
import inspect
import psutil 
import signal
import time 

def get_relative_path(path: str, level: int = 1) -> str:
    prev_globals = inspect.stack()[level][0].f_globals
    file_var = (
        os.path.dirname(os.path.abspath(prev_globals["__file__"]))
        if "__file__" in prev_globals
        else os.getcwd()
    )
    return os.path.join(file_var, path)

lock_file_path = f"{os.path.expanduser('~')}/.cache/wallpaper.lock"
old_pid = None  
settings_file_path = get_relative_path("../../json/settings.json")

def acquire_lock():
    global lock_file, old_pid
    clean_stale_lock()
    max_retries = 3
    retry_delay = 0.1
    
    if os.path.exists(lock_file_path):
        try:
            with open(lock_file_path, "r") as f:
                pid_str = f.read().strip()
                if pid_str.isdigit():
                    old_pid = int(pid_str)
        except Exception:
            old_pid = None

    current_pid = os.getpid()

    for attempt in range(max_retries):
        try:
            lock_file = open(lock_file_path, "w+")
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_file.seek(0)
            lock_file.truncate()
            lock_file.write(str(current_pid))
            lock_file.flush()
            break
        except (IOError, BlockingIOError):
            if attempt == max_retries - 1:
                return False
            time.sleep(retry_delay)
        except Exception:
            return False

    if old_pid and old_pid != current_pid and psutil.pid_exists(old_pid):
        try:
            proc = psutil.Process(old_pid)
            cmdline = proc.cmdline()
            if any("wallpaper.py" in arg for arg in cmdline):
                proc.kill()
                time.sleep(0.05)
        except Exception:
            pass

    
    time.sleep(0.05)

    try:
        if old_pid and not psutil.pid_exists(old_pid):
            lock_file.seek(0)
            lock_file.truncate()
            lock_file.write(str(current_pid))
            lock_file.flush()
    except Exception:
        pass

    return True

def kill_previous_instances():
    current_pid = os.getpid()

    if os.path.exists(lock_file_path):
        try:
            with open(lock_file_path, "r") as f:
                lock_pid_str = f.read().strip()
                if lock_pid_str.isdigit():
                    lock_pid = int(lock_pid_str)
                    if lock_pid != current_pid and psutil.pid_exists(lock_pid):
                        proc = psutil.Process(lock_pid)
                        cmdline = proc.cmdline()
                        if any("wallpaper.py" in arg for arg in cmdline):
                            proc.kill()
                            time.sleep(0.05)
        except Exception:
            pass

def clean_stale_lock():
    if os.path.exists(lock_file_path):
        try:
            with open(lock_file_path, "r") as f:
                pid_str = f.read().strip()
                if pid_str.isdigit():
                    pid = int(pid_str)
                    if not psutil.pid_exists(pid):
                        os.remove(lock_file_path)
                else:
                    os.remove(lock_file_path)
        except Exception:
            pass

def release_lock():
    fcntl.flock(lock_file, fcntl.LOCK_UN)
    lock_file.close()
    os.remove(lock_file_path)

def hue_to_numeric_hex(hue):
    hue = hue / 360.0
    rgb = colorsys.hls_to_rgb(hue, 0.5, 1.0)
    hex_color_str = "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )
    numeric_hex_color = int(hex_color_str.lstrip("#"), 16)
    return numeric_hex_color

def load_settings():
    default_settings = { 
        "color-scheme": "dark",
        "custom-color": "none",
        "generation-scheme": "tonalSpot",
    }

    if not os.path.exists(settings_file_path):
        os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)
        with open(settings_file_path, "w") as file:
            json.dump(default_settings, file, indent=4)

    with open(settings_file_path, "r") as file:
        return json.load(file)

class FadeWindow(Gtk.Window):
    def __init__(self, image_path, fade_duration):
        super().__init__()
        self.set_keep_below(True)
        self.set_decorated(False)
        self.fullscreen()
        
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)
        GtkLayerShell.set_exclusive_zone(self, -1)
        GtkLayerShell.set_namespace(self, "wallpaper")
        
        screen = self.get_screen()
        width = screen.get_width()
        height = screen.get_height()
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        
        self.image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.add(self.image)
        
        self.fade_duration = fade_duration
        self.tick = 0
        self.image.set_opacity(0)
        
        fps = 60
        self.steps = int(self.fade_duration * fps)
        GLib.timeout_add(int(1000 / fps), self.on_fade_step)
        
        self.show_all()

    def on_fade_step(self):
        self.tick += 1
        progress = self.tick / self.steps
        self.image.set_opacity(progress)
        
        if progress >= 1.0:
            return False
        return True

    def finish(self):
        self.destroy()
        Gtk.main_quit()

def current_state(state_str: str, status_file: str):
    with open(status_file, "w") as f:
        f.write(state_str)

def send_notify(label: str, desc: str, notify: bool):
    if not notify:
        return
    subprocess.run(["notify-send", label, desc])

def state(name: str | None, label: str | None, desc: str | None, status_file: str, notify: bool):
    if name is not None:
        current_state(name, status_file)
    if label is not None:
        send_notify(label, desc or "", notify)

def join(*args):
    return os.path.join(*args)

async def square_image(wallpaper: str, notify: bool, status_file: str):
    square = f"{os.path.expanduser('~')}/.cache/square_wallpaper.png"
    state(None, "Creating square version...", f"with image {wallpaper}", status_file, notify)
    cmd = f"magick {wallpaper}[0] -gravity Center -extent 1:1 {square}"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

async def png_image(wallpaper: str, notify: bool, status_file: str):
    png = f"{os.path.expanduser('~')}/.cache/current_wallpaper.png"
    if wallpaper.lower().endswith((".jpg", ".jpeg")):
        state(None, "Converting jpg to png...", f"with image {wallpaper}", status_file, notify)
        cmd = f"magick {wallpaper}[0] {png}"
    else:
        cmd = f"cp -f {wallpaper} {png}"

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

async def change_wallpaper(args):
    HOME = os.path.expanduser("~")
    cache_file = f"{HOME}/.cache/current_wallpaper"
    
    state("init", None, None, args.status, args.notify)

    settings = load_settings()
    color_scheme = settings["color-scheme"]
    custom_color = settings["custom-color"]
    generation_scheme = settings["generation-scheme"]

    new_wallpaper = f"{HOME}/Pictures/wallpaper/example-1.jpg"

    if args.random:
        files = [
            f
            for f in os.listdir(f"{HOME}/Pictures/wallpaper/")
            if f.endswith((".png", ".jpg", ".jpeg"))
        ]
        if files:
            new_wallpaper = join(f"{HOME}/Pictures/wallpaper", _random.choice(files))
    elif args.prev:
        try:
            with open(cache_file) as f:
                new_wallpaper = f.read().strip()
        except FileNotFoundError:
            pass
    elif args.image is not None:
        new_wallpaper = os.path.abspath(args.image)

    with open(cache_file, "w") as f:
        f.write(new_wallpaper)

    with_image = f"with image {new_wallpaper}"

    state("changing", "Changing wallpaper...", with_image, args.status, args.notify)
    win = FadeWindow(new_wallpaper, args.fade)
    Gtk.main()

    state("colors", "Generating colors...", with_image, args.status, args.notify)
    
    module_path = get_relative_path("../material-colors")
    sys.path.append(module_path)
    module_name = "generate"
    file_path = f"{module_path}/{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    GENERATOR = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(GENERATOR)

    _starts_with = lambda x: str(x).startswith("-")
    GENERATOR.main(
        color_scheme,
        new_wallpaper,
        (
            hue_to_numeric_hex(int(custom_color.lstrip("-")))
            if _starts_with(custom_color)
            else (int(custom_color.lstrip("#"), 16) if custom_color != "none" else None)
        ),
        scheme_name=generation_scheme,
    )

    await asyncio.gather(
        square_image(new_wallpaper, args.notify, args.status),
        png_image(new_wallpaper, args.notify, args.status)
    )

    state("finish", "Wallpaper procedure complete!", with_image, args.status, args.notify)

async def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-I", "--image", type=str, help="Image")
    group.add_argument(
        "-P",
        "--prev",
        help="Use last used wallpaper for color generation",
        action="store_true",
    )
    group.add_argument(
        "-R", "--random", help="Random image from folder", action="store_true"
    )
    parser.add_argument("-n", "--notify", help="Send notifications", action="store_true")
    parser.add_argument(
        "--status", type=str, help="Status file", default="/tmp/wallpaper.status"
    )
    parser.add_argument("--fade", type=float, default=1.0, help="Fade duration (seconds)")

    args = parser.parse_args()
    await change_wallpaper(args)

if __name__ == "__main__":
    acquire_lock()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 
        release_lock()
