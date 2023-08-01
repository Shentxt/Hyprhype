local wezterm = require ("wezterm")


-- The filled in variant of the < symbol
local SOLID_LEFT_ARROW = utf8.char(0xe0ba)
local SOLID_LEFT_MOST = utf8.char(0x2588)

-- The filled in variant of the > symbol
local SOLID_RIGHT_ARROW = utf8.char(0xe0bc)

local my_colors = {
	 foreground = "#a5b6cf",
	 background = "#0d0f18",
	 cursor_bg = "#a5b6cf",
	 cursor_fg = "#282a36",
	 cursor_border = "#f8f8f2",
	 selection_fg = "none",
	 selection_bg = "rgba(68,71,90,0.5)",
	 scrollbar_thumb = "#44475a",
	 split = "#6272a4",
	 ansi = {
		 "#3d414f", 
		 "#dd6777", 
		 "#90ceaa", 
		 "#ecd3a0", 
		 "#86aaec", 
		 "#c296eb", 
		 "#93cee9", 
		 "#cbced3"
	 },
	 brights = {
		 "#3d414f", 
		 "#dd6777", 
		 "#90ceaa", 
		 "#ecd3a0", 
		 "#86aaec", 
		 "#c296ed", 
		 "#93cee9", 
		 "#cbced3"
	 },
	 
	 compose_cursor = "#FFB86C",

     tab_bar = {
	     background = '#181926',
             inactive_tab_edge = '#363a4f',

     active_tab = {
	     bg_color = '#0d0f18',
	     fg_color = '#a5b6cf',
	     intensity = 'Normal',
	     italic = false,
	     strikethrough = false,
	     underline = 'None', 
        },

     inactive_tab = {
             bg_color = '#1e2030',
	     fg_color = '#cad3f5',
	     intensity = 'Normal',
	     italic = false,
	     strikethrough = false,
	     underline = 'None',
        },

     inactive_tab_hover = {
	     bg_color = '#24273a',
	     fg_color = '#cad3f5',
	     intensity = 'Normal',
	     italic = false,
	     strikethrough = false,
	     underline = 'None',}
        },
}

 local mykeys = {}
table.insert(mykeys, {
	key = "1",
	mods = "CTRL",
	action = wezterm.action.ActivateTabRelative(-1),
})

table.insert(mykeys, {
	key = "2",
	mods = "CTRL",
	action = wezterm.action.ActivateTabRelative(1),
})

table.insert(mykeys, {
	key = "h",
	mods = "CTRL",
	action = wezterm.action{SplitHorizontal={domain="CurrentPaneDomain"}},
})

table.insert(mykeys, {
	key = "l",
	mods = "CTRL",
	action = wezterm.action{SplitVertical={domain="CurrentPaneDomain"}},
})

local pwd = io.popen("cd"):read()
local padding = {
	left = "1cell",
	right = "1cell",
	top = "0.5cell",
	bottom = "0.5cell",
}

wezterm.time.call_after(60, function()
wezterm.reload_configuration()
end)

local function font_with_fallback(name, params)
local names = { name, "mini-file-icons", "Hack Nerd Font", "SauceCodePro Nerd Font" }
return wezterm.font_with_fallback(names, params)
end

local function window_padding(margins)
	return {
		top = margins,
		bottom = margins,
		left = margins,
		right = margins,
	}
end

return {
	colors = my_colors,
        window_padding = window_padding(16),
        default_cwd = pwd,
  	scrollback_lines = 2500,
        cursor_blink_ease_in = "EaseOut", 
        cursor_blink_rate = 450,
        default_cursor_style = "BlinkingBar",
        cursor_thickness = "2px",
        use_fancy_tab_bar = false,
        enable_wayland = true,
        window_close_confirmation = "NeverPrompt",
    font = wezterm.font "Monocraft",
	font_size = 11,
	line_height = 1.3,
	enable_tab_bar = true,
	window_padding = window_padding(16),
	window_decorations = "RESIZE",
	bold_brightens_ansi_colors = true,
	use_dead_keys = true,
	disable_default_key_bindings = false,
   --window_background_image = "Pictures/background/A_magic_sword_among_ancient_ruins_3840x2160.jpeg",
   --windowTitle = "d Terminal ${sessionName}-${terminalNumber}",
    keys = mykeys,
	} 
