import { sh } from "lib/utils"
import { opt, mkOptions } from "lib/option"

export default {
    execs: {
      update: opt("bash -c 'kitty --title 'Float' -e ~/.config/hypr/scripts/get_updates.sh --update-system &'"),
      list: opt("bash -c 'kitty --title 'Float' -e ~/.config/hypr/scripts/get_updates.sh --print-updates &'")
  },
    services: {
        networkSettings: opt("nm-connection-editor"),
        bluetoothSettings: opt("blueberry"),
        profile: opt("mugshot")
    },
  }
