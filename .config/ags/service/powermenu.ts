import options from "options"

const { sleep, reboot, logout, shutdown, lock } = options.powermenu

export type Action = "sleep" | "reboot" | "logout" | "shutdown" | "lock"

class PowerMenu extends Service {
    static {
        Service.register(this, {}, {
            "title": ["string"],
            "cmd": ["string"],
        })
    }

    #title = ""
    #cmd = ""

    get title() { return this.#title }

    action(action: Action) {
        [this.#cmd, this.#title] = {
            sleep: [sleep.value, "Sleep"],
            reboot: [reboot.value, "Reboot"],
            logout: [logout.value, "Log Out"],
            shutdown: [shutdown.value, "Shutdown"],
            lock: [lock.value, "Lock"], 
        }[action]

        this.notify("cmd")
        this.notify("title")
        this.emit("changed")

        if (action === "lock") {
            Utils.exec(this.#cmd)
        } else {
            App.closeWindow("powermenu")
            App.openWindow("verification")
        }
    }

    readonly shutdown = () => {
        this.action("shutdown")
    }

    readonly exec = () => {
        App.closeWindow("verification")
        Utils.exec(this.#cmd)
    }
}

const powermenu = new PowerMenu
Object.assign(globalThis, { powermenu })
export default powermenu
