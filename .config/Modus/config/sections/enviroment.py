import shutil
import gi
import os
import subprocess
from fabric.utils import get_relative_path

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

def create_separator():
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box.set_margin_start(20)
    box.set_margin_end(20)
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    box.pack_start(separator, True, True, 0)
    return box 

def backup(src, dest):
    if os.path.exists(dest):
        backup_path = dest + ".bak"
        if not os.path.exists(backup_path):
            try:
                shutil.move(dest, backup_path)
            except PermissionError:
                subprocess.run(f"sudo mv {dest} {backup_path}", shell=True, check=True)

def copy(src, dest):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)  
        else:
            shutil.copy(src, dest)  
    except PermissionError:
        if os.path.isdir(src):
            subprocess.run(f"sudo cp -r {src} {dest}", shell=True, check=True)
        else:
            subprocess.run(f"sudo cp {src} {dest}", shell=True, check=True)

class EnvSection(Gtk.Box):
    def __init__(self, show_enviroment: bool):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Font
        font_title = Pango.FontDescription("20")
        font_subtitle = Pango.FontDescription("8")

        general_label = Gtk.Label(label="Enviroments Settings")
        general_label.set_margin_top(20)
        general_label.override_font(font_title)
        self.pack_start(general_label, False, False, 0) 

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.pack_start(create_separator(), False, False, 10)
        
        #Tips
        tips_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tips_box.set_margin_start(20)

        tips_text_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        tips_icon = Gtk.Label(label="󱠂")  
        tips_icon.modify_font(Pango.FontDescription("20"))  

        tips_label = Gtk.Label(label=" Check the box to restart your configuration")
        tips_label.set_margin_bottom(2)  

        tips_text_box.pack_start(tips_icon, False, False, 0)
        tips_text_box.pack_start(tips_label, False, False, 0)

        tips_box.pack_start(tips_text_box, False, False, 0)

        self.pack_start(tips_box, False, False, 0)

        # Content 
        # Hypr  
        self.hypr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.hypr_box.set_margin_start(20)  
        self.hypr_box.set_margin_end(20)  
        self.pack_start(self.hypr_box, False, False, 0)

        # Extra  
        self.ex_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10) 
        self.ex_box.set_margin_start(20) 
        self.ex_box.set_margin_end(20) 
        self.pack_start(self.ex_box, False, False, 0)

        # Create all config sections
        self.create_config_sections()
    
    def create_config_section(self, name, config_file, dest_path, is_directory=False):
        """Helper function to create a consistent config section"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        checkbox = Gtk.CheckButton(label=f" {name}")
        checkbox.set_margin_bottom(4)
        checkbox.set_active(False)
        box.pack_start(checkbox, False, False, 0)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10) 

        copy_button = Gtk.Button(label="Copy")
        backup_button = Gtk.Button(label="Backup")

        button_box.pack_start(copy_button, False, False, 0)
        button_box.pack_start(backup_button, False, False, 0)  
        
        button_box.set_visible(False)
        box.pack_start(button_box, False, False, 0)

        #Callback functions
        def on_toggled(checkbox):
            button_box.set_visible(checkbox.get_active()) 
        
        def on_copy_clicked(button): 
            if checkbox.get_active():  
                src = os.path.expanduser(f"~/.config/Modus/config/config/{config_file}") 
                dest = os.path.expanduser(dest_path) 
                try: 
                    if is_directory: 
                        shutil.copytree(src, dest, dirs_exist_ok=True) 
                    else: 
                        shutil.copy(src, dest)  
                        subprocess.run(["notify-send","Fuuka - Copy",f"Successfully: {dest}","-i",os.path.expanduser("~/.config/Modus/assets/Icon/fuuka.png")])
                        if name == "Hyprland": 
                            subprocess.run(["hyprctl", "reload"], check=True) 
                except Exception as e: 
                    subprocess.run(["notify-send","Morgana - Copy",f"failed: {str(e)}","-i",os.path.expanduser("~/.config/Modus/assets/Icon/morgana.png")])
                   
        def on_backup_clicked(button): 
            if checkbox.get_active(): 
                src = os.path.expanduser(dest_path)  
                backup_path = src + ".bak"
                try: 
                    if os.path.exists(src): 
                        shutil.move(src, backup_path)  
                        subprocess.run(["notify-send","Fuuka - Backup",f"Successfully: {backup_path}","-i",os.path.expanduser("~/.config/Modus/assets/Icon/fuuka.png")])
                except Exception as e:  
                    subprocess.run(["notify-send","Morgana - Backup",f"Failed: {srt(e)}","-i",os.path.expanduser("~/.config/Modus/assets/Icon/morgana.png")])

        # Connect signals
        checkbox.connect("toggled", on_toggled)
        copy_button.connect("clicked", on_copy_clicked)
        backup_button.connect("clicked", on_backup_clicked)
        
        return box

    def create_config_sections(self):
        """Create and add all configuration sections"""
        sections = [
            # (name, config_file, dest_path, is_directory)
            ("Hyprland", "hyprland.conf", "~/.config/hypr/hyprland.conf"),
            ("Hypridle", "hypridle.conf", "~/.config/hypr/hypridle.conf"),
            ("Hyprlock", "hyprlock.conf", "~/.config/hypr/hyprlock.conf"),
            ("Kitty", "kitty.conf", "~/.config/kitty/kitty.conf"),
            ("Neovim", "nvim", "~/.config/nvim", True),
            ("Ly", "config.ini", "/etc/ly/config.ini"),
        ]

        for i, section in enumerate(sections):
            config_section = self.create_config_section(*section)
            if i < 3:  # First 3 go to hypr_box
                self.hypr_box.pack_start(config_section, False, False, 0)
            else:       # Others go to ex_box
                self.ex_box.pack_start(config_section, False, False, 0)

        self.pack_start(create_separator(), False, False, 10)
