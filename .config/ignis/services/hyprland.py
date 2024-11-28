from ignis.utils import Utils  # noqa: E402

def rgba(color: str) -> str:
    hex_color = color.lstrip("#")
    return f"rgba({int(hex_color[:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:], 16)}, 1)"

def send_batch(batch: list[str]):
    for command in batch:
        try:
            Utils.exec_sh(f"hyprctl dispatch {command}")
        except Exception:
            pass

def setup_hyprland(width: str, wm_gaps: int, active1: str, active2: str, inactive1: str, inactive2: str, radius: int, shadows: bool, blur: float):
    commands = [
        f"general:border_size {width}",
        f"general:gaps_out {wm_gaps}",
        f"general:gaps_in {wm_gaps // 4}",
        f"general:col.active_border {rgba(active1)} {rgba(active2)}",
        f"general:col.inactive_border {rgba(inactive1)} {rgba(inactive2)}",
        f"decoration:rounding {radius}",
        f"decoration:drop_shadow {'yes' if shadows else 'no'}",
        f"dwindle:no_gaps_when_only 0",
        f"master:no_gaps_when_only 0",
    ]
    send_batch(commands)

    if blur > 0:
        blur_commands = [
            "layerrule unset, example_app",
            "layerrule blur, example_app",
            "layerrule ignorealpha 0.2, example_app",
        ]
        send_batch(blur_commands)

    def update_border_colors():
        while True:
            send_batch([
                f"general:col.active_border {rgba(active1)} {rgba(active2)}",
                f"general:col.inactive_border {rgba(inactive1)} {rgba(inactive2)}"
            ])
            time.sleep(2.3)

    update_border_colors()

def main():
    width = "2"
    wm_gaps = 5
    active1 = "#ff0000"
    active2 = "#00ff00"
    inactive1 = "#cccccc"
    inactive2 = "#444444"
    radius = 10
    shadows = True
    blur = 0.5

    setup_hyprland(width, wm_gaps, active1, active2, inactive1, inactive2, radius, shadows, blur)

if __name__ == "__main__":
    main()
