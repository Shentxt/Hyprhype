//------------------------[Import]------------------------------------------------

import { opt, mkOptions } from "lib/option"
import { distro } from "lib/variables"
import { icon } from "lib/utils"
import icons from "lib/icons"

//------------------------[Options]------------------------------------------------

const options = mkOptions(OPTIONS, {
    autotheme: opt(true),

    wallpaper: {
       resolution: opt<import("service/wallpaper").Resolution>(1920),
       market: opt<import("service/wallpaper").Market>("random"),
    },

    theme: {
        dark: {
            primary: {
                bg: opt("#a69ae6"), //widgets background
                fg: opt("#2E3440"), //active foreground 
            },
            error: {
                bg: opt("#a69ae6"), //active background
                fg: opt("#2E3440"), //icon foreground 
            },
            bg: opt("#2E3440"), //background
            fg: opt("#c0caf5"), //font
            widget: opt("#BC9AD4"), //widgets foreground
            border: opt("#a69ae6"), //border
        },
        light: {
            primary: {
                bg: opt("#a69ae6"),
                fg: opt("#2E3440"),
            },
            error: {
                bg: opt("#a69ae6"),
                fg: opt("#2E3440"),
            },
            bg: opt("#D8D8D8"),
            fg: opt("#c0caf5"),
            widget: opt("#BC9AD4"),
            border: opt("#a69ae6"),
        },

        blur: opt(1),
        scheme: opt<"dark" | "light">("dark"),
        widget: { opacity: opt(85) },
        border: {
            width: opt(1),
            opacity: opt(1),
        },

        shadows: opt(true),
        padding: opt(6),
        spacing: opt(10),
        radius: opt(21),
    },

    transition: opt(200),

    font: {
        size: opt(10),
        name: opt("minecraft"),
    },

    bar: {
        flatButtons: opt(false),
        position: opt<"top" | "bottom">("top"),
        corners: opt(65),
        transparent: opt(true),
        layout: {
            start: opt<Array<import("widget/bar/Bar").BarWidget>>([
                "launcher",
                "workspaces",
                "taskbar",
                "expander",
                "messages",
            ]),
            center: opt<Array<import("widget/bar/Bar").BarWidget>>([
                "date",
            ]),
            end: opt<Array<import("widget/bar/Bar").BarWidget>>([
                "media",
                "expander",
                "systray",
                "colorpicker",
                "screenrecord",
                "system",
                "battery",
                "powermenu",
            ]),
        },
        launcher: {
            icon: {
                colored: opt(false),
                icon: opt(icon(distro.logo, icons.ui.search)),
            },
            label: {
                colored: opt(true),
		label: opt(""),
            },
            action: opt(() => App.toggleWindow("launcher")),
        },
        date: {
            format: opt("%H:%M:%S %p"),
            action: opt(() => App.toggleWindow("datemenu")),
        },
        battery: {
            bar: opt<"hidden" | "regular" | "whole">("regular"),
            charging: opt("#00D787"),
            percentage: opt(true),
            blocks: opt(7),
            width: opt(50),
            low: opt(30),
        },
        workspaces: {
            workspaces: opt(6),
        },
        taskbar: {
            iconSize: opt(16),
            monochrome: opt(true),
            exclusive: opt(true),
        },
        messages: {
            action: opt(() => App.toggleWindow("datemenu")),
        },
        systray: {
            ignore: opt([
                "KDE Connect Indicator",
                "spotify-client",
                "blueman-manager",
            ]),
        },
        media: {
            monochrome: opt(true),
            preferred: opt("spotify"),
            direction: opt<"left" | "right">("right"),
            format: opt("{artists} - {title}"),
            length: opt(40),
        },
        powermenu: {
            monochrome: opt(true),
            action: opt(() => App.toggleWindow("powermenu")),
        },
    },

    launcher: {
        width: opt(20),
        margin: opt(80),
        nix: {
            pkgs: opt("nixpkgs/nixos-unstable"),
            max: opt(6),
        },
        sh: {
            max: opt(16),
        },
        apps: {
            iconSize: opt(45),
            max: opt(6),
            favorites: opt([
                [
                    "firefox",
                    "stremio",
                    "org.gnome.Nautilus",
                    "steam",
                ],
            ]),
        },
    },

    overview: {
        scale: opt(8),
        workspaces: opt(6),
        monochromeIcon: opt(true),
    },

    powermenu: {
        sleep: opt("systemctl suspend"),
        reboot: opt("systemctl reboot"),
        logout: opt("pkill Hyprland"),
        shutdown: opt("shutdown now"),
        lock: opt("bash -c 'hyprlock -c ~/.config/hypr/rules/hyprlock.conf'"),
        layout: opt<"line" | "box">("line"),
        labels: opt(true),
    },

    quicksettings: {
        avatar: {
            image: opt(`/var/lib/AccountsService/icons/${Utils.USER}`),
            size: opt(70),
        },
        width: opt(380),
        position: opt<"left" | "center" | "right">("right"), 
        media: {
            monochromeIcon: opt(true),
            coverSize: opt(100),
        },
    },

    datemenu: {
        position: opt<"left" | "center" | "right">("center"),
        weather: {
            interval: opt(60_000),
            unit: opt<"metric" | "imperial" | "standard">("metric"),
            key: opt<string>(
                JSON.parse(Utils.readFile(`${App.configDir}/.weather`) || "{}")?.key || "",
            ),
            cities: opt<Array<number>>(
                JSON.parse(Utils.readFile(`${App.configDir}/.weather`) || "{}")?.cities || [],
            ),
        },
    },

    osd: {
        progress: {
            vertical: opt(true),
            pack: {
                h: opt<"start" | "center" | "end">("end"),
                v: opt<"start" | "center" | "end">("center"),
            },
        },
        microphone: {
            pack: {
                h: opt<"start" | "center" | "end">("center"),
                v: opt<"start" | "center" | "end">("end"),
            },
        },
    },

    notifications: {
        position: opt<Array<"top" | "bottom" | "left" | "right">>(["top", "right"]),
        blacklist: opt(["Spotify"]),
        width: opt(440),
    },
 
    hyprland: {
        gaps: opt(2.0),
        inactiveBorder: opt("#282828"),
        gapsWhenOnly: opt(false),
    },
})

globalThis["options"] = options
export default options
