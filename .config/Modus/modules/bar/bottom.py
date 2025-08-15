from typing import Literal
from fabric.widgets.shapes import Corner
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GLib 

from modules.bar.components import (
    Dock,
)

class StatusBarCorner(Box):
    def __init__(self, corner: Literal["bottom-right", "bottom-left"]):
        super().__init__(
            style="margin-top: 15px;",
            name="bar-corner",
            children=Corner(
                orientation=corner,
                size=15,
            ),
        )

class Bottom(Window):
    def __init__(self):
        self.dock = Dock()
        self.bar_content = CenterBox(name="center-bar")

        self.bar_content.end_children = [
            StatusBarCorner("bottom-right"),
            Box(
                name="bot",
                spacing=4,
                children=[],
                style_classes="end-container",
            ),
        ]

        self.bar_content.center_children = [
            StatusBarCorner("bottom-right"),
            Box(
                name="bot",
                spacing=4,
                children=[
                    self.dock,
                ],  
                style_classes="center-container",
            ),
            StatusBarCorner("bottom-left"),
        ]

        self.bar_content.start_children = [
            Box(
                name="bot",
                spacing=4,
                children=[],  
                style_classes="start-container",
            ),
            StatusBarCorner("bottom-left"),
        ]

        super().__init__(
            layer="top",
            anchor="left bottom right",  
            exclusivity="auto",
            visible=True,
            child=self.bar_content,
        )
        self.hidden = False

    def toggle_hidden(self):
        self.hidden = not self.hidden
        if self.hidden:
            self.bar_content.add_style_class("hidden")
            self.bar_content.remove_style_class("visible")
            self.set_property("visible", False)
        else:
            self.bar_content.add_style_class("visible")
            self.bar_content.remove_style_class("hidden")
            self.set_property("visible", True)

    def toggle_center_hidden(self):
        center_container = self.bar_content.get_child_by_name("bar")
        if center_container.has_style_class("hidden"):
            center_container.remove_style_class("hidden")
            center_container.add_style_class("visible")
            center_container.set_property("visible", True)
        else:
            center_container.add_style_class("hidden")
            center_container.remove_style_class("visible")
            center_container.set_property("visible", False)

class ScreenCorners(Window):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="bottom left right top",
            pass_through=True,
            child=Box(
                orientation="vertical",
                children=[
                    Box(
                        children=[
                            self.make_corner("bottom-left"),
                            Box(h_expand=True),
                            self.make_corner("bottom-right"),
                        ]
                    ),
                    Box(v_expand=True),
                    Box(
                        children=[
                            self.make_corner("top-left"),
                            Box(h_expand=True),
                            self.make_corner("top-right"),
                        ]
                    ),
                ],
            ),
        )

    def make_corner(self, orientation) -> Box:
        return Box(
            h_expand=False,
            v_expand=False,
            name="bar-corner",
            children=Corner(
                orientation=orientation,
                size=45,
            ),
        )
