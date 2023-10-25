// Import And Config Modules
import { Utils } from './imports.js';
const WP = `/home/${Utils.USER}/Pictures/Wallpapers/`;

const editScheme = (scheme, edit) => {
    const obj = {};
    Object.keys(scheme).forEach(color => obj[color] = edit(scheme[color]));
    return obj;
};

// ----------------------------------------------
// Colors
const gnome = {
    red: '#BF616A',
    green: '#57e389',
    yellow: '#f6d32d',
    blue: '#5e81ac',
    magenta: '#c061cb',
    violet: '#a69ae6',
    teal: '#5bc8aF',
    orange: '#D08770',
    white: '#cad5ff',
};

const light = {
    color_scheme: 'light',
    fg_color: '#cad5ff',
    bg_color: '#2A2F3A',
    hover_fg: '#8FAFD1', 
   ...editScheme(gnome, c => `darken(${c}, 8%)`),
};

// Styles bar: floating, normal and separated
const misc = {
    wm_gaps: 22,
    radii: 9,
    spacing: 9,
    shadow: 'rgba(59, 66, 82, 0.6)',
    drop_shadow: true,
    transition: 200,
    screen_corners: true,
    bar_style: 'separated',
    layout: 'topbar',
    desktop_clock: 'center center',
    font: 'minecraft',
    mono_font: 'Mononoki Nerd Font',
    font_size: 16,
};

const colors = {
    wallpaper_fg: 'white',
    hypr_active_border: 'rgb(5e81ac) rgb(BC9AD4) 45deg',
    hypr_inactive_border: 'rgb(586A80) rgb(cad5ff) 45deg',
    accent: '$fg_color',
    accent_fg: '$bg_color',
    widget_bg: '$bg_color',
    widget_opacity: 94,
    active_gradient: 'to right, $accent, lighten($accent, 6%)',
    border_color: '$fg_color',
    border_opacity: 50,
    border_width: 3,
};

//--------------------------------------------------------
const theme = {
    ...light,
    ...misc,
    ...colors,
};

const cherry = {
    ...theme,
    wallpaper: WP + 'cherry.png',
    name: 'cherry',
    icon: ' ',
    accent: '$blue',
    active_gradient: 'to right, $accent, lighten(mix($magenta, $blue, 70%), 21%)',
    radii: 13,
    brorder_width: 12,
    bg_color: 'transparentize(#3B4252, 0.3)',
};

export default [
    cherry,
];
