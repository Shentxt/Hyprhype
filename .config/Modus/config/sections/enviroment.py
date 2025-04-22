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
                subprocess.run(["bash", "-c", f'notify-send "Backup" "Backup created successfully at {backup_path}" -i ~/.config/Modus/assets/Icon/futaba.png'])
            except PermissionError:
                subprocess.run(f"sudo mv {dest} {backup_path}", shell=True, check=True)
                subprocess.run(["bash", "-c", f'notify-send "Backup" "Backup created successfully at {backup_path}" -i ~/.config/Modus/assets/Icon/futaba.png'])

def copy(src, dest):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)  # Si es un directorio
        else:
            shutil.copy(src, dest)  # Si es un archivo
        subprocess.run(["bash", "-c", f'notify-send "Copy" "Successfully copied to {dest}" -i ~/.config/Modus/assets/Icon/futaba.png'])
    except PermissionError:
        if os.path.isdir(src):
            subprocess.run(f"sudo cp -r {src} {dest}", shell=True, check=True)
        else:
            subprocess.run(f"sudo cp {src} {dest}", shell=True, check=True)
        subprocess.run(["bash", "-c", f'notify-send "Copy" "Successfully copied to {dest}" -i ~/.config/Modus/assets/Icon/futaba.png'])

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

        # Conten
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

        # Hypr  
        self.land_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2) 
        self.land_checkbox = Gtk.CheckButton(label=" Hyprland") 
        self.land_checkbox.set_margin_bottom(4) 
        self.land_checkbox.set_active(False) 
        self.land_box.pack_start(self.land_checkbox, False, False, 0)

        self.land_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10) 
        self.copy_button = Gtk.Button(label="Copy") 
        self.backup_button = Gtk.Button(label="Backup") 

        self.land_button_box.pack_start(self.copy_button, False, False, 0) 
        self.land_button_box.pack_start(self.backup_button, False, False, 0)  
        self.land_button_box.set_visible(False) 
        self.land_box.pack_start(self.land_button_box, False, False, 0) 

        def on_land_toggled(checkbox): 
            if checkbox.get_active(): 
                self.land_button_box.set_visible(True)
            else: 
                self.land_button_box.set_visible(False)  

        def on_copy_button_clicked(button): 
            if self.land_checkbox.get_active(): 
                src_land = os.path.expanduser("~/.config/Modus/config/config/hyprland.conf") 
                dest_land = os.path.expanduser("~/.config/hypr/hyprland.conf") 
                copy(src_land, dest_land)  
                subprocess.run(["hyprctl", "reload"], check=True) 

        def on_backup_button_clicked(button): 
            if self.land_checkbox.get_active(): 
                src_land = os.path.expanduser("~/.config/Modus/config/config/hyprland.conf") 
                dest_land = os.path.expanduser("~/.config/hypr/hyprland.conf") 
                backup(src_land, dest_land)  
                
        self.land_checkbox.connect("toggled", on_land_toggled) 
        self.copy_button.connect("clicked", on_copy_button_clicked) 
        self.backup_button.connect("clicked", on_backup_button_clicked) 
        self.hypr_box.pack_start(self.land_box, False, False, 0)
 
        # Idle   
        self.idle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  
        self.idle_checkbox = Gtk.CheckButton(label=" Hypridle")  
        self.idle_checkbox.set_margin_bottom(4)  
        self.idle_checkbox.set_active(False)  
        self.idle_box.pack_start(self.idle_checkbox, False, False, 0) 
        
        self.idle_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.idle_copy_button = Gtk.Button(label="Copy")  
        self.idle_backup_button = Gtk.Button(label="Backup")  

        self.idle_button_box.pack_start(self.idle_copy_button, False, False, 0)  
        self.idle_button_box.pack_start(self.idle_backup_button, False, False, 0)   
        self.idle_button_box.set_visible(False)  
        self.idle_box.pack_start(self.idle_button_box, False, False, 0) 

        def on_idle_toggled(checkbox):  
            if checkbox.get_active():  
                self.idle_button_box.set_visible(True)   
            else:  
                self.idle_button_box.set_visible(False)   

        def on_idle_copy_button_clicked(button):  
            if self.idle_checkbox.get_active():  
                src_idle = os.path.expanduser("~/.config/Modus/config/config/hypridle.conf")  
                dest_idle = os.path.expanduser("~/.config/hypr/hypridle.conf")  
                copy(src_idle, dest_idle)   

        def on_idle_backup_button_clicked(button):  
            if self.idle_checkbox.get_active():  
                src_idle = os.path.expanduser("~/.config/Modus/config/config/hypridle.conf")  
                dest_idle = os.path.expanduser("~/.config/hypr/hypridle.conf")  
                backup(src_idle, dest_idle)   

        self.idle_checkbox.connect("toggled", on_idle_toggled)  
        self.idle_copy_button.connect("clicked", on_idle_copy_button_clicked) 
        self.idle_backup_button.connect("clicked", on_idle_backup_button_clicked)  
        self.hypr_box.pack_start(self.idle_box, False, False, 0)  

        # Lock   
        self.lock_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  
        self.lock_checkbox = Gtk.CheckButton(label=" Hyprlock")  
        self.lock_checkbox.set_margin_bottom(4)  
        self.lock_checkbox.set_active(False)  
        self.lock_box.pack_start(self.lock_checkbox, False, False, 0) 
        self.lock_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.lock_copy_button = Gtk.Button(label="Copy")  
        self.lock_backup_button = Gtk.Button(label="Backup")  
        self.lock_button_box.pack_start(self.lock_copy_button, False, False, 0)  
        self.lock_button_box.pack_start(self.lock_backup_button, False, False, 0)   
        self.lock_button_box.set_visible(False)  
        self.lock_box.pack_start(self.lock_button_box, False, False, 0)  

        def on_lock_toggled(checkbox):  
            if checkbox.get_active():  
                self.lock_button_box.set_visible(True)   
            else:  
                self.lock_button_box.set_visible(False)   
        
        def on_lock_copy_button_clicked(button):  
            if self.lock_checkbox.get_active():  
                src_lock = os.path.expanduser("~/.config/Modus/config/config/hyprlock.conf")  
                dest_lock = os.path.expanduser("~/.config/hypr/hyprlock.conf")  
                copy(src_lock, dest_lock)   
        
        def on_lock_backup_button_clicked(button):  
            if self.lock_checkbox.get_active():  
                src_lock = os.path.expanduser("~/.config/Modus/config/config/hyprlock.conf")  
                dest_lock = os.path.expanduser("~/.config/hypr/hyprlock.conf")  
                backup(src_lock, dest_lock)   

        self.lock_checkbox.connect("toggled", on_lock_toggled)  
        self.lock_copy_button.connect("clicked", on_lock_copy_button_clicked)  
        self.lock_backup_button.connect("clicked", on_lock_backup_button_clicked)  
        self.hypr_box.pack_start(self.lock_box, False, False, 0)

        # Kitty   
        self.kitty_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  
        self.kitty_checkbox = Gtk.CheckButton(label=" Kitty")  
        self.kitty_checkbox.set_margin_bottom(4)  
        self.kitty_checkbox.set_active(False)  
        self.kitty_box.pack_start(self.kitty_checkbox, False, False, 0) 

        self.kitty_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.kitty_copy_button = Gtk.Button(label="Copy")  
        self.kitty_backup_button = Gtk.Button(label="Backup")  
        self.kitty_button_box.pack_start(self.kitty_copy_button, False, False, 0) 
        self.kitty_button_box.pack_start(self.kitty_backup_button, False, False, 0)  
        self.kitty_button_box.set_visible(False)  
        self.kitty_box.pack_start(self.kitty_button_box, False, False, 0) 

        def on_kitty_toggled(checkbox): 
            if checkbox.get_active(): 
                self.kitty_button_box.set_visible(True)  
            else: 
                self.kitty_button_box.set_visible(False)   

        def on_kitty_copy_button_clicked(button): 
            if self.kitty_checkbox.get_active(): 
                src_kitty = os.path.expanduser("~/.config/Modus/config/config/kitty.conf")  
                dest_kitty = os.path.expanduser("~/.config/kitty/kitty.conf")  
                copy(src_kitty, dest_kitty)   

        def on_kitty_backup_button_clicked(button):  
            if self.kitty_checkbox.get_active():  
                src_kitty = os.path.expanduser("~/.config/Modus/config/config/kitty.conf")  
                dest_kitty = os.path.expanduser("~/.config/kitty/kitty.conf")  
                backup(src_kitty, dest_kitty)   
                
        self.kitty_checkbox.connect("toggled", on_kitty_toggled)  
        self.kitty_copy_button.connect("clicked", on_kitty_copy_button_clicked)  
        self.kitty_backup_button.connect("clicked", on_kitty_backup_button_clicked)  
        self.ex_box.pack_start(self.kitty_box, False, False, 0)  

        # NVim   
        self.vi_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  
        self.vi_checkbox = Gtk.CheckButton(label=" Neovim")  
        self.vi_checkbox.set_margin_bottom(4)  
        self.vi_checkbox.set_active(False)  
        self.vi_box.pack_start(self.vi_checkbox, False, False, 0) 

        self.vi_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.vi_copy_button = Gtk.Button(label="Copy")  
        self.vi_backup_button = Gtk.Button(label="Backup")  

        self.vi_button_box.pack_start(self.vi_copy_button, False, False, 0)  
        self.vi_button_box.pack_start(self.vi_backup_button, False, False, 0)   
        self.vi_button_box.set_visible(False)  
        self.vi_box.pack_start(self.vi_button_box, False, False, 0) 

        def on_vi_toggled(checkbox):  
            if checkbox.get_active():  
                self.vi_button_box.set_visible(True)   
            else:  
                self.vi_button_box.set_visible(False)   

        def on_vi_copy_button_clicked(button): 
            if self.vi_checkbox.get_active(): 
                src_vi = os.path.expanduser("~/.config/Modus/config/config/nvim") 
                dest_vi = os.path.expanduser("~/.config/nvim") 
                copytree(src_vi, dest_vi)  

        def on_vi_backup_button_clicked(button): 
            if self.vi_checkbox.get_active(): 
                src_vi = os.path.expanduser("~/.config/Modus/config/config/nvim") 
                dest_vi = os.path.expanduser("~/.config/nvim") 
                backup(src_vi, dest_vi)  

        self.vi_checkbox.connect("toggled", on_vi_toggled) 
        self.vi_copy_button.connect("clicked", on_vi_copy_button_clicked) 
        self.vi_backup_button.connect("clicked", on_vi_backup_button_clicked) 
        self.ex_box.pack_start(self.vi_box, False, False, 0) 

        # Ly   
        self.ly_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  
        self.ly_checkbox = Gtk.CheckButton(label=" Ly")  
        self.ly_checkbox.set_margin_bottom(4)  
        self.ly_checkbox.set_active(False)  
        self.ly_box.pack_start(self.ly_checkbox, False, False, 0) 

        self.ly_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  
        self.ly_copy_button = Gtk.Button(label="Copy")  
        self.ly_backup_button = Gtk.Button(label="Backup")  

        self.ly_button_box.pack_start(self.ly_copy_button, False, False, 0)  
        self.ly_button_box.pack_start(self.ly_backup_button, False, False, 0)   
        self.ly_button_box.set_visible(False)  
        self.ly_box.pack_start(self.ly_button_box, False, False, 0)  
        
        def on_ly_toggled(checkbox):  
            if checkbox.get_active(): 
                self.ly_button_box.set_visible(True)  
            else: 
                self.ly_button_box.set_visible(False)  

        def on_ly_copy_button_clicked(button): 
            if self.ly_checkbox.get_active(): 
                src_ly = os.path.expanduser("~/.config/Modus/config/config/config.ini") 
                dest_ly = os.path.expanduser("/etc/ly/config.ini") 
                copy(src_ly, dest_ly)  

        def on_ly_backup_button_clicked(button): 
            if self.ly_checkbox.get_active(): 
                src_ly = os.path.expanduser("~/.config/Modus/config/config/config.ini") 
                dest_ly = os.path.expanduser("/etc/ly/config.ini") 
                backup(src_ly, dest_ly)  

        self.ly_checkbox.connect("toggled", on_ly_toggled) 
        self.ly_copy_button.connect("clicked", on_ly_copy_button_clicked) 
        self.ly_backup_button.connect("clicked", on_ly_backup_button_clicked) 
        self.ex_box.pack_start(self.ly_box, False, False, 0)

        self.pack_start(create_separator(), False, False, 10)   
