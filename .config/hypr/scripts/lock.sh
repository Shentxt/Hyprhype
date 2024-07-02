#!/bin/bash

# -------------------------------------------------------------------------
#
# ██╗      ██████╗  ██████╗██╗  ██╗
# ██║     ██╔═══██╗██╔════╝██║ ██╔╝
# ██║     ██║   ██║██║     █████╔╝ 
# ██║     ██║   ██║██║     ██╔═██╗ 
# ███████╗╚██████╔╝╚██████╗██║  ██╗
# ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
#
# ----- Author: Shen - url: https://github.com/Shentxt -----

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                 Executed Lockscreen
#
# just block, there is not much science behind this
#
# required to function
# --------------------
# lock: hyprlock
# admi: swayidle
# notify-send: really?
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#!/bin/bash

lock_screen() {
    notify-send 'Mitsuru' 'The screen will lock <span color="yellow">10 seconds</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png
    sleep 10
    hyprlock -c ~/.config/hypr/rules/hyprlock.conf
}

unlock_screen() {
    notify-send 'Mitsuru' 'The Screen <span color="yellow">Will Unlock</span>' -i ~/.config/hypr/assets/icons/persona/mitsuru.png
}

swayidle -w \
    timeout 600 'lock_screen' \
    resume 'unlock_screen'
