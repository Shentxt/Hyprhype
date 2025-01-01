import os
from ignis.utils import Utils
from ignis.widgets import Widget
from datetime import datetime
from gi.repository import GObject

NOTES_FOLDER = os.path.expanduser("~/.notes")
AUTHOR = os.getlogin()
DATE = datetime.now().date().isoformat()

if not os.path.exists(NOTES_FOLDER):
    os.makedirs(NOTES_FOLDER)

def get_notes():
    return [f for f in os.listdir(NOTES_FOLDER) if f.endswith(".md")]

class NoteItem(Widget.Button):
    def __init__(self, note_name: str, on_update: callable) -> None:
        self._note_name = note_name
        self._on_update = on_update
        super().__init__(
            on_click=lambda x: self.open_note(),
            on_right_click=lambda x: self._menu.popup(),
            css_classes=["notes"],
            child=Widget.Box(
                child=[
                    Widget.Label(
                        label=note_name,
                        ellipsize="end",
                        max_width_chars=30,
                    ),
                ]
            ),
        )
        self.__sync_menu()

    def open_note(self) -> None:
        note_path = os.path.join(NOTES_FOLDER, self._note_name)
        Utils.exec_sh_async(f"kitty --title 'Float' -e nvim {note_path}")

    def delete_note(self) -> None:
        note_path = os.path.join(NOTES_FOLDER, self._note_name)
        if os.path.exists(note_path):
            os.remove(note_path)
        self._on_update()

    def __sync_menu(self) -> None:
        self._menu = Widget.PopoverMenu(
            items=[  
                Widget.MenuItem(
                    label="󱙑  Delete", 
                    on_activate=lambda x: self.delete_note()
                ),
            ]
        )
        self.child.append(self._menu)


class NoteManager(GObject.GObject):
    __gsignals__ = {
        "notes-updated": (GObject.SIGNAL_RUN_FIRST, None, [])
    }

    def emit_update(self):
        self.emit("notes-updated")

note_manager = NoteManager()

def create_new_note() -> None:
    new_note_name = datetime.now().strftime("%H-%M-%S-%f") + ".md"  
    default_note_path = os.path.join(NOTES_FOLDER, new_note_name)
    with open(default_note_path, "w") as f:
        f.write("---\n")
        f.write(f"Date: {DATE}\n")
        f.write(f"Author: {AUTHOR}\n")
        f.write("---\n")
    note_manager.emit_update()

def update_notes() -> None:
    notes_list = get_notes()
    note_items = [
        NoteItem(note, on_update=lambda: note_manager.emit_update())
        for note in notes_list
    ]
    create_button = Widget.Button(
        label="󰎜  New Notes",
        on_click=lambda x: create_new_note(),
        css_classes=["notes"]
    )
    notes_box.child = [create_button] + note_items

note_manager.connect("notes-updated", lambda x: update_notes())

def notes() -> Widget.Box:
    global notes_box
    notes_box = Widget.Box(vertical=True)
    update_notes()
    return notes_box
