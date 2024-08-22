import type Gtk from "gi://Gtk?version=3.0"
import { Media } from "../quicksettings/widgets/Media"
import PopupWindow from "widget/PopupWindow"
import options from "options"

const media = (await Service.import("mpris")).bind("players")

const { bar, datemenu, quicksettings } = options
const pos = bar.position.bind()
const layout = Utils.derive([bar.position, datemenu.position], (bar, qs) =>
    `${bar}-${qs}` as const,
);

const updateSettings = () => Widget.Box({
    vertical: true,
    class_name: "quicksettings vertical",
    css: quicksettings.width.bind().as(w => `min-width: ${w}px;`),
    children: [
        Widget.Box({
            class_name: "sliders-box vertical",
            vertical: true,
            children: [
                Media(),
            ],
        }),
    ],
})

const MediaWindow = () => PopupWindow({
    name: "media",
    exclusivity: "exclusive",
    transition: pos.as(pos => pos === "top" ? "slide_down" : "slide_up"),
    layout: layout.value,
    child: updateSettings()
});

export function setupMediaWindow() {
    App.addWindow(MediaWindow());
    layout.connect("changed", () => {
        App.removeWindow("media");
        App.addWindow(MediaWindow());
    });
}
