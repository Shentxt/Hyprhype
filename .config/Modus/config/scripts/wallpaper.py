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


def get_relative_path(path: str, level: int = 1) -> str:
    prev_globals = inspect.stack()[level][0].f_globals
    file_var = (
        os.path.dirname(os.path.abspath(prev_globals["__file__"]))
        if "__file__" in prev_globals
        else os.getcwd()
    )
    return os.path.join(file_var, path)


lock_file_path = "/tmp/wallpaper.lock"
settings_file_path = get_relative_path("../../json/settings.json")


def acquire_lock():
    global lock_file
    lock_file = open(lock_file_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_file.write(str(os.getpid()))
        lock_file.flush()
    except IOError:
        print("Another instance of the script is already running.")
        sys.exit(1)


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

args = parser.parse_args()

random = args.random
prev = args.prev
image = args.image
notify = args.notify
status = args.status

HOME = os.path.expanduser("~")

module_path = get_relative_path("../material-colors")
sys.path.append(module_path)

module_name = "generate"
file_path = f"{module_path}/{module_name}.py"

spec = importlib.util.spec_from_file_location(module_name, file_path)
GENERATOR = importlib.util.module_from_spec(spec)  # type: ignore
spec.loader.exec_module(GENERATOR)  # type: ignore

cache_file = f"{HOME}/.cache/current_wallpaper"
square = f"{HOME}/.cache/square_wallpaper.png"
png = f"{HOME}/.cache/current_wallpaper.png"


def current_state(state_str: str):
    with open(status, "w") as f:
        f.write(state_str)


def send_notify(label: str, desc: str):
    if not notify:
        return
    subprocess.run(["notify-send", label, desc])


def state(name: str | None, label: str | None, desc: str | None):
    if name is not None:
        current_state(name)
    if label is not None:
        send_notify(label, desc or "")


def join(*args):
    return os.path.join(*args)


async def main():
    state("init", None, None)

    settings = load_settings()
    color_scheme = settings["color-scheme"]
    custom_color = settings["custom-color"]
    generation_scheme = settings["generation-scheme"]
    swww_animation = "wipe"
    wallpaper_engine = "swww"

    new_wallpaper = f"{HOME}/Pictures/wallpaper/example-1.jpg"
    # new_wallpaper = get_relative_path("../assets/wallpapers/1.png")

    if random:
        files = [
            f
            for f in os.listdir(f"{HOME}/Pictures/wallpaper/")
            if f.endswith((".png", ".jpg", ".jpeg"))
        ]
        if files:
            new_wallpaper = join(f"{HOME}/Pictures/wallpaper", _random.choice(files))
    elif prev:
        try:
            with open(cache_file) as f:
                new_wallpaper = f.read().strip()
        except FileNotFoundError:
            pass
    elif image is not None:
        new_wallpaper = os.path.abspath(image)

    print(f":: Wallpaper {new_wallpaper}")

    with open(cache_file, "w") as f:
        f.write(new_wallpaper)

    with_image = f"with image {new_wallpaper}"

    # -----------------------------------------------------
    # Set the new wallpaper
    # -----------------------------------------------------

    transition_type = swww_animation

    state("changing", "Changing wallpaper...", with_image)
    print(":: Changing wallpaper...")

    if wallpaper_engine == "swww":
        print(":: Using swww")

        cursor_pos = subprocess.getoutput("hyprctl cursorpos").replace(", ", ",")
        
        subprocess.run(
            [
                "swww",
                "img",
                new_wallpaper,
                "--transition-bezier",
                ".43,1.19,1,.4",
                "--transition-fps",
                "60",
                "--transition-type",
                transition_type,
                "--transition-duration",
                "0.7",
                "--transition-pos",
                cursor_pos,
            ]
        )

    else:
        print(":: Wallpaper Engine disabled")

    # -----------------------------------------------------
    # Generate colors
    # -----------------------------------------------------
    state("colors", "Generating colors...", with_image)
    print(":: Generate colors")
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

    # Generate square and png versions
    await asyncio.gather(square_image(new_wallpaper), png_image(new_wallpaper))

    state("finish", "Wallpaper procedure complete!", with_image)


async def png_image(wallpaper: str):
    if wallpaper.lower().endswith((".jpg", ".jpeg")):
        state(None, "Converting jpg to png...", f"with image {wallpaper}")
        print(":: Converting jpg to png...")
        cmd = f"magick {wallpaper}[0] {png}"
    else:
        cmd = f"cp -f {wallpaper} {png}"

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(f":: Error while processing image: {stderr.decode()}")
    else:
        print(":: JPG successfully converted to PNG!")


async def square_image(wallpaper):
    state(None, "Creating square version...", f"with image {wallpaper}")
    print(":: Creating square version")
    cmd = f"magick {wallpaper}[0] -gravity Center -extent 1:1 {square}"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(f":: Error while processing image: {stderr.decode()}")
    else:
        print(":: Square image created!")


if __name__ == "__main__":
    acquire_lock()
    try:
        asyncio.run(main())
    finally:
        release_lock()
