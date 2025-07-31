from sections.theme import ThemeSection
from sections.keys import KeybindSection
from sections.enviroment import EnvSection
from sections.profile import ProfileSection
from sections.about import AboutSection

import sys
import os
import re 
from PyQt5 import QtWidgets, QtCore 

utils_path = os.path.expanduser("~/.config/Modus/utils")
sys.path.append(utils_path)

from qess import load_compiled_qss

class HyprConfGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  
        qss = load_compiled_qss("config")
        self.setStyleSheet(qss)
                
        self.setWindowTitle("Configurations - Python Window")
        self.setFixedSize(800, 450)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.Window)
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.tab_list = QtWidgets.QListWidget()
        self.tab_list.setFixedWidth(150)
        self.tab_list.setSpacing(10)
        self.tab_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tab_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.tab_list.addItem("󰢵   Theme")
        self.tab_list.addItem("   Keybind")
        self.tab_list.addItem("   Presets")
        self.tab_list.addItem("   Profile")
        self.tab_list.addItem("   About")

        main_layout.addWidget(self.tab_list)

        self.pages = QtWidgets.QStackedWidget()
        main_layout.addWidget(self.pages)
        
        theme_page = ThemeSection()
        keybind_page = KeybindSection()
        env_page = EnvSection() 
        profile_page = ProfileSection() 
        about_page = AboutSection() 

        self.pages.addWidget(theme_page)
        self.pages.addWidget(keybind_page)
        self.pages.addWidget(env_page)
        self.pages.addWidget(profile_page)
        self.pages.addWidget(about_page)
        
        cache_config_dir = os.path.expanduser("~/.cache/modus")
        os.makedirs(cache_config_dir, exist_ok=True)
        settings_path = os.path.join(cache_config_dir, "config.ini")

        self.settings = QtCore.QSettings(settings_path, QtCore.QSettings.IniFormat)
        self.tab_list.currentRowChanged.connect(self.save_last_tab)
        
        last_tab = self.settings.value("last_tab_index", 0, type=int)
        self.tab_list.setCurrentRow(last_tab)
        self.pages.setCurrentIndex(last_tab)

        self.tab_list.currentRowChanged.connect(self.pages.setCurrentIndex)

    def save_last_tab(self, index):
        self.settings.setValue("last_tab_index", index) 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HyprConfGUI()
    window.show()
    sys.exit(app.exec_())
