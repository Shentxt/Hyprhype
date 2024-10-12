import options from "options"
import { active1, active2, inactive1, inactive2 } from "colrandom"
const { messageAsync } = await Service.import("hyprland")

const {
    hyprland,
    theme: {
        spacing,
        radius,
        border: { width },
        blur,
        shadows,
        dark: {
            primary: { bg: darkActive },
        },
        light: {
            primary: { bg: lightActive },
        },
        scheme,
    },
} = options

const deps = [
    "hyprland",
    spacing.id,
    radius.id,
    blur.id,
    width.id,
    shadows.id,
    darkActive.id,
    lightActive.id,
    scheme.id,
]

function primary() {
    return scheme.value === "dark"
        ? darkActive.value
        : lightActive.value
}

function rgba(color: string) {
    return `rgba(${color}ff)`.replace("#", "")
}

function sendBatch(batch: string[]) {
    const cmd = batch
        .filter(x => !!x)
        .map(x => `keyword ${x}`)
        .join("; ")

    return messageAsync(`[[BATCH]]/${cmd}`)
}

async function setupHyprland() {
    const wm_gaps = Math.floor(hyprland.gaps.value * spacing.value)
 
    sendBatch([
        `general:border_size ${width}`,
        `general:gaps_out ${wm_gaps}`,
        `general:gaps_in ${Math.floor(wm_gaps / 4)}`, 
        `general:col.active_border ${rgba(active1())} ${rgba(active2())}`,
        `general:col.inactive_border ${rgba(inactive1())} ${rgba(inactive2())}`,       
        `decoration:rounding ${radius}`,
        `decoration:drop_shadow ${shadows.value ? "yes" : "no"}`,
        `dwindle:no_gaps_when_only ${hyprland.gapsWhenOnly.value ? 0 : 1}`,
        `master:no_gaps_when_only ${hyprland.gapsWhenOnly.value ? 0 : 1}`,
    ])

    await sendBatch(App.windows.map(({ name }) => `layerrule unset, ${name}`))

    if (blur.value > 0) {
        sendBatch(App.windows.flatMap(({ name }) => [
            `layerrule unset, ${name}`,
            `layerrule blur, ${name}`,
            `layerrule ignorealpha ${/* based on shadow color */.20}, ${name}`,
        ]))
    }

    function updateBorderColors() {
        sendBatch([
            `general:col.active_border ${rgba(active1())} ${rgba(active2())}`,
            `general:col.inactive_border ${rgba(inactive1())} ${rgba(inactive2())}`
        ]);
    }

    setInterval(updateBorderColors, 2300);
}

export default function init() {
    options.handler(deps, setupHyprland)
    setupHyprland()
}
