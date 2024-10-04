import icons from "lib/icons"
//import { uptime } from "lib/variables"
import { uptime, userAndHost } from "lib/variables";
import options from "options"
import apps from "lib/apps"
import { dependencies, sh } from "lib/utils"

const battery = await Service.import("battery")
const { image, size } = options.quicksettings.avatar
const marginRight = '5px';

function up(up: number) {
    const h = Math.floor(up / 60)
    const m = Math.floor(up % 60)
    return `${h}h ${m < 10 ? "0" + m : m}m`
} 
 
const Avatar = () => Widget.Button({
    class_name: "avatar",
    css: Utils.merge([image.bind(), size.bind()], (img, size) => `
        min-width: ${size}px;
        min-height: ${size}px;
        background-image: url('${img}');
        background-size: cover;
    `),
    on_clicked: () => sh(apps.services.profile.value),
});

export const Header = () => Widget.Box(
    { class_name: "header horizontal" },
    Avatar(),
    Widget.Box({
        vertical: true,
        vpack: "center",
        children: [
            Widget.Box({
                visible: battery.bind("available"),
                children: [
                    Widget.Icon({ icon: battery.bind("icon_name") }),
                    Widget.Label({ label: battery.bind("percent").as(p => `${p}%`) }),
                ],
            }),
            Widget.Box([
                  Widget.Label({ label: userAndHost.bind().as(info => info) }),
            ]),
            Widget.Label({
                label: "----- -----",
                class_name: "section-label",
            }),
            Widget.Box([
            Widget.Icon({
            icon: icons.ui.time,
            css: `margin-right: ${marginRight};`
            }),
                Widget.Label({ label: uptime.bind().as(up) }),
            ]),
       ],
    }),
    Widget.Box({ hexpand: true }),
    Widget.Button({
        vpack: "center",
        child: Widget.Icon(icons.system.disk),
        on_clicked: () => {
          sh(apps.execs.list.value);
        },
    }),
    Widget.Button({
        vpack: "center",
        child: Widget.Icon(icons.ui.settings),
        on_clicked: () => {
            App.closeWindow("quicksettings")
            App.closeWindow("settings-dialog")
            App.openWindow("settings-dialog")
        },
    }), 
)
