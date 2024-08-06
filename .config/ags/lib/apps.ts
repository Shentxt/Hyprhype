import { sh } from "lib/utils"
import { opt, mkOptions } from "lib/option"

export default {
    services: {
        networkSettings: opt("kitty --title 'Float' networkctl"),
        bluetoothSettings: opt("blueberry"),
    },
  }
