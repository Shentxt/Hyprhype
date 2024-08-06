import { sh } from "lib/utils"

class UpdateChecker extends Service {
    static {
        Service.register(this, {}, {
            "updateCount": ["number", "r"],
        })
    }

    #updateCount: number = 0
    #intervalId: number | null = null

    constructor() {
        super()
        this.checkForUpdates()
        this.startInterval()
    }

    async checkForUpdates() {
        try {
            const checkupdates = await sh("bash -c 'checkupdates 2> /dev/null | wc -l'")
            const paru = await sh("bash -c 'yay -Qua 2> /dev/null | wc -l'")
            
            const totalUpdates = parseInt(checkupdates.trim(), 10) + parseInt(paru.trim(), 10)
            if (!isNaN(totalUpdates)) {
                this.#updateCount = totalUpdates
                this.changed("updateCount")
                console.log(`Updated count: ${this.#updateCount}`)
            } else {
                console.error("Failed to parse update count")
                this.#updateCount = 0
                this.changed("updateCount")
            }
        } catch (error) {
            console.error("Error checking for updates:", error)
            this.#updateCount = 0
            this.changed("updateCount")
        }
    }

    startInterval() {
        this.#intervalId = setInterval(() => {
            this.checkForUpdates()
        }, 60000) 
    }

    stopInterval() {
        if (this.#intervalId !== null) {
            clearInterval(this.#intervalId)
            this.#intervalId = null
        }
    }

    get updateCount() { 
        return this.#updateCount 
    }
}

export default new UpdateChecker()
