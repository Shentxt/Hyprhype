import { Service, Utils } from "../imports.js";

class Amdctl extends Service {
  static {
    Service.register(
      this,
      {},
      {
        profile: ["string", "r"],
        mode: ["string", "r"],
      },
    );
  }

  nextProfile() {
    Utils.execAsync("amdctl profile -n")
      .then(() => {
        this._profile = Utils.exec("amdctl profile -p").split(" ")[3];
        this.changed("profile");
      })
      .catch(console.error);
  }

  setProfile(prof) {
    Utils.execAsync(`amdctl profile --profile-set ${prof}`)
      .then(() => {
        this._profile = prof;
        this.changed("profile");
      })
      .catch(console.error);
  }

  nextMode() {
    Utils.execAsync(
      `supergfxctl -m ${this._mode === "Hybrid" ? "Integrated" : "Hybrid"}`,
    )
      .then(() => {
        this._mode = Utils.exec("supergfxctl -g");
        this.changed("profile");
      })
      .catch(console.error);
  }

  constructor() {
    super();

    if (Utils.exec("which amdctl")) {
      this.available = true;
      Utils.execAsync(`amdctl profile --profile-set Balanced`);
      this._profile = "Balanced";
      Utils.execAsync("supergfxctl -g").then((mode) => (this._mode = mode));
    } else {
      this.available = false;
      this._profile = "Balanced";
    }
  }

  get profiles() {
    return ["Performance", "Balanced", "Quiet"];
  }
  get profile() {
    return this._profile;
  }
  get mode() {
    return this._mode || "Hybrid";
  }
}

export default new Amdctl();
