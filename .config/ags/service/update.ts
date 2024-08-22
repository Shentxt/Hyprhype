import { sh, bash } from "lib/utils"
import icons from "lib/icons"
import apps from "lib/apps"

class UpdateChecker extends Service {
    static {
        Service.register(this, {}, {
            "updateCount": ["number", "r"],
        })
    }

    #updateCount: number = 0
    #lastUpdateCount: number = 0
    #intervalId: number | null = null
    #notificationShown: boolean = false // Flag to control notification display
    #pacmanCount: number = 0 // New field to store pacman updates count
    #yayCount: number = 0 // New field to store yay updates count
    #subscribers: Array<(updateCount: number) => void> = []

    constructor() {
        super()
        this.checkForUpdates()
        this.startInterval()
    }

    async checkForUpdates() {
        console.log("Checking for updates...")
        try {
            const checkupdates = await sh("bash -c 'checkupdates 2> /dev/null | wc -l'")
            const paru = await sh("bash -c 'yay -Qua 2> /dev/null | wc -l'")

            this.#pacmanCount = parseInt(checkupdates.trim(), 10) || 0
            this.#yayCount = parseInt(paru.trim(), 10) || 0
            
            const totalUpdates = this.#pacmanCount + this.#yayCount
            
            if (!isNaN(totalUpdates)) {
                this.#updateCount = totalUpdates
                this.changed("updateCount")
                console.log(`Pacman updates: ${this.#pacmanCount}, Yay updates: ${this.#yayCount}, Total updates: ${this.#updateCount}`)
                
                // Notify subscribers of the update count change
                this.#subscribers.forEach(callback => callback(this.#updateCount))

                // Mostrar notificación si hay actualizaciones
                if (this.#updateCount > this.#lastUpdateCount) {
                    this.#notificationShown = true // Set flag to true when updates are detected
                }
                
                this.#lastUpdateCount = this.#updateCount
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
        console.log("Starting update interval...")
        this.#intervalId = setInterval(() => {
            console.log("Interval triggered...")
            this.checkForUpdates()
            
            // Show notification if updates are available and notification was not shown recently
            if (this.#updateCount > 0 && this.#notificationShown) {
                this.showNotification()
                this.#notificationShown = false // Reset flag after showing notification
            }
        }, 10000) // 10 seconds
    }

    stopInterval() {
        if (this.#intervalId !== null) {
            clearInterval(this.#intervalId)
            this.#intervalId = null
            console.log("Update interval stopped.")
        }
    }

    showNotification() {
        console.log("Showing notification...")
        Utils.notify({
            image: icons.custom.fuuka, 
            summary: `Updates ${this.#updateCount} Available`,
            body: `Pacman: ${this.#pacmanCount}\nYay: ${this.#yayCount}`,
            actions: {
                "Check Updates": () => sh(apps.execs.update.value),
            },
        })
    }

    get updateCount() { 
        return this.#updateCount 
    }

    subscribe(callback: (updateCount: number) => void) {
        this.#subscribers.push(callback)
    }
}

export default new UpdateChecker()
