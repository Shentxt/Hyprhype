import options from "options"
import { dependencies, sh } from "lib/utils"

const WP = `${Utils.HOME}/.config/background`
const Cache = `${Utils.HOME}/Pictures/Wallpapers`

class Wallpaper extends Service {
    static {
        Service.register(this, {}, {
            "wallpaper": ["string"],
        })
    }

    #blockMonitor = false

    #wallpaper() {
        if (!dependencies("swww"))
            return

        sh("hyprctl cursorpos").then(pos => {
            sh([
                "swww", "img",
                "--invert-y",
                "--transition-type", "grow",
                "--transition-pos", pos.replace(" ", ""),
                WP,
            ]).then(() => {
                this.changed("wallpaper")
            })
        })
    }

    async #setWallpaper(path) {
        this.#blockMonitor = true

        await sh(`cp ${path} ${WP}`)
        this.#wallpaper()

        this.#blockMonitor = false
    }

    async #fetchReddit() {
        const REDDIT_URL = "https://www.reddit.com/r/wallpaper/random.json";

        const response = await Utils.fetch(REDDIT_URL, {
            headers: {
                "User-Agent": "WallpaperFetcher/0.1" 
          } 
        });

        if (!response.ok) {
            return console.warn("Error getting images from Reddit:", response.statusText);
        }

        const data = await response.json();
        const post = data[0].data.children[0].data;

        if (post.url.endsWith('.jpg') || post.url.endsWith('.png')) {
            const file = `${Cache}/${post.url.split('/').pop()}`; 

            if (dependencies("curl")) {
                Utils.ensureDirectory(Cache);
                await sh(`curl "${post.url}" --output ${file}`);
                this.#setWallpaper(file);
            }
        } else {
            console.warn("The post does not contain a valid image.");
        }
    }

    readonly random = () => { this.#fetchReddit() }
    readonly set = (path) => { this.#setWallpaper(path) }
    get wallpaper() { return WP }

    constructor() {
        super()

        if (!dependencies("swww"))
            return this

        // gtk portal
        Utils.monitorFile(WP, () => {
            if (!this.#blockMonitor)
                this.#wallpaper()
        })

        Utils.execAsync("swww-daemon")
            .then(this.#wallpaper)
            .catch(() => null)
    }
}

export default new Wallpaper();
