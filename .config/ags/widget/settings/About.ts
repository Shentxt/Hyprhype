import GLib from 'gi://GLib';

const homeDir = GLib.get_home_dir();
const imagePath = `${homeDir}/.config/ags/assets/linux.png`; 

const fontSize = '18px';
const marginBottom = '15px';

export default () => {
    const systemInfo = { 
    };

    systemInfo.distro = Utils.exec("bash -c \"lsb_release -i | awk -F':' '{print $2}' | xargs\"");
    systemInfo.window = Utils.exec("bash -c \"echo $XDG_CURRENT_DESKTOP\""); 
    systemInfo.server = Utils.exec("bash -c \"echo $XDG_SESSION_TYPE\""); 
    
    systemInfo.kernel = Utils.exec("bash -c \"uname -r\""); 
    systemInfo.bar = `AGS ${Utils.exec("ags -v")}`;

  systemInfo.memory = Utils.exec("bash -c \"free -h | awk 'NR==2 {print $3}' | xargs\"") + "/" + Utils.exec("bash -c \"free -h | awk 'NR==2 {print $2}' | xargs\"");
  systemInfo.disksize = Utils.exec("bash -c \"df -h / | awk 'NR==2 {print $3}' | xargs\"") + "/" + Utils.exec("bash -c \"df -h / | awk 'NR==2 {print $2}' | xargs\"");

  systemInfo.icon = Utils.exec("bash -c \"gsettings get org.gnome.desktop.interface icon-theme\" | xargs"); 
  systemInfo.gtk = Utils.exec("bash -c \"gsettings get org.gnome.desktop.interface gtk-theme\" | tr -d \"'\""); 
  systemInfo.cursor = Utils.exec("bash -c \"gsettings get org.gnome.desktop.interface cursor-theme\" | tr -d \"'\"");
  systemInfo.font = Utils.exec("bash -c \"gsettings get org.gnome.desktop.interface font-name\" | tr -d \"'\"");

    return Widget.Box(
        { class_name: "row about", hexpand: true },
        Widget.Box(
            { vertical: true, hexpand: true, halign: 'center', vexpand: true },
            Widget.Label({
                xalign: 0,
                class_name: "row-title",
                label: "About",
                vpack: "start",
            }),
            Widget.Label({
                label: "----- [ System ] -----",
                class_name: "section-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.kernel}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: `󰥠 : ${systemInfo.distro}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: `  : ${systemInfo.bar}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.window}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.server}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),


            Widget.Label({
                label: "----- [ Storage & Memory ] -----",
                class_name: "section-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: `󰍛 : ${systemInfo.memory}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.disksize}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),

            Widget.Label({
               label: "----- [ Theme ] -----",
                class_name: "section-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.icon}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.cursor}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.gtk}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
            Widget.Label({
                label: ` : ${systemInfo.font}`,
                class_name: "info-label",
                css: `font-size: ${fontSize}; margin-bottom: ${marginBottom};`,
            }),
        
    ),
        Widget.Box(
            {
                class_name: "image-box",
                css: `
                    min-width: 500px;
                    min-height: 120px;
                    background-image: url('${imagePath}');
                    background-size: cover;
                    background-position: center;
                `,
            }
        ),
    );
};
