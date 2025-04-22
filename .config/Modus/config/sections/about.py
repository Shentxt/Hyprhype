import gi
import os
import platform
import subprocess
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Pango

current_year = datetime.now().year

cpu_model = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | uniq | sed 's/model name\\s*:\\s*\\(.*\\) with Radeon Graphics/\\1/'")
ram_size = subprocess.getoutput("free -h | awk '/^Mem:/ {print $2}' | cut -d' ' -f1")
ram_type = subprocess.getoutput("sudo dmidecode -t 17 | grep 'Type' | head -n 1 | awk -F: '{print $2}' | sed 's/^ *//'")

def create_separator():
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box.set_margin_start(20)
    box.set_margin_end(20)
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    box.pack_start(separator, True, True, 0)
    return box   

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
        f"│─  GPU: {subprocess.getoutput('lspci | grep -E "VGA|3D" | awk -F: \'{print $2}\' | cut -d\' \' -f1-3')}",
        f"╰──────────────────────────────────",
        
    ]

class AboutSection(Gtk.Box):
    def __init__(self, show_about: bool):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Font
        font_title = Pango.FontDescription("20")
        font_subtitle = Pango.FontDescription("8")

        general_label = Gtk.Label(label="About Settings")
        general_label.set_margin_top(20)
        general_label.override_font(font_title)
        self.pack_start(general_label, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.pack_start(create_separator(), False, False, 10)
        
        self.pack_start(hbox, False, False, 10)

        # System Logo
        user_image_box = Gtk.Box()
        face_image_path = os.path.expanduser("~/.config/Modus/assets/Icon/about.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(face_image_path, 200, 200, True)

        user_image = Gtk.Image.new_from_pixbuf(pixbuf)
        user_image_box.pack_start(user_image, False, False, 0)

        # System Informations
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        system_info = get_system_info()
        
        for info in system_info:
            label = Gtk.Label(label=info)
            label.set_xalign(0)
            info_box.pack_start(label, False, False, 0)

        hbox.pack_start(user_image_box, False, False, 0)
        hbox.pack_start(info_box, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.pack_start(create_separator(), False, False, 10)

        #Box
        cp_box = Gtk.Box(spacing=10) 
        cp_box.set_halign(Gtk.Align.CENTER)

        cp_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        cp_text_box.set_halign(Gtk.Align.CENTER) 
        
        #Title
        cp_label = Gtk.Label(label="Shen")
        cp_label.set_margin_bottom(2)
        cp_text_box.pack_start(cp_label, False, False, 0) 
        
        #Subtitle
        cp_subtitle = Gtk.Label(label=f"© Copyright {current_year}")
        cp_subtitle.modify_font(font_subtitle)
        cp_subtitle.set_margin_bottom(5)
        cp_text_box.pack_start(cp_subtitle, False, False, 0)

        cp_box.pack_start(cp_text_box, False, False, 0)   
        self.pack_start(cp_box, False, False, 0)

