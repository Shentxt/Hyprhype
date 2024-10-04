//import Launcher from "./buttons/Launcher"
import Taskbar from "./buttons/Taskbar"
import options from "options"

const { transparent, position } = options.bar

export default (monitor: number) => Widget.Window({
    monitor,
    class_name: "bar",
    name: `dock${monitor}`,
    exclusivity: "exclusive",
//  anchor: position.bind().as(pos => [pos, "right", "left"]),
    anchor: position.bind().as(pos => ["bottom", "right", "left"]),
    child: Widget.CenterBox({
        css: "min-width: 2px; min-height: 2px;",
        startWidget: Widget.Box({
            hexpand: true,
            children: [
 //           Launcher(),
      ],
        }),
        centerWidget: Widget.Box({
            hpack: "center",
            children: [
            Taskbar(),
      ],
        }),
        endWidget: Widget.Box({
            hexpand: true,
            children: [ 
            Widget.Box({ expand: true }),
            ],
        }),
    }),
    setup: self => self.hook(transparent, () => {
        self.toggleClassName("transparent", transparent.value)
    }),
})
