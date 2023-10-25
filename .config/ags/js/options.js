export default {
    // if this player is running this will be shown on panel
    preferredMpris: 'spotify',
    preferredMpris: 'firefox',
    preferredMpris: 'youtube-music',

    // number of workspaces shown on panel and overview
    workspaces: 4,

    //
    dockItemSize: 56,

    battaryBar: {
        // wether to show percentage by deafult
        showPercentage: true,

        // at what percentages should the battery-bar change color
        low: 30,
        medium: 50,
    },

    // at what intervals should cpu, ram, temperature refresh
    systemFetchInterval: 5000,

    // the slide down animation on quicksettings and dashboard
    windowAnimationDuration: 250,

    // keyboard id for brightnessctl
    brightnessctlKBD: 'asus::kbd_backlight',
};
