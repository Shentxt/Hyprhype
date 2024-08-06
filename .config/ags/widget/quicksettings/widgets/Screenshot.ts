import { Menu, ArrowToggleButton } from "../ToggleButton"
import icons from "lib/icons"
import { dependencies, sh, bash } from "lib/utils"
import GLib from "gi://GLib"

const screenshotsPath = `${Utils.HOME}/Pictures/Screenshots`

export const ScreenshotToggle = () => ArrowToggleButton({
    name: "screenshot",
    icon: icons.screenshot.shot,
    label: "Screenshot",
    connection: [], 
    deactivate: () => {},
    activate: () => ScreenshotMenu().open(), 
})

export const ScreenshotMenu = () => Menu({
    name: "screenshot",
    icon: icons.screenshot.shot,
    title: "Screenshot Options",
    content: [
        Widget.Box({
            vertical: true,
            children: [
                Widget.Button({
                    on_clicked: async () => {
                        if (!dependencies("slurp", "wayshot")) return

                        const file = `${screenshotsPath}/${now()}.png`
                        Utils.ensureDirectory(screenshotsPath)

                        await sh(`wayshot -f ${file}`)
                        bash(`wl-copy < ${file}`)

                        Utils.notify({
                            image: file,
                            summary: "Screenshot",
                            body: file,
                            actions: {
                                "Show in Files": () => sh(`xdg-open ${screenshotsPath}`),
                                "View": () => sh(`xdg-open ${file}`),
                                "Edit": () => {
                                    if (dependencies("swappy"))
                                        sh(`swappy -f ${file}`)
                                },
                            },
                        })
                    },
                    child: Widget.Box({
                        children: [
                            Widget.Icon(icons.screenshot.shot),
                            Widget.Label("Full Screenshot"),
                        ],
                    }),
                }),
                Widget.Button({
                    on_clicked: async () => {
                        if (!dependencies("slurp", "wayshot")) return

                        const size = await sh("slurp")
                        if (!size) return

                        const file = `${screenshotsPath}/${now()}.png`
                        Utils.ensureDirectory(screenshotsPath)

                        await sh(`wayshot -f ${file} -s "${size}"`)
                        bash(`wl-copy < ${file}`)

                        Utils.notify({
                            image: file,
                            summary: "Screenshot",
                            body: file,
                            actions: {
                                "Show in Files": () => sh(`xdg-open ${screenshotsPath}`),
                                "View": () => sh(`xdg-open ${file}`),
                                "Edit": () => {
                                    if (dependencies("swappy"))
                                        sh(`swappy -f ${file}`)
                                },
                            },
                        })
                    },
                    child: Widget.Box({
                        children: [
                            Widget.Icon(icons.screenshot.region),
                            Widget.Label("Region Screenshot"),
                        ],
                    }),
                }),
            ],
        }),
    ],
})

const now = () => GLib.DateTime.new_now_local().format("%Y-%m-%d_%H-%M-%S")
