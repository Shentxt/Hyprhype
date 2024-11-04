import PopupWindow from "widget/PopupWindow";
import { sh } from "lib/utils";

function CommandOutput() {

  const commandOutput = Utils.exec('bash -c "awk \'/^[a-z]/ && last {print $0, \\"\t\\",last} {last=\\"\\"} /^#/{last=$0}\' /home/shen/.config/hypr/rules/keybinds.conf | column -t -s $\'\\t\' | awk \'{$1=$1; print}\'"');

  const outputLines = commandOutput.split('\n').filter(line => line.trim() !== '').map(line => 
    Widget.Label({
      label: line,
      className: 'wallpaper', 
    })
  );

  return Widget.Box({
    className: 'wallpaper',
    vertical: true,
    spacing: 6,
    children: outputLines,
  });
}

export default () => PopupWindow({
  name: "Mapkey",
  layout: "center",
  child: Widget.Box({
    className: 'wallpapers',
    vertical: true,
    children: [
      Widget.Label({ label: "Keybinds:", className: 'title' }),
      CommandOutput(),
    ],
  }),
});

