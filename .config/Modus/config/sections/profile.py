import os
import subprocess
import shutil
import socket
from PyQt5 import QtWidgets, QtGui, QtCore

CONFIG_DIR = os.path.expanduser("~/.config/Modus")
WALLPAPERS_DIR_DEFAULT = os.path.expanduser("~/.config/Modus/assets/wallpaper")
FACE_PATH = os.path.expanduser("~/.face")
username = subprocess.check_output("whoami", shell=True).decode().strip()
hostname = socket.gethostname()

def create_separator():
    line = QtWidgets.QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setStyleSheet("margin-left: 2px; margin-right: 2px;")
    return line

def create_rounded_avatar(image_path, size=100, radius=20):
    original = QtGui.QPixmap(image_path).scaled(size, size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
    rounded = QtGui.QPixmap(size, size)
    rounded.fill(QtCore.Qt.transparent)  

    painter = QtGui.QPainter(rounded)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
    path = QtGui.QPainterPath()
    path.addRoundedRect(0, 0, size, size, radius, radius)
    painter.setClipPath(path)

    painter.drawPixmap(0, 0, original)
    painter.end()

    return rounded

class ProfileSection(QtWidgets.QWidget):
    def __init__(self, show_theme=True):
        super().__init__() 
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QtWidgets.QLabel("Profile Settings")
        title.setStyleSheet("font-size: 20pt;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFixedHeight(55)
        layout.addWidget(title)
        layout.addWidget(create_separator())

        font_title = QtGui.QFont()
        font_title.setPointSize(20)
        font_subtitle = QtGui.QFont()
        font_subtitle.setPointSize(8) 
        
        user_image_box = QtWidgets.QHBoxLayout()
        user_image_box.setContentsMargins(200, 0, 100, 20)
        user_image_box.setSpacing(10)

        avatar_pixmap = create_rounded_avatar(FACE_PATH)
        avatar_label = QtWidgets.QLabel()
        avatar_label.setPixmap(avatar_pixmap)
        avatar_label.setFixedSize(100, 100)

        user_text_layout = QtWidgets.QVBoxLayout() 
        user_text_layout.setSpacing(0)
        user_text_layout.setContentsMargins(0, 70, 0, 0)

        user_label = QtWidgets.QLabel(username) 
        user_label.setFont(font_title)
        user_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft) 

        hostname_label = QtWidgets.QLabel(hostname)
        hostname_label.setFont(font_subtitle)
        #hostname_label.setSpacing(0)
        hostname_label.setContentsMargins(0, 0, 0, 80)
        hostname_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
   
        user_label.setAlignment(QtCore.Qt.AlignCenter)
        hostname_label.setAlignment(QtCore.Qt.AlignCenter)
        
        user_text_layout.addWidget(user_label)
        user_text_layout.addWidget(hostname_label)

        user_image_box.addWidget(avatar_label)
        user_image_box.addLayout(user_text_layout)
        user_image_box.addStretch()

        layout.addLayout(user_image_box)

        face_box = QtWidgets.QHBoxLayout()
        face_box.setContentsMargins(20, 0, 20, 0)
        face_box.setSpacing(5)

        face_text_box = QtWidgets.QVBoxLayout()
        face_label = QtWidgets.QLabel("Avatar")
        face_label.setAlignment(QtCore.Qt.AlignLeft)
        face_label.setContentsMargins(0, 0, 0, 2)

        face_subtitle = QtWidgets.QLabel("the image is automatically updated")
        face_subtitle.setAlignment(QtCore.Qt.AlignLeft)
        face_subtitle.setFont(font_subtitle)
        face_subtitle.setContentsMargins(0, 0, 0, 5)

        face_text_box.addWidget(face_label)
        face_text_box.addWidget(face_subtitle)

        self.face_chooser = QtWidgets.QPushButton("Select Image")
        self.face_chooser.clicked.connect(self.open_face_chooser)

        face_box.addLayout(face_text_box)
        face_box.addWidget(self.face_chooser)

        layout.addLayout(face_box)
        layout.addWidget(create_separator())

        wall_box = QtWidgets.QHBoxLayout()
        wall_box.setContentsMargins(20, 0, 20, 0)
        wall_box.setSpacing(10)

        wall_text_box = QtWidgets.QVBoxLayout()
        wall_label = QtWidgets.QLabel("Wallpapers Directory")
        wall_label.setAlignment(QtCore.Qt.AlignLeft)
        wall_label.setContentsMargins(0, 0, 0, 2)

        wall_subtitle = QtWidgets.QLabel("the button left copies a default directory")
        wall_subtitle.setAlignment(QtCore.Qt.AlignLeft)
        wall_subtitle.setFont(font_subtitle)
        wall_subtitle.setContentsMargins(0, 0, 0, 5)

        wall_text_box.addWidget(wall_label)
        wall_text_box.addWidget(wall_subtitle)

        self.wall_dir_chooser = QtWidgets.QPushButton(os.path.basename(WALLPAPERS_DIR_DEFAULT.rstrip("/")))
        self.wall_dir_chooser.clicked.connect(self.open_wall_dir_chooser)

        self.copy_button = QtWidgets.QPushButton("Copy")
        self.copy_button.setContentsMargins(0, 0, 20, 0)
        self.copy_button.clicked.connect(self.on_copy_wallpapers_clicked)

        wall_box.addLayout(wall_text_box)
        wall_box.addWidget(self.wall_dir_chooser)
        wall_box.addWidget(self.copy_button)

        layout.addLayout(wall_box)
        self.selected_wall_dir = WALLPAPERS_DIR_DEFAULT

    def open_face_chooser(self):
        dialog = QtWidgets.QFileDialog(self, "Select an image")
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_():
            selected_file = dialog.selectedFiles()[0]
            if selected_file:
                shutil.copy(selected_file, FACE_PATH)
                subprocess.run(["pkill", "gnome-shell"])
                avatar_pixmap = create_rounded_avatar(FACE_PATH)
                self.update_avatar(avatar_pixmap)

    def update_avatar(self, pixmap):
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, QtWidgets.QLabel) and widget.pixmap():
                        widget.setPixmap(pixmap)
                        return

    def open_wall_dir_chooser(self):
        dialog = QtWidgets.QFileDialog(self, "Select a folder")
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            folder = dialog.selectedFiles()[0]
            self.selected_wall_dir = folder
            folder_name = os.path.basename(folder.rstrip("/"))
            self.wall_dir_chooser.setText(folder_name)

    def on_copy_wallpapers_clicked(self):
        selected_dir = self.selected_wall_dir
        if not selected_dir or not os.path.exists(selected_dir):
            selected_dir = WALLPAPERS_DIR_DEFAULT
        self.copy_wallpapers(selected_dir)
        subprocess.run([
            "notify-send", "Ann - WallCopy",
            f"Successfully copied to: {selected_dir}",
            "-i", os.path.expanduser("~/.config/Modus/assets/Icon/ann.png")
        ])

    def copy_wallpapers(self, dest_wallpaper_dir):
        src_wallpaper_dir = os.path.expanduser("~/.config/Modus/assets/wallpaper")
        if not any(folder in dest_wallpaper_dir.lower() for folder in ['wallpaper', 'images']):
            if not os.path.exists(dest_wallpaper_dir):
                os.makedirs(dest_wallpaper_dir)
            shutil.copytree(src_wallpaper_dir, os.path.join(dest_wallpaper_dir, "wallpaper"), dirs_exist_ok=True)
            subprocess.run([
                "python",
                os.path.expanduser("~/.config/Modus/config/scripts/wallpaper.py"),
                "-I",
                os.path.join(dest_wallpaper_dir, "wallpaper", "example-1.jpg"),
            ])
