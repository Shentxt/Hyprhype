from ignis.widgets import Widget
from ignis.utils import Utils

def on_date_selected(calendar):
    day, month, year = calendar.get_date()
    Utils.notify(f"Selected date: {day}/{month + 1}/{year}")

def calendar():
    calendar = Widget.Calendar(
        css_classes=["date-center"],
        show_day_names=True,
        show_heading=True,
        show_week_numbers=False,
    )

    calendar.connect("day-selected", on_date_selected)

    return calendar
