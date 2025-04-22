import json

from fabric.hyprland.service import Hyprland
from fabric.widgets.label import Label

kanji_numbers = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十"
}

def convert_to_kanji(number):
    return kanji_numbers.get(number, str(number))  

connection = Hyprland()

workspaceData = connection.send_command("j/activeworkspace").reply
activeWorkspace = json.loads(workspaceData.decode("utf-8"))["name"]
workspace = Label(label=f"{convert_to_kanji(int(activeWorkspace))}", name="center-workspace")

def on_workspace(obj, signal):
    global activeWorkspace
    activeWorkspace = json.loads(signal.data[0])
    workspace.set_label(f"{convert_to_kanji(int(activeWorkspace))}")

connection.connect("event::workspace", on_workspace)