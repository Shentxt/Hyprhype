import { launchApp, icon } from "lib/utils";
import options from "options";
import icons from "lib/icons";
import { type Application } from "types/service/applications";
import PanelButton from "../../bar/PanelButton";

const apps = await Service.import("applications");
const { query } = apps;
const { iconSize } = options.launcher.apps;

const QuickAppButton = (app: Application) => PanelButton({
    class_name: "panel-button",
    tooltip_text: app.name,
    on_primary_click: () => {
        launchApp(app);  
    },
    child: Widget.Icon({
        size: iconSize.bind(),
        icon: icon(app.icon_name, icons.fallback.executable),
    }),
});

export function FavoritesWidget() {
    const favs = options.launcher.apps.favorites.bind();
    
    return Widget.Box({
        vertical: true,
        children: favs.as(favs => favs.flatMap(fs => [
            Widget.Separator(),
            Widget.Box({
                children: fs
                    .map(f => query(f)?.[0])
                    .filter(f => f)
                    .map(QuickAppButton),  
            }),
        ])),
    });
}
