import os
import json
import subprocess
from PyQt5 import QtWidgets, QtCore, QtGui

CONFIG_PATH = os.path.expanduser("~/.cache/modus/config/config.json")

def create_separator():
    sep = QtWidgets.QFrame()
    sep.setFrameShape(QtWidgets.QFrame.HLine)
    sep.setFrameShadow(QtWidgets.QFrame.Sunken)
    sep.setStyleSheet("margin-left: 20px; margin-right: 20px;")
    return sep

class ToggleSlider(QtWidgets.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRange(0, 1)
        self.setSingleStep(1)
        self.setPageStep(1)

    def mousePressEvent(self, event):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        handle_rect = self.style().subControlRect(
            QtWidgets.QStyle.CC_Slider,
            opt,
            QtWidgets.QStyle.SC_SliderHandle,
            self
        )
        if handle_rect.contains(event.pos()):
            self.setValue(1 if self.value() == 0 else 0)
            event.accept()
        else:
            event.ignore()

class ThemeSection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_config = {
            "border_enabled": True,
            "border_size": 1,
            "border_radius": 10,
            "gaps_in": 5,
            "gaps_out": 20,
            "active_opacity": 0.6,
            "inactive_opacity": 0.5,
            "shadow_enabled": True,
            "shadow_range": 20,
            "shadow_render_power": 3,
            "font_name": "Minecraft Rus",
            "font_size": 12,
            "cursor_theme": "nier-cursors-bin",
            "cursor_size": 24,
            "icon_theme": "Windows-Beuty",
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
        title = QtWidgets.QLabel("Theme Settings")
        title.setStyleSheet("font-size: 20pt;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title_bar.addWidget(title, stretch=1)

        self.global_reset_btn = QtWidgets.QPushButton("↺")
        self.global_reset_btn.setFixedSize(8, 25)
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

        layout.addLayout(self.create_subsection_title("Hyprland"))

        layout.addLayout(self.create_toggle_slider_with_reset("Enable Borders", "border_enabled", self.on_borders_toggled))
        layout.addLayout(self.create_slider_with_reset("Border Size:", 0, 10, "border_size", self.on_border_size_changed))
        layout.addLayout(self.create_slider_with_reset("Border Radius:", 0, 40, "border_radius", self.on_radius_changed))

        layout.addLayout(self.create_slider_with_reset("Gaps In:", 0, 50, "gaps_in", self.on_gaps_in_changed))
        layout.addLayout(self.create_slider_with_reset("Gaps Out:", 0, 50, "gaps_out", self.on_gaps_out_changed))

        layout.addLayout(self.create_double_slider_with_reset("Active Opacity:", 0.0, 1.0, "active_opacity", self.on_active_opacity_changed))
        layout.addLayout(self.create_double_slider_with_reset("Inactive Opacity:", 0.0, 1.0, "inactive_opacity", self.on_inactive_opacity_changed))

        layout.addLayout(self.create_toggle_slider_with_reset("Enable Shadows", "shadow_enabled", self.on_shadow_enabled_changed))
        layout.addLayout(self.create_slider_with_reset("Shadow Range", 0, 100, "shadow_range", self.on_shadow_range_changed))
        layout.addLayout(self.create_slider_with_reset("Render Power", 1, 10, "shadow_render_power", self.on_shadow_render_power_changed))

        layout.addWidget(create_separator())

        layout.addLayout(self.create_subsection_title("GTK and QT"))

        layout.addLayout(self.create_combo_box_with_reset(self.get_system_fonts(), "System Font:", "font_name", self.on_font_changed))
        layout.addLayout(self.create_slider_with_reset("Font Size:", 6, 30, "font_size", self.on_font_size_changed))

        layout.addLayout(self.create_combo_box_with_reset(self.get_cursor_themes(), "Cursor Theme:", "cursor_theme", self.on_cursor_theme_changed))
        layout.addLayout(self.create_slider_with_reset("Cursor Size:", 16, 64, "cursor_size", self.on_cursor_size_changed))

        layout.addLayout(self.create_combo_box_with_reset(self.get_icon_themes(), "Icon Theme:", "icon_theme", self.on_icon_theme_changed))

        layout.addStretch()

        self.update_global_reset_visibility()
        for key, btn in self.reset_buttons.items():
            if self.temp_config.get(key) == self.default_config.get(key):
                btn.hide()
            else:
                btn.show()

    def create_subsection_title(self, text):
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(text)
        label.setStyleSheet("font-size: 13pt; font-weight: bold; margin-left: 10px;")
        hbox.addWidget(label)
        hbox.setContentsMargins(20, 0, 0, 0)
        hbox.addStretch()
        return hbox

    def create_reset_button(self, key, widget, on_change):
        btn = QtWidgets.QPushButton("↺")
        btn.setFixedSize(18, 22)
        btn.setStyleSheet("""
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
            if isinstance(widget, QtWidgets.QComboBox):
                idx = widget.findText(val)
                if idx >= 0:
                    widget.setCurrentIndex(idx)
            elif isinstance(widget, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox, ToggleSlider)):
                widget.blockSignals(True)
                widget.setValue(val)
                widget.blockSignals(False)
            on_change(val)
            self.handle_change(key, val, on_change)  
        btn.clicked.connect(reset)

        self.reset_buttons[key] = btn
        if self.temp_config.get(key) == self.default_config.get(key):
            btn.hide()
        return btn

    def create_combo_box_with_reset(self, options, label_text, key, on_change):
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        combo = QtWidgets.QComboBox()
        combo.addItems(options)
        if self.temp_config.get(key) in options:
            combo.setCurrentText(self.temp_config[key])
        combo.currentTextChanged.connect(lambda val: self.handle_change(key, val, on_change))
        reset_btn = self.create_reset_button(key, combo, on_change)
        hbox.addWidget(label)
        hbox.addWidget(combo)
        hbox.addWidget(reset_btn)
        self.widgets[key] = combo
        return hbox

    def create_toggle_slider_with_reset(self, label_text, key, on_change):
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        slider = ToggleSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 1)
        slider.setValue(int(self.temp_config.get(key, True)))
        slider.setFixedWidth(80)
        slider.valueChanged.connect(lambda val: self.handle_change(key, bool(val), on_change))
        reset_btn = self.create_reset_button(key, slider, on_change)
        hbox.addWidget(label)
        hbox.addWidget(slider)
        hbox.addWidget(reset_btn)
        self.widgets[key] = slider
        return hbox

    def create_slider_with_reset(self, label_text, min_val, max_val, key, on_change):
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        spin_box = QtWidgets.QSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setValue(self.temp_config.get(key, 10))
        spin_box.setFixedWidth(80)
        spin_box.valueChanged.connect(lambda val: self.handle_change(key, val, on_change))
        reset_btn = self.create_reset_button(key, spin_box, on_change)
        hbox.addWidget(label)
        hbox.addWidget(spin_box)
        hbox.addWidget(reset_btn)
        self.widgets[key] = spin_box
        return hbox

    def create_double_slider_with_reset(self, label_text, min_val, max_val, key, on_change):
        hbox = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        spin_box = QtWidgets.QDoubleSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setSingleStep(0.01)
        spin_box.setDecimals(2)
        spin_box.setValue(self.temp_config.get(key, min_val))
        spin_box.setFixedWidth(80)
        spin_box.valueChanged.connect(lambda val: self.handle_change(key, val, on_change))
        reset_btn = self.create_reset_button(key, spin_box, on_change)
        hbox.addWidget(label)
        hbox.addWidget(spin_box)
        hbox.addWidget(reset_btn)
        self.widgets[key] = spin_box
        return hbox

    def handle_change(self, key, value, callback):
        self.temp_config[key] = value
        self.save_config()
        callback(value)
        if key in self.reset_buttons:
            if value != self.default_config.get(key):
                self.reset_buttons[key].show()
            else:
                self.reset_buttons[key].hide()
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
            callback = getattr(self, f'on_{key}_changed', lambda x: None)
        
            if isinstance(widget, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox, ToggleSlider)):
                widget.blockSignals(True)
                widget.setValue(val)
                widget.blockSignals(False)
            elif isinstance(widget, QtWidgets.QComboBox):
                idx = widget.findText(val)
                if idx >= 0:
                    widget.blockSignals(True)
                    widget.setCurrentIndex(idx)
                    widget.blockSignals(False)
            self.handle_change(key, val, callback)  


        self.on_radius_changed(self.temp_config["border_radius"])
        self.on_icon_theme_changed(self.temp_config["icon_theme"])

        for btn in self.reset_buttons.values():
            btn.hide()
        self.update_global_reset_visibility() 

    def load_config(self):
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r") as f:
                    return json.load(f)
        except Exception as e:
            print("Error loading config:", e)
        return self.default_config.copy()

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.temp_config, f, indent=2)

    def on_radius_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "decoration:rounding", str(value)])

    def on_borders_toggled(self, enabled):
        value = "1" if enabled else "0"
        subprocess.run(["hyprctl", "keyword", "general:border_size", value])

    def on_border_size_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "general:border_size", str(value)])

    def on_gaps_in_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "general:gaps_in", str(value)])

    def on_gaps_out_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "general:gaps_out", str(value)])

    def on_active_opacity_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "decoration:active_opacity", str(value)])

    def on_inactive_opacity_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "decoration:inactive_opacity", str(value)])

    def on_shadow_enabled_changed(self, enabled):
        subprocess.run(["hyprctl", "keyword", "decoration:shadow:enabled", "true" if enabled else "false"])

    def on_shadow_range_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "decoration:shadow:range", str(value)])

    def on_shadow_render_power_changed(self, value):
        subprocess.run(["hyprctl", "keyword", "decoration:shadow:render_power", str(value)])

    def get_system_fonts(self):
        try:
            output = subprocess.check_output(["fc-list", ":family"], universal_newlines=True)
            fonts = set()
            for line in output.splitlines():
                parts = line.split(":")
                if len(parts) < 2:
                    continue
                families = parts[1].split(",")
                for fam in families:
                    fonts.add(fam.strip())
            return sorted(fonts)
        except Exception as e:
            print("Error:", e)
            return []

    def on_font_changed(self, font_name):
        size = self.temp_config.get("font_size", 11)
        font = QtGui.QFont(font_name, size)
        QtWidgets.QApplication.setFont(font)
        main_window = self.window()
        if main_window:
            self.apply_font_recursively(main_window, font)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "font-name", font_name])
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "document-font-name", font_name])
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "monospace-font-name", font_name])

    def on_font_size_changed(self, size):
        current_font = QtGui.QFont(self.temp_config.get("font_name", "Sans"))
        current_font.setPointSize(size)
        QtWidgets.QApplication.setFont(current_font)
        self.apply_font_recursively(self, current_font)

    def apply_font_recursively(self, widget, font):
        widget.setFont(font)
        for child in widget.findChildren(QtWidgets.QWidget):
            child.setFont(font)

    def get_cursor_themes(self):
        paths = [
            os.path.expanduser('~/.icons'),
            os.path.expanduser('~/.local/share/icons'),
            '/usr/share/icons'
        ]
        themes = set()
        for path in paths:
            if not os.path.isdir(path):
                continue
            for entry in os.listdir(path):
                theme_path = os.path.join(path, entry)
                if os.path.isdir(os.path.join(theme_path, 'cursors')):
                    themes.add(entry)
        return sorted(themes)

    def get_icon_themes(self):
        paths = [
            os.path.expanduser('~/.icons'),
            os.path.expanduser('~/.local/share/icons'),
            '/usr/share/icons'
        ]
        themes = set()
        for path in paths:
            if not os.path.isdir(path):
                continue
            for entry in os.listdir(path):
                index_path = os.path.join(path, entry, 'index.theme')
                if os.path.isfile(index_path):
                    themes.add(entry)
        excluded = {"default", "hicolor", "pixelfun2-dracula"}
        return sorted(
            theme for theme in themes
            if theme.lower() not in excluded and "cursor" not in theme.lower()
        )

    def on_cursor_theme_changed(self, theme):
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", theme])
        subprocess.run(["hyprctl", "setcursor", theme, str(self.temp_config["cursor_size"])])

    def on_cursor_size_changed(self, size):
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-size", str(size)])
        subprocess.run(["hyprctl", "setcursor", self.temp_config["cursor_theme"], str(size)])

    def on_icon_theme_changed(self, theme_name):
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", theme_name])
