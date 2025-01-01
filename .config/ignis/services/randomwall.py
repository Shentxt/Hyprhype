import os
import random
import requests
from bs4 import BeautifulSoup
import json
from ignis.services.wallpaper import WallpaperService  
from services.material import MaterialService  

class WallpaperManager:
    def __init__(self):
        self.wallpaper_directory = os.path.expanduser('~') + '/Pictures/Wallpapers/'
        self.history_file = os.path.expanduser('~') + '/.cache/ignis/history.json'
        
        self.wallpaper_service = WallpaperService.get_default()
        self.material_service = MaterialService.get_default()

    def change_wallpaper(self, file_path):
        print(f"Wallpaper change: {file_path}")
        
        self.wallpaper_service.set_wallpaper(file_path)
        
        self.material_service.generate_colors(file_path)

    def fetch_wallpapers(self):
        BASE_URL = "https://old.reddit.com/r/wallpapers/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(BASE_URL, headers=headers)

        if response.status_code == 200:
            print("Successfully fetched wallpapers from Reddit (old version)")
            self.parse_wallpapers(response.text)
        else:
            print(f"Error fetching wallpapers: {response.status_code}")

    def parse_wallpapers(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        image_links = []

        for link in soup.find_all('a', {'href': True}):
            url = link['href']
            if url.endswith(('.jpg', '.png')):
                image_links.append(url)

        print(f"Found {len(image_links)} image URLs.")

        downloaded_images = self.load_downloaded_images()

        new_images = [url for url in image_links if url not in downloaded_images]

        if new_images:
            selected_image = random.choice(new_images)
            print(f"Selected image URL: {selected_image}")
            self.download_image(selected_image)
            self.add_to_downloaded_images(selected_image)
        else:
            print("No new images found.")

    def download_image(self, image_url):
        try:
            file_name = os.path.basename(image_url)

            if not os.path.exists(self.wallpaper_directory):
                os.makedirs(self.wallpaper_directory)

            file_path = os.path.join(self.wallpaper_directory, file_name)

            response = requests.get(image_url)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Wallpaper successfully downloaded to: {file_path}")
                self.change_wallpaper(file_path)  # Aplicamos el wallpaper y los colores
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading wallpaper: {e}")

    def load_downloaded_images(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                return json.load(file)
        return []

    def add_to_downloaded_images(self, image_url):
        downloaded_images = self.load_downloaded_images()
        downloaded_images.append(image_url)
        with open(self.history_file, 'w') as file:
            json.dump(downloaded_images, file)

wallpaper_manager = WallpaperManager()
wallpaper_manager.fetch_wallpapers()
