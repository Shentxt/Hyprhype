import { Menu, ArrowToggleButton } from "../ToggleButton"
import icons from "lib/icons"
import { dependencies, sh, bash } from "lib/utils"
import GLib from "gi://GLib"

const recordingsPath = `${Utils.HOME}/Videos/Screencasting`

export const VideoToggle = () => ArrowToggleButton({
    name: "video",
    icon: icons.ui.muted,
    label: "Video",
    connection: [], 
    deactivate: () => {},
    activate: () => VideoMenu().open(), 
})

export const VideoMenu = () => Menu({
    name: "video",
    icon: icons.ui.video,
    title: "Video Options",
    content: [
        Widget.Box({
            vertical: true,
            children: [
                Widget.Button({
                    on_clicked: async () => {
                        if (!dependencies("slurp", "wf-recorder")) return

                        const file = `${recordingsPath}/${now()}.mp4`
                        Utils.ensureDirectory(recordingsPath)

                        // Start recording area if selected
                        const area = await sh("slurp")
                        if (area) {
                            await sh(`wf-recorder -g "${area}" -f ${file} --pixel-format yuv420p`)
                        } else {
                            await sh(`wf-recorder -f ${file} --pixel-format yuv420p`)
                        }

                        Utils.notify({
                            iconName: icons.fallback.video,
                            summary: "Video Recording",
                            body: file,
                            actions: {
                                "Show in Files": () => sh(`xdg-open ${recordingsPath}`),
                                "View": () => sh(`xdg-open ${file}`),
                            },
                        })
                    },
                    child: Widget.Box({
                        children: [
                            Widget.Icon(icons.ui.video),
                            Widget.Label("Start Recording (Area or Full Screen)"),
                        ],
                    }),
                }),
                Widget.Button({
                    on_clicked: async () => {
                        if (!dependencies("wf-recorder")) return

                        await bash("killall -INT wf-recorder")

                        Utils.notify({
                            iconName: icons.fallback.video,
                            summary: "Video Recording Stopped",
                            body: "Recording has been stopped.",
                            actions: {
                                "Show in Files": () => sh(`xdg-open ${recordingsPath}`),
                            },
                        })
                    },
                    child: Widget.Box({
                        children: [
                            Widget.Icon(icons.ui.stop),
                            Widget.Label("Stop Recording"),
                        ],
                    }),
                }),
            ],
        }),
    ],
})

const now = () => GLib.DateTime.new_now_local().format("%Y-%m-%d_%H-%M-%S")
