import gi
import os
import subprocess
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Pango, Gdk
import cairo

CONFIG_DIR = os.path.expanduser("~/.config/Modus")
WALLPAPERS_DIR_DEFAULT = os.path.expanduser("~/.config/Modus/assets/wallpaper")
FACE_PATH = os.path.expanduser("~/.face")
username = subprocess.check_output("whoami", shell=True).decode().strip()

def create_separator():
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    box.set_margin_start(20)
    box.set_margin_end(20)
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    box.pack_start(separator, True, True, 0)
    return box 

def create_rounded_square_pixbuf(pixbuf, size=100, corner_radius=20):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)

    ctx.set_line_width(1)
    ctx.set_source_rgba(0, 0, 0, 0)     
    ctx.move_to(corner_radius, 0)
    ctx.line_to(size - corner_radius, 0)
    ctx.arc(size - corner_radius, corner_radius, corner_radius, 3 * 3.1416 / 2, 0)
    ctx.line_to(size, size - corner_radius)
    ctx.arc(size - corner_radius, size - corner_radius, corner_radius, 0, 3.1416 / 2)
    ctx.line_to(corner_radius, size)
    ctx.arc(corner_radius, size - corner_radius, corner_radius, 3.1416 / 2, 3.1416)
    ctx.line_to(0, corner_radius)
    ctx.arc(corner_radius, corner_radius, corner_radius, 3.1416, 2 * 3.1416)
    ctx.close_path()

    ctx.clip()

    Gdk.cairo_set_source_pixbuf(ctx, pixbuf, 0, 0)
    ctx.paint()

    return Gdk.pixbuf_get_from_surface(surface, 0, 0, size, size)

class ThemeSection(Gtk.Box):
    def __init__(self, show_theme: bool):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Fonts
        font_title = Pango.FontDescription("20")
        font_subtitle = Pango.FontDescription("8")
        
        general_label = Gtk.Label(label="Theme Settings")
        general_label.set_margin_top(20)
        general_label.modify_font(font_title)
        self.pack_start(general_label, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10) 

        self.pack_start(create_separator(), False, False, 10)   

        # User Preview
        user_image_box = Gtk.Box(spacing=2)
        user_image_box.set_margin_start(200)
        user_image_box.set_margin_bottom(20)
        user_image_box.set_margin_end(100)
        face_image_path = os.path.expanduser("~/.face")
 
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(face_image_path)
        pixbuf = pixbuf.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
        rounded_pixbuf = create_rounded_square_pixbuf(pixbuf)
        user_image = Gtk.Image.new_from_pixbuf(rounded_pixbuf)

        user_label = Gtk.Label(label=username)
        user_label.modify_font(font_title)
        user_label.set_margin_start(20)
        user_image_box.pack_start(user_image, False, False, 0)
        user_image_box.pack_start(user_label, False, False, 0)

        self.pack_start(user_image_box, False, False, 0) 

        # Icon  
        face_box = Gtk.Box(spacing=10)  
        face_box.set_margin_start(20)
        face_box.set_margin_end(20)

        face_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        face_label = Gtk.Label(label="Avatar")
        face_label.set_xalign(0) 
        face_label.set_margin_bottom(2)
        face_text_box.pack_start(face_label, False, False, 0) 
        
        face_subtitle = Gtk.Label(label="the image is automatically updated")
        face_subtitle.set_xalign(0)
        face_subtitle.modify_font(font_subtitle)
        face_subtitle.set_margin_bottom(5)
        face_text_box.pack_start(face_subtitle, False, False, 0)

        face_box.pack_start(face_text_box, False, False, 0) 
       
        self.face_chooser = Gtk.FileChooserButton(
            title="Select an image", action=Gtk.FileChooserAction.OPEN
        )
        
        self.face_chooser.set_filename(FACE_PATH)
        
        face_box.pack_start(self.face_chooser, True, True, 0)
        self.face_chooser.connect("file-set", self.on_face_selected)

        self.pack_start(face_box, False, False, 0)
 
        self.pack_start(create_separator(), False, False, 10)  

        # Wallpaper
        wall_box = Gtk.Box(spacing=10) 
        wall_box.set_margin_start(20)

        wall_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        wall_label = Gtk.Label(label="Wallpapers Directory")
        wall_label.set_xalign(0) 
        wall_label.set_margin_bottom(2)
        wall_text_box.pack_start(wall_label, False, False, 0) 
        
        wall_subtitle = Gtk.Label(label="the button left copies a default directory")
        wall_subtitle.set_xalign(0)
        wall_subtitle.modify_font(font_subtitle)
        wall_subtitle.set_margin_bottom(5)
        wall_text_box.pack_start(wall_subtitle, False, False, 0)

        wall_box.pack_start(wall_text_box, False, False, 0)  
        
        self.wall_dir_chooser = Gtk.FileChooserButton(
            title="Select a folder", action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        
        self.wall_dir_chooser.set_filename(WALLPAPERS_DIR_DEFAULT)
        
        wall_box.pack_start(self.wall_dir_chooser, True, True, 0)
        hbox.pack_start(wall_box, True, True, 0)
      
        # Copy Wallpaper file
        self.copy_button = Gtk.Button(label="Copy  ")
        self.copy_button.set_margin_end(20)

        self.copy_button.set_image_position(Gtk.PositionType.LEFT)        
        self.copy_button.connect("clicked", self.on_copy_wallpapers_clicked)
        hbox.pack_start(self.copy_button, False, False, 0)

        self.pack_start(hbox, False, False, 0) 


    # def 
    def on_copy_wallpapers_clicked(self, widget):
        selected_dir = self.wall_dir_chooser.get_filename()
        
        if not selected_dir or not os.path.exists(selected_dir):
            selected_dir = WALLPAPERS_DIR_DEFAULT
        self.copy_wallpapers(selected_dir)
        subprocess.run(["bash", "-c", f'notify-send "Copy" "Successfully copied to {WALLPAPERS_DIR_DEFAULT}" -i ~/.config/Modus/assets/Icon/futaba.png']) 


    def copy_wallpapers(self, selected_dir):
        dest_wallpaper_dir = selected_dir
        src_wallpaper_dir = os.path.expanduser("~/.config/Modus/assets/wallpaper")
        
        if not any(folder in dest_wallpaper_dir.lower() for folder in ['wallpaper', 'images']):
            if not os.path.exists(dest_wallpaper_dir):
                os.makedirs(dest_wallpaper_dir) 
            
            shutil.copytree(src_wallpaper_dir, os.path.join(dest_wallpaper_dir, "wallpaper"), dirs_exist_ok=True)
            
            subprocess.run(
                [
                    "python",
                    os.path.expanduser("~/.config/Modus/config/scripts/wallpaper.py"),
                    "-I",
                    os.path.join(dest_wallpaper_dir, "wallpaper", "example-1.jpg"),
                ]
            ) 

    def on_face_selected(self, widget):
        selected_file = self.face_chooser.get_filename()

        if selected_file:
            shutil.copy(selected_file, FACE_PATH)
            subprocess.run(["pkill", "gnome-shell"])
