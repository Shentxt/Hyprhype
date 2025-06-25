import re
from fabric.hyprland.widgets import ActiveWindow
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box

from utils.windowstitle import WINDOW_TITLE_MAP

class WindowTitleWidget(Box):
    """A widget that displays the title of the active window."""

    def __init__(self, **kwargs):
        super().__init__(name="window-box", **kwargs)

        self.config = {
            "truncation": True,
            "truncation_size": 80,
            "title_map": [],
            "enable_icon": True,
        }

        self.box = Box()
        self.children = (self.box,)

        self.window = ActiveWindow(
            name="window",
            formatter=FormattedString(
                "{ get_title(win_title, win_class) }",
                get_title=self.get_title,
            ),
        )

        self.box.children = (self.window,)

    def get_title(self, win_title, win_class):
        win_title = (
            truncate(win_title, self.config["truncation_size"])
            if self.config["truncation"]
            else win_title
        )

        merged_titles = self.config["title_map"] + WINDOW_TITLE_MAP

        matched_window = next(
            (wt for wt in merged_titles if re.search(wt[0], win_class.lower())),
            None,
        )

        if matched_window is None:
            return f"  {win_class.lower()}"

        return (
             f"{matched_window[1]}  {matched_window[2]}"  
             if self.config["enable_icon"] 
             else f"{matched_window[2]}" 
         )
