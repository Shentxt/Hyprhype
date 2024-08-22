import type Gtk from "gi://Gtk?version=3.0";
import { ProfileSelector, ProfileToggle } from "./widgets/PowerProfile";
import { Header } from "./widgets/Header";
import { Volume, Microphone, SinkSelector, AppMixer } from "./widgets/Volume";
import { Brightness } from "./widgets/Brightness";
import { NetworkToggle, WifiSelection } from "./widgets/Network";
import { BluetoothToggle, BluetoothDevices } from "./widgets/Bluetooth";
import { DND } from "./widgets/DND";
import { DarkModeToggle } from "./widgets/DarkMode";
import { MicMute } from "./widgets/MicMute";
import { Media } from "./widgets/Media";
import { UpdateWidget } from "./widgets/Update";
import { ScreenshotToggle, ScreenshotMenu } from "./widgets/Screenshot";
import PopupWindow from "widget/PopupWindow";
import options from "options";

const { bar, quicksettings } = options;
const media = (await Service.import("mpris")).bind("players");

const layout = Utils.derive([bar.position, quicksettings.position], (bar, qs) =>
    `${bar}-${qs}` as const
);

const Row = (
    toggles: Array<() => Gtk.Widget> = [],
    menus: Array<() => Gtk.Widget> = []
) => Widget.Box({
    vertical: true,
    children: [
        Widget.Box({
            homogeneous: true,
            class_name: "row horizontal",
            children: toggles.map(w => w())
        }),
        ...menus.map(w => w())
    ]
});

const activeBox = Variable('box1'); 

const Box1 = () => Widget.Box({
    vertical: true,
    class_name: "quicksettings vertical",
    css: quicksettings.width.bind().as(w => `min-width: ${w}px;`),
    children: [
        Row(
            [NetworkToggle, BluetoothToggle],
            [WifiSelection, BluetoothDevices]
        ),
        Row(
           [UpdateWidget, DarkModeToggle],
        ),
        Row([MicMute, DND]),
        Widget.Button({
            class_name: "sliders-box vertical",
            label: "Switch to Box2",
            on_clicked: async () => {
                activeBox.value = 'box2'; 
            }
        }),
    ],
});

const Box2 = () => Widget.Box({
    vertical: true,
    class_name: "quicksettings vertical",
    css: quicksettings.width.bind().as(w => `min-width: ${w}px;`),
    children: [ 
        Row(
            [ScreenshotToggle, ProfileToggle],
            [ScreenshotMenu, ProfileSelector],
        ),
        Widget.Button({
             class_name: "sliders-box vertical",
            label: "Switch to Box1",
            on_clicked: async () => {
                activeBox.value = 'box1';
            }
        }),
    ],
});

const RenderActiveBox = () => {
    return activeBox.value === 'box1' ? Box1() : Box2();
};

const updateSettings = () => {
    const settingsBox = Widget.Box({
        vertical: true,
        class_name: "quicksettings vertical",
        css: quicksettings.width.bind().as(w => `min-width: ${w}px;`),
        children: [
            Header(),
            RenderActiveBox(),
            Widget.Box({
                class_name: "sliders-box vertical",
                vertical: true,
                children: [
                    Row(
                        [Volume],
                        [SinkSelector, AppMixer]
                    ),
                    Microphone(),
                    Brightness()
                ]
            }),
           // Widget.Box({
           //     visible: media.as(l => l.length > 0),
           //     child: Media()
           // })
        ]
    });
    return settingsBox;
};

const QuickSettings = () => PopupWindow({
    name: "quicksettings",
    exclusivity: "exclusive",
    transition: bar.position.bind().as(pos => pos === "top" ? "slide_down" : "slide_up"),
    layout: layout.value,
    child: updateSettings()
});

activeBox.connect('changed', () => {
    App.removeWindow("quicksettings");
    App.addWindow(QuickSettings());
});

export function setupQuickSettings() {
    App.addWindow(QuickSettings());
    layout.connect("changed", () => {
        App.removeWindow("quicksettings");
        App.addWindow(QuickSettings());
    });
}
