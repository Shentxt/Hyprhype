import { sh } from "lib/utils"

type Profile = "Performance" | "Balanced" | "Quiet"
type Mode = "Hybrid" | "Integrated" | "AMD"

class PowerManager extends Service {
    static {
        Service.register(this, {}, {
            "profile": ["string", "r"],
            "mode": ["string", "r"],
        })
    }

    #profile: Profile = "Balanced"
    #mode: Mode = "Hybrid"

    get available() {
        return Utils.exec("which asusctl || which amdctl", () => true, () => false)
    }

    showNotification() {
        console.log("Checking CPU info and installed utilities...");

        sh("cat /proc/cpuinfo").then(cpuInfo => {
            const isAMD = cpuInfo.includes("AMD Ryzen");

            sh("which asusctl").then(() => {
                this.#mode = "Asus";
                Utils.notify({
                    image: icons.custom.asus, 
                    summary: `ASUS Control Detected`,
                    body: `Profile: ${this.#profile}\nMode: ${this.#mode}`,
                });
                console.log("Notification sent: ASUS Control Detected"); 
            }).catch(() => {
                if (isAMD) {
                    sh("amdctl -g").then(() => {
                        this.#mode = "AMD";
                        Utils.notify({
                            image: icons.custom.amd, 
                            summary: `AMD Control Detected`,
                            body: `CPU Model: AMD Ryzen\nMode: ${this.#mode}`,
                        });
                        console.log("Notification sent: AMD Control Detected");
                    }).catch(() => {
                        Utils.notify({
                            image: icons.custom.error, 
                            summary: `No Control Utility Found`,
                            body: `Neither ASUS nor AMD control utilities are installed.`,
                        });
                        console.log("Notification sent: No Control Utility Found"); 
                    });
                } else {
                    Utils.notify({
                        image: icons.custom.error, 
                        summary: `No Control Utility Found`,
                        body: `Neither ASUS nor AMD control utilities are installed.`,
                    });
                    console.log("Notification sent: No Control Utility Found"); 
                }
            });
        });
    }

    async nextProfile() {
        if (await this.isAsus()) {
            await sh("asusctl profile -n")
            const profile = await sh("asusctl profile -p")
            const p = profile.split(" ")[3] as Profile
            this.#profile = p
        } 
        this.changed("profile")
    }

    async setProfile(prof: Profile) {
        if (await this.isAsus()) {
            await sh(`asusctl profile --profile-set ${prof}`)
        } 
        this.#profile = prof
        this.changed("profile")
    }

    async nextMode() {
        if (await this.isAsus()) {
            await sh(`supergfxctl -m ${this.#mode === "Hybrid" ? "Integrated" : "Hybrid"}`)
            this.#mode = await sh("supergfxctl -g") as Mode
        } else {
            await sh("amdctl -g")
            this.#mode = "AMD"
        }
        this.changed("mode")
    }

    constructor() {
        super()

        if (this.available) {
            this.isAsus().then(isAsus => {
                if (isAsus) {
                    sh("asusctl profile -p").then(p => this.#profile = p.split(" ")[3] as Profile)
                    sh("supergfxctl -g").then(m => this.#mode = m as Mode)
                } else {
                    sh("amdctl -g").then(() => this.#mode = "AMD")
                }
            })
        }
    }

    get profiles(): Profile[] { return ["Performance", "Balanced", "Quiet"] }
    
    async isAsus(): Promise<boolean> {
        return await sh("which asusctl").then(() => true).catch(() => false)
    }
}

export default new PowerManager()
