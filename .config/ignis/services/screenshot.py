import os
import json
import subprocess
import datetime
import argparse

class ScreenshotService:
    def __init__(self):
        self.default_file_location = "~/Pictures"
        self.default_filename = "screenshot_{}.png"
        self.config_file = os.path.expanduser("~/.cache/ignis/screenshots_config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.default_file_location = config.get('file_location', self.default_file_location)
                    self.default_filename = config.get('filename', self.default_filename)
            except Exception:
                pass

    def save_config(self):
        config = {
            'file_location': self.default_file_location,
            'filename': self.default_filename
        }
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception:
            pass

    def set_default_file_location(self, path):
        self.default_file_location = path
        self.save_config()

    def set_default_filename(self, filename):
        self.default_filename = filename
        self.save_config()

    def take_screenshot(self, full_screen=True):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.default_filename.format(timestamp)
        file_path = f"{self.default_file_location}/{filename}"

        if full_screen:
            command = f"sleep 1 && grimblast --notify --freeze copysave output {file_path}"
        else:
            command = f"grimblast --notify --freeze copysave area {file_path}"

        subprocess.run(command, shell=True)
        return file_path

def main():
    parser = argparse.ArgumentParser(description="Servicio de captura de pantalla")
    parser.add_argument('--area', action='store_true', help="Captura una área específica de la pantalla")
    parser.add_argument('--full', action='store_true', help="Captura la pantalla completa")
    parser.add_argument('--path', type=str, help="Especifica la ruta donde guardar la captura")
    parser.add_argument('--filename', type=str, help="Especifica el nombre del archivo de la captura")
    
    args = parser.parse_args()

    screenshot_service = ScreenshotService()

    if args.path:
        screenshot_service.set_default_file_location(args.path)
    if args.filename:
        screenshot_service.set_default_filename(args.filename)

    if args.area:
        screenshot_service.take_screenshot(full_screen=False)
    elif args.full:
        screenshot_service.take_screenshot(full_screen=True)

if __name__ == "__main__":
    main()
