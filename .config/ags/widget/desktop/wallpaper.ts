import wallpaper from "service/wallpaper"; 
import PopupWindow from "widget/PopupWindow";
import icons from "lib/icons"

const WALLPAPERS_PATH = `/home/${Utils.exec("whoami")}/Pictures/Wallpapers`;

function Wallpaper(wallpaperPath) {
  return Widget.Button({
    className: 'wallpaper',
    onPrimaryClick: () => {
      Utils.exec(`rm ${WALLPAPERS_PATH}/current.set`);
      Utils.exec(`ln -s ${wallpaperPath} ${WALLPAPERS_PATH}/current.set`);

      Utils.exec(`bash -c "${App.configDir}/shared/scripts/sidebar.sh close"`);
      Utils.exec(`bash -c "${App.configDir}/shared/scripts/sidebar.sh toggle-wallpapers"`);

      Utils.exec(`swww img ${wallpaperPath} --transition-type "wipe" --transition-duration 2`);

      wallpaper.set(wallpaperPath);
    },
    child: Widget.Overlay({
      className: 'overlay',
      child: Widget.Box(),
      overlays: [
        Widget.Icon({
          className: 'img',
          icon: wallpaperPath,
          size: 300,
        }),
      ],
    }),
  });
}

function WallpaperList() {
  return Widget.Scrollable({
    vexpand: true,
    child: Widget.Box({
      className: 'list',
      vertical: false,
      spacing: 12,
      children: Utils.exec(`find -L ${WALLPAPERS_PATH} -iname '*.png' -or -iname '*.jpg'`)
        .split('\n')
        .map(Wallpaper),
    }),
  });
}

function RandomWallpaperButton() {
  return Widget.Button({
    className: 'random',
    cursor: 'pointer',
    child: Widget.Box({
      vertical: false,
      children: [
        Widget.Icon({
          icon: icons.screenshot.shot, 
          css: 'margin-right: 5px;', 
        }),
        Widget.Label({ label: "Random" }) 
      ],
    }),
    onPrimaryClick: () => {
      const randomWallpaper = wallpaper.random(); 
      Utils.exec(`rm ${WALLPAPERS_PATH}/current.set`);
      Utils.exec(`ln -s ${randomWallpaper} ${WALLPAPERS_PATH}/current.set`);

      Utils.exec(`swww img ${randomWallpaper} --transition-type "wipe" --transition-duration 2`);

      wallpaper.set(randomWallpaper);
    },
  });
}

export default () => PopupWindow({
  name: "wallpaper",
  layout: "center",
  child: Widget.Box({
    className: 'wallpapers',
    vertical: true,
    children: [
      RandomWallpaperButton(), 
      WallpaperList(),
     ],
  }),
});
