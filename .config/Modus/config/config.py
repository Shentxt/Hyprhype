import gi
import os
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from sections.enviroment import EnvSection
from sections.theme import ThemeSection
from sections.about import AboutSection 

class HyprConfGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configurations - Python Window")
        self.set_border_width(0)
        self.set_default_size(500, 450)
        self.set_resizable(True)
        self.set_decorated(False)
 
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_vbox)
          
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        main_vbox.pack_start(notebook, True, True, 0)

        env_page = EnvSection(True) 
        theme_page = ThemeSection(True)  
        about_page = AboutSection(True)

        notebook.append_page(env_page, Gtk.Label(label="Environment"))
        notebook.append_page(theme_page, Gtk.Label(label="Theme"))
        notebook.append_page(about_page, Gtk.Label(label="About")) 

    def on_close_button_clicked(self, widget):
        self.destroy() 

if __name__ == "__main__":
    window = HyprConfGUI()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
