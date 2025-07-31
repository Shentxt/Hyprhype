import os
import json
from PyQt5 import QtWidgets, QtCore, QtGui

CONFIG_PATH = os.path.expanduser("~/.cache/modus/config/keys.json")

def create_separator():
    sep = QtWidgets.QFrame()
    sep.setFrameShape(QtWidgets.QFrame.HLine)
    sep.setFrameShadow(QtWidgets.QFrame.Sunken)
    sep.setStyleSheet("margin-left: 20px; margin-right: 20px;")
    return sep

class KeyCaptureInput(QtWidgets.QLineEdit):
    keyChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Press shortcut...")
        self.setReadOnly(True)

    def keyPressEvent(self, event):
        modifiers = []
        if event.modifiers() & QtCore.Qt.ControlModifier:
            modifiers.append("Ctrl")
        if event.modifiers() & QtCore.Qt.AltModifier:
            modifiers.append("Alt")
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            modifiers.append("Shift")
        if event.modifiers() & QtCore.Qt.MetaModifier:
            modifiers.append("Super")

        key = event.key()
        key_text = QtGui.QKeySequence(key).toString()
        if not key_text:
            key_text = QtGui.QKeySequence(event.key()).toString()
        if key_text in ("Shift", "Ctrl", "Alt", "Meta"):
            return

        parts = modifiers + [key_text]
        result = "+".join(parts)

        self.setText(result)
        self.keyChanged.emit(result)

class KeybindSection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.default_config = {
            "launch_terminal": "Super+Return",
            "kill_window": "Super+Q",
            "fullscreen": "Super+F",
            "toggle_floating": "Super+Space",
            "lock_screen": "Super+X",
            "screenshot_full": "Super+P",
            "screenshot_area": "Super+Shift+P",
            "record_screen": "Super+Alt+P",
            "launch_launcher": "Super+D",
            "notes_editor": "Super+Alt+D",
            "music_player": "Super+Shift+D",
            "wallpapers": "Super+W",
            "power_menu": "Super+Shift+Q",
            "reload_wm": "Super+R",
            "clip_manager": "Super+C",
            "window_switcher": "Super+S",
            "volume_up": "Super+0x003d",
            "volume_down": "Super+0x002d",
            "volume_toggle": "Super+U",
            "brightness_up": "Super+Shift+0x003d",
            "brightness_down": "Super+Shift+0x002d",
            "brightness_toggle": "Super+Ctrl+I", 
            "hide_bar": "Super+H", 
        }

        self.temp_config = self.load_config()
        self.widgets = {}
        self.reset_buttons = {}

        outer_layout = QtWidgets.QVBoxLayout(self)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        outer_layout.addWidget(scroll_area)

        content_widget = QtWidgets.QWidget()
        scroll_area.setWidget(content_widget)

        layout = QtWidgets.QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        title_bar = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Keybindings")
        title.setStyleSheet("font-size: 20pt;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title_bar.addWidget(title, stretch=1)

        self.global_reset_btn = QtWidgets.QPushButton("\u21BA") 
        self.global_reset_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            font-size: 24px;
            border: none;
            padding: 0px;
            margin: 0px;
            min-width: 80px;
        }
        """)
        self.global_reset_btn.clicked.connect(self.reset_to_defaults)
        title_bar.addWidget(self.global_reset_btn, alignment=QtCore.Qt.AlignRight)

        layout.addLayout(title_bar)
        layout.addWidget(create_separator())

        for key in self.default_config:
            layout.addLayout(self.create_key_input_with_reset(key))

        layout.addStretch()
        self.update_global_reset_visibility()

    def create_key_input_with_reset(self, key):
        hbox = QtWidgets.QHBoxLayout() 
        label = QtWidgets.QLabel(key.replace("_", " ").title())
        label.setFixedWidth(320)

        key_input = KeyCaptureInput()
        key_input.setFixedWidth(200)
        full_value = self.temp_config.get(key, self.default_config[key])
        key_input.setText(full_value)
        key_input.keyChanged.connect(lambda val, key=key: self.handle_change(key, val))

        reset_btn = QtWidgets.QPushButton("\u21BA")
        reset_btn.setFixedSize(18, 22)
        reset_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            font-size: 18px;
            border: none;
            padding: 0;
            margin: 0;
        }
        """)

        def reset():
            val = self.default_config[key]
            self.temp_config[key] = val
            self.save_config()
            key_input.blockSignals(True)
            key_input.setText(val)
            key_input.blockSignals(False)
            self.handle_change(key, val)

        reset_btn.clicked.connect(reset)

        btn_stack = QtWidgets.QStackedLayout()
        placeholder = QtWidgets.QWidget()
        placeholder.setFixedSize(reset_btn.sizeHint()) 

        btn_container = QtWidgets.QWidget()
        btn_layout = QtWidgets.QVBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(reset_btn)

        btn_stack.addWidget(placeholder)     
        btn_stack.addWidget(btn_container)   

        wrapper = QtWidgets.QWidget()
        wrapper.setLayout(btn_stack)

        hbox.addWidget(label)
        hbox.addWidget(key_input)
        hbox.addWidget(wrapper)

        self.widgets[key] = key_input
        self.reset_buttons[key] = btn_stack  

        if full_value == self.default_config.get(key):
            btn_stack.setCurrentIndex(0)
        else:
            btn_stack.setCurrentIndex(1)

        return hbox

    def handle_change(self, key, value):
        self.temp_config[key] = value
        self.save_config()
        if key in self.reset_buttons:
            btn_stack = self.reset_buttons[key]
            if value != self.default_config.get(key):
                btn_stack.setCurrentIndex(1)
            else:
                btn_stack.setCurrentIndex(0)
        self.update_global_reset_visibility()

    def update_global_reset_visibility(self):
        modified = any(
            self.temp_config.get(k) != self.default_config.get(k)
            for k in self.default_config
        )
        self.global_reset_btn.setVisible(modified)

    def reset_to_defaults(self):
        self.temp_config = self.default_config.copy()
        self.save_config()

        for key, widget in self.widgets.items():
            val = self.default_config[key]
            widget.blockSignals(True)
            widget.setText(val)
            widget.blockSignals(False)
            self.handle_change(key, val)

        self.update_global_reset_visibility()

    def load_config(self):
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r") as f:
                    return json.load(f)
        except Exception as e:
            print("Error loading key config:", e)
        return self.default_config.copy()

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.temp_config, f, indent=2)
