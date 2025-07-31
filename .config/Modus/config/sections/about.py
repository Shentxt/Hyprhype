import os
import platform
import subprocess
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

current_year = datetime.now().year

cpu_model = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | uniq | sed 's/model name\\s*:\\s*\\(.*\\) with Radeon Graphics/\\1/'")
ram_size = subprocess.getoutput("free -h | awk '/^Mem:/ {print $2}' | cut -d' ' -f1")
ram_type = subprocess.getoutput("sudo dmidecode -t 17 | grep 'Type' | head -n 1 | awk -F: '{print $2}' | sed 's/^ *//'")

def get_system_info():
    return [
        f"╭────────────  Enviroments ───────────",
        f"│─   Hostname: {platform.node()}",
        f"│─   Distribución: {subprocess.getoutput('source /etc/os-release && echo $NAME $VERSION')}",
        f"│─   Kernel: {platform.release()}",
        f"│────────────  Hadware ────────────",
        f"│─󰍛  Architecture: {platform.architecture()[0]}",
        f"│─󰍛  RAM: {ram_size} ({ram_type})",
        f"│─󰍛  CPU: {cpu_model}",
        f"│─  GPU: {subprocess.getoutput('lspci | grep -E \"VGA|3D\" | awk -F: \'{print $2}\' | cut -d\' \' -f1-3')}",
        f"╰──────────────────────────────────",
    ]

def create_separator():
    sep = QtWidgets.QFrame()
    sep.setFrameShape(QtWidgets.QFrame.HLine)
    sep.setFrameShadow(QtWidgets.QFrame.Sunken)
    sep.setStyleSheet("margin-left: 20px; margin-right: 20px;")
    return sep

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

class AboutSection(QtWidgets.QWidget):
    def __init__(self, show_about=True):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("About Settings")
        title.setStyleSheet("font-size: 20pt; margin-top: 20px;")
        title.setAlignment(QtCore.Qt.AlignCenter) 
        layout.addWidget(title)

        layout.addWidget(create_separator())

        # Image and Date
        hbox = QtWidgets.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignTop)

        # Imagen
        image_box = QtWidgets.QVBoxLayout()
        image_box.setContentsMargins(40, 0, 0, 0)
        image_path = os.path.expanduser("~/.config/Modus/assets/Icon/about.jpg")
        
        pixmap = create_rounded_avatar(image_path, size=200, radius=30)
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(pixmap) 
        
        image_label.setFixedSize(200, 200)
        image_box.addWidget(image_label)
        hbox.addLayout(image_box)

        # Info System
        info_box = QtWidgets.QVBoxLayout()
        info_box.setAlignment(QtCore.Qt.AlignTop)

        for info in get_system_info():
            label = QtWidgets.QLabel(info)
            label.setAlignment(QtCore.Qt.AlignLeft)
            info_box.addWidget(label)
        hbox.addLayout(info_box)

        layout.addLayout(hbox)
        layout.addWidget(create_separator())

        # Footer copyright
        footer_box = QtWidgets.QVBoxLayout()
        footer_box.setAlignment(QtCore.Qt.AlignCenter)

        name_label = QtWidgets.QLabel("Shen")
        name_label.setStyleSheet("margin-bottom: 2px;")
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        footer_box.addWidget(name_label)

        copyright_label = QtWidgets.QLabel(f"© Copyright 2024-{current_year}")
        copyright_label.setStyleSheet("font-size: 8pt; margin-bottom: 5px;")
        footer_box.addWidget(copyright_label)

        layout.addLayout(footer_box)
