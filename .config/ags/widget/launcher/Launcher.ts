import { type Binding } from "lib/utils";
import PopupWindow, { Padding } from "widget/PopupWindow";
import icons from "lib/icons";
import options from "options";
import nix from "service/nix";
import * as AppLauncher from "./AppLauncher";
import * as NixRun from "./NixRun";
import * as ShRun from "./ShRun";
import GLib from 'gi://GLib';

const { width, margin } = options.launcher;
const isnix = nix.available;
const homeDir = GLib.get_home_dir();
const imagePath = `${homeDir}/.config/ags/assets/icon.jpg`;

function Launcher() {
    const favs = AppLauncher.Favorites();
    const applauncher = AppLauncher.Launcher();
    const sh = ShRun.ShRun();
    const shicon = ShRun.Icon();
    const nix = NixRun.NixRun();
    const nixload = NixRun.Spinner();

    function HelpButton(cmd: string, desc: string | Binding<string>) {
        return Widget.Box(
            { vertical: true },
            Widget.Separator(),
            Widget.Button(
                {
                    class_name: "help",
                    on_clicked: () => {
                        entry.grab_focus();
                        entry.text = `:${cmd} `;
                        entry.set_position(-1);
                    },
                },
                Widget.Box([
                    Widget.Label({
                        class_name: "name",
                        label: `:${cmd}`,
                    }),
                    Widget.Label({
                        hexpand: true,
                        hpack: "end",
                        class_name: "description",
                        label: desc,
                    }),
                ]),
            ),
        );
    }

    const help = Widget.Revealer({
        child: Widget.Box(
            { vertical: true },
            HelpButton("sh", "run a binary"),
            isnix ? HelpButton("nx", options.launcher.nix.pkgs.bind().as(pkg =>
                `run a nix package from ${pkg}`,
            )) : Widget.Box(),
        ),
    });

    const entry = Widget.Entry({
        hexpand: true,
        primary_icon_name: icons.ui.search,
        on_accept: ({ text }) => {
            if (text?.startsWith(":nx"))
                nix.run(text.substring(3));
            else if (text?.startsWith(":sh"))
                sh.run(text.substring(3));
            else
                applauncher.launchFirst();

            App.toggleWindow("launcher");
            entry.text = "";
        },
        on_change: ({ text }) => {
            text ||= "";
            favs.reveal_child = text === "";
            help.reveal_child = text.split(" ").length === 1 && text?.startsWith(":");

            if (text?.startsWith(":nx"))
                nix.filter(text.substring(3));
            else
                nix.filter("");

            if (text?.startsWith(":sh"))
                sh.filter(text.substring(3));
            else
                sh.filter("");

            if (!text?.startsWith(":"))
                applauncher.filter(text);
        },
              class_name: "selection",
       css: `
             background: transparent;
             color: #c0caf5;
             padding: 6px;
         `
    });

    const entryContainer = Widget.Box({
       css: ` 
            background-image: url('${imagePath}'); 
            background-size: cover;
            background-position: center;
            border-color: #a69ae6;
            border-width: 2px;
            border-radius: 12px;
            border-style: inset;
        `,
        children: [entry]  
    });

    function focus() {
        entry.text = "Search";
        entry.set_position(-1);
        entry.select_region(0, -1);
        entry.grab_focus();
        favs.reveal_child = true;
    }

    const layout = Widget.Box({
        css: width.bind().as(v => `min-width: ${v}pt;`),
        class_name: "launcher",
        vertical: true,
        vpack: "start",
        setup: self => self.hook(App, (_, win, visible) => {
            if (win !== "launcher")
                return;

            entry.text = "";
            if (visible)
                focus();
        }),
        children: [
            Widget.Box([entryContainer, nixload, shicon]),  
            favs,
            help,
            applauncher,
            nix,
            sh,
        ],
    });

    return Widget.Box(
        { vertical: true, css: "padding: 1px" },
        Padding("launcher", {
            css: margin.bind().as(v => `min-height: ${v}pt;`),
            vexpand: false,
        }),
        layout,
    );
}

export default () => PopupWindow({
    name: "launcher",
    layout: "top",
    child: Launcher(),
});
