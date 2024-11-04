import "lib/session"
import "style/style"
import init from "lib/init"
import options from "options"
import Bar from "widget/bar/Bar"
import Launcher from "widget/launcher/Launcher"
import NotificationPopups from "widget/notifications/NotificationPopups"
import OSD from "widget/osd/OSD"
import Overview from "widget/overview/Overview"
import PowerMenu from "widget/powermenu/PowerMenu"
import ScreenCorners from "widget/bar/ScreenCorners"
import SettingsDialog from "widget/settings/SettingsDialog"
import Verification from "widget/powermenu/Verification"
import WallpaperWindow from "widget/desktop/wallpaper" 
import Mapkey from "widget/desktop/Mapkey" 
import { forMonitors } from "lib/utils"
import { setupQuickSettings } from "widget/quicksettings/QuickSettings"
import { setupDateMenu } from "widget/datemenu/DateMenu"
import { setupMediaWindow } from "widget/media/media";

App.config({
    onConfigParsed: () => {
        setupQuickSettings()
        setupDateMenu()
        setupMediaWindow()
        init()
    },
    closeWindowDelay: {
        "launcher": options.transition.value,
        "overview": options.transition.value,
        "quicksettings": options.transition.value,
        "datemenu": options.transition.value,
        "media": options.transition.value,
        "wallpaper": options.transition.value,
        "mapkey": options.transition.value, 
    },
    windows: () => [
        ...forMonitors(Bar),
        ...forMonitors(NotificationPopups),
        ...forMonitors(ScreenCorners),
        ...forMonitors(OSD),
        Launcher(),
        Overview(),
        PowerMenu(),
        SettingsDialog(),
        Verification(),
        WallpaperWindow(),
        Mapkey(),
    ],
})
