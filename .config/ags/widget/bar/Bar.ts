import BatteryBar from "./buttons/BatteryBar"
import ColorPicker from "./buttons/ColorPicker"
import Date from "./buttons/Date"
import Launcher from "./buttons/Launcher"
import Media from "./buttons/Media"
import PowerMenu from "./buttons/PowerMenu"
import SysTray from "./buttons/SysTray"
import SystemIndicators from "./buttons/SystemIndicators"
import Workspaces from "./buttons/Workspaces"
import ScreenRecord from "./buttons/ScreenRecord"
import Messages from "./buttons/Messages"
import Taskbar from "./buttons/Taskbar"
import options from "options"

const { transparent, position } = options.bar

export default (monitor: number) => Widget.Window({
    monitor,
    class_name: "bar",
    name: `bar${monitor}`,
    exclusivity: "exclusive",
    layer: "bottom",
    anchor: position.bind().as(pos => [pos, "right", "left"]),
    child: Widget.CenterBox({
        css: "min-width: 2px; min-height: 2px;",
        startWidget: Widget.Box({
            hexpand: true,
            children: [
            Launcher(),
            Workspaces(),
            Taskbar(),
      ],
        }),
        centerWidget: Widget.Box({
            hpack: "center",
            children: [
            Messages(),
            Date(),
            Media(),
      ],
        }),
        endWidget: Widget.Box({
            hexpand: true,
            children: [ 
            Widget.Box({ expand: true }), 
            ColorPicker(),
            BatteryBar(),
            ScreenRecord(),
            SysTray(),
            SystemIndicators(),
            PowerMenu(),
            ],
        }),
    }),
    setup: self => self.hook(transparent, () => {
        self.toggleClassName("transparent", transparent.value)
    }),
})
