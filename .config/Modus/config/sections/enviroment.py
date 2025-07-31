import os
import shutil
import subprocess
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

def create_separator():
    sep = QtWidgets.QFrame()
    sep.setFrameShape(QtWidgets.QFrame.HLine)
    sep.setFrameShadow(QtWidgets.QFrame.Sunken)
    sep.setStyleSheet("margin-left: 20px; margin-right: 20px;")
    return sep

class EnvSection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("Presets Settings")
        title.setStyleSheet("font-size: 20pt; margin-top: 20px;")
        title.setAlignment(QtCore.Qt.AlignCenter)  
        layout.addWidget(title) 

        layout.addWidget(create_separator())
        
        #title 
        font_title = QtGui.QFont()
        font_title.setPointSize(20)
        font_subtitle = QtGui.QFont()
        font_subtitle.setPointSize(8)

        tips_row = QtWidgets.QHBoxLayout()
        tips_row.setContentsMargins(100, 0, 100, 0)
        tips_row.setSpacing(10)

        tips_icon = QtWidgets.QLabel("󱠂")
        tips_icon.setFont(font_title)

        tips_label = QtWidgets.QLabel(" Check the box to Restart or Backup your configuration")
        tips_label.setFont(font_subtitle)

        tips_row.addWidget(tips_icon)
        tips_row.addWidget(tips_label)
        tips_row.addStretch()

        tips_widget = QtWidgets.QWidget()
        tips_widget.setLayout(tips_row)
        layout.addWidget(tips_widget)

        columns_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(columns_layout)

        self.left_column = QtWidgets.QVBoxLayout()
        self.center_column = QtWidgets.QVBoxLayout()
        self.right_column = QtWidgets.QVBoxLayout()

        self.left_column.setAlignment(QtCore.Qt.AlignTop)
        self.center_column.setAlignment(QtCore.Qt.AlignTop)
        self.right_column.setAlignment(QtCore.Qt.AlignTop)

        left_wrapper = QtWidgets.QWidget()
        left_wrapper.setLayout(self.left_column)
        left_wrapper.setMaximumWidth(300)

        center_wrapper = QtWidgets.QWidget()
        center_wrapper.setLayout(self.center_column)
        center_wrapper.setMaximumWidth(300)

        right_wrapper = QtWidgets.QWidget()
        right_wrapper.setLayout(self.right_column)
        right_wrapper.setMaximumWidth(300)

        divider1 = QtWidgets.QFrame()
        divider1.setFrameShape(QtWidgets.QFrame.VLine)
        divider1.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider1.setFixedWidth(3)
        divider1.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 1px; margin-left: 10px; margin-right: 10px; }")

        divider2 = QtWidgets.QFrame()
        divider2.setFrameShape(QtWidgets.QFrame.VLine)
        divider2.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider2.setFixedWidth(3)
        divider2.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 1px; margin-left: 10px; margin-right: 10px; }")

        columns_layout.addWidget(left_wrapper)
        columns_layout.addWidget(divider1)
        columns_layout.addWidget(center_wrapper)
        columns_layout.addWidget(divider2)
        columns_layout.addWidget(right_wrapper)

        columns_layout.setStretch(0, 1)
        columns_layout.setStretch(1, 0)
        columns_layout.setStretch(2, 1)
        columns_layout.setStretch(3, 0)
        columns_layout.setStretch(4, 1)
         
        sections = [
            ("Hyprland", "hyprland.conf", "~/.config/hypr/hyprland.conf"),
            ("Hypridle", "hypridle.conf", "~/.config/hypr/hypridle.conf"),
            ("Hyprlock", "hyprlock.conf", "~/.config/hypr/hyprlock.conf"),
            ("Kitty", "kitty.conf", "~/.config/kitty/kitty.conf"),
            ("Neovim", "nvim", "~/.config/nvim", True),
            ("Ly", "config.ini", "/etc/ly/config.ini"),
        ]
    
        MAX_PER_COLUMN = 2
        columns = [self.left_column, self.right_column, self.center_column]

        col_idx = 0
        count_in_col = 0

        for section in sections:
            widget = self.create_config_section(*section)
            columns[col_idx].addWidget(widget)
            count_in_col += 1

            if count_in_col >= MAX_PER_COLUMN:
                col_idx += 1
                count_in_col = 0
                if col_idx >= len(columns):
                    col_idx = len(columns) - 1 

    def create_config_section(self, name, config_file, dest_path, is_directory=False):
        box = QtWidgets.QVBoxLayout()
        box.setSpacing(1)
 
        checkbox = QtWidgets.QCheckBox(f" {name}")
        checkbox.setContentsMargins(0, 0, 0, 0)
        box.addWidget(checkbox)

        button_box = QtWidgets.QHBoxLayout()
        button_box.setSpacing(4)

        copy_button = QtWidgets.QPushButton("󰆒")
        backup_button = QtWidgets.QPushButton("󰁯")
        button_box.addWidget(copy_button)
        button_box.addWidget(backup_button)

        button_widget = QtWidgets.QWidget()
        button_widget.setLayout(button_box)
        button_widget.setVisible(False)
        box.addWidget(button_widget)

        def on_toggled(state):
            button_widget.setVisible(state)

        def on_copy_clicked():
            if checkbox.isChecked():
                src = os.path.expanduser(f"~/.config/Modus/config/config/{config_file}")
                dest = os.path.expanduser(dest_path)
                try:
                    if is_directory:
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy(src, dest)
                    subprocess.run([
                        "notify-send", "Fuuka - Copy",
                        f"Successfully copied to: {dest}",
                        "-i", os.path.expanduser("~/.config/Modus/assets/Icon/fuuka.png")
                    ])
                    if name == "Hyprland":
                        subprocess.run(["hyprctl", "reload"], check=True)
                except Exception as e:
                    subprocess.run([
                        "notify-send", "Morgana - Copy",
                        f"Failed to copy: {str(e)}",
                        "-i", os.path.expanduser("~/.config/Modus/assets/Icon/morgana.png")
                    ])

        def on_backup_clicked():
            if checkbox.isChecked():
                src = os.path.expanduser(dest_path)
                backups_dir = os.path.expanduser("~/backups")
                os.makedirs(backups_dir, exist_ok=True)

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(src.rstrip("/"))
                backup_name = f"{base_name}_{timestamp}"
                backup_path = os.path.join(backups_dir, backup_name)

                try:
                    if os.path.exists(src):
                        if os.path.isdir(src):
                            shutil.copytree(src, backup_path)
                        else:
                            shutil.copy(src, backup_path)
                        subprocess.run([
                            "notify-send", "Fuuka - Backup",
                            f"Backup created at: {backup_path}",
                            "-i", os.path.expanduser("~/.config/Modus/assets/Icon/fuuka.png")
                        ])
                except Exception as e:
                    subprocess.run([
                        "notify-send", "Morgana - Backup",
                        f"Backup failed: {str(e)}",
                        "-i", os.path.expanduser("~/.config/Modus/assets/Icon/morgana.png")
                    ])

        checkbox.toggled.connect(on_toggled)
        copy_button.clicked.connect(on_copy_clicked)
        backup_button.clicked.connect(on_backup_clicked)

        container = QtWidgets.QWidget()
        container.setLayout(box)
        return container
