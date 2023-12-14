import icons from "../../icons.js";
import Avatar from "../../misc/Avatar.js";
import { uptime } from "../../variables.js";
import { Battery, Widget } from "../../imports.js";

export const BatteryProgress = () =>
  Widget.Box({
    className: "battery-progress",
    vexpand: true,
    binds: [["visible", Battery, "available"]],
    connections: [
      [
        Battery,
        (w) => {
          w.toggleClassName("half", Battery.percent < 46);
          w.toggleClassName("low", Battery.percent < 30);
        },
      ],
    ],
    children: [
      Widget.Overlay({
        vexpand: true,
        child: Widget.ProgressBar({
          hexpand: true,
          vexpand: true,
          connections: [
            [
              Battery,
              (progress) => {
                progress.fraction = Battery.percent / 100;
              },
            ],
          ],
        }),
        overlays: [
          Widget.Label({
            connections: [
              [
                Battery,
                (l) => {
                  l.label =
                    Battery.charging || Battery.charged
                      ? icons.battery.charging
                      : `${Battery.percent}%`;
                },
              ],
            ],
          }),
        ],
      }),
    ],
  });

export default () =>
  Widget.Box({
    className: "header",
    children: [
      Avatar(),
      Widget.Box({
        className: "system-box",
        vertical: true,
        hexpand: true,
        children: [
          Widget.Box({
            children: [
              Widget.Button({
                valign: "center",
                onClicked: "mugshot",
                onSecondaryClick: "nwg-look",
                child: Widget.Icon(icons.settings),
              }),
              Widget.Label({
                className: "uptime",
                hexpand: true,
                valign: "center",
                connections: [
                  [
                    uptime,
                    (label) => {
                      label.label = `uptime: ${uptime.value}`;
                    },
                  ],
                ],
              }),
              Widget.Button({
                valign: "center",
                onClicked: "bash -c \"'~/.config/hypr/scripts/pacman/'\"",
                onSecondaryClick:
                  "bash -c \"wezterm start --always-new-process -e $SHELL -c 'w3m https://archlinux.org/packages/'\"",
                child: Widget.Icon(icons.update),
              }),
              Widget.Button({
                valign: "center",
                onClicked: "bash -c ~/.config/hypr/scripts/gamemode",
                onSecondaryClick:
                  "bash -c \"wezterm start --always-new-process -e $SHELL -c 'w3m https://www.protondb.com/explore?selectedFilters=whitelisted'\"",
                child: Widget.Icon(icons.game),
              }),
            ],
          }),
          BatteryProgress(),
        ],
      }),
    ],
  });
