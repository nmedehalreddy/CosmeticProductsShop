import requests
import os

SKETCHFAB_TOKEN = os.getenv("SKETCHFAB_TOKEN")
API_URL = "https://api.sketchfab.com/v3/search?type=models&license=CC0&downloadable=true"

headers = {
    "Authorization": f"Token {SKETCHFAB_TOKEN}"
}

def fetch_assets():
    response = requests.get(API_URL, headers=headers)
    results = response.json()["results"]
    for model in results:
        title = model["name"].replace(" ", "_")
        download_url = model.get("archives", {}).get("gltf", {}).get("url")
        if download_url:
            r = requests.get(download_url)
            with open(f"static/assets/3d/{title}.zip", "wb") as f:
                f.write(r.content)

if __name__ == "__main__":
    os.makedirs("static/assets/3d", exist_ok=True)
    fetch_assets()
