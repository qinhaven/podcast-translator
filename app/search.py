import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("LISTEN_NOTES_API_KEY")
BASE_URL = "https://listen-api.listennotes.com/api/v2"

HEADERS = {
    "X-ListenAPI-Key": API_KEY
}

def search_podcast(query, max_results=5):
    url = f"{BASE_URL}/search"
    params = {"q": query, "type": "episode", "len_min": 5, "sort_by_date": 0}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])[:max_results]

def download_episode_mp3(audio_url, output_path="downloaded_episode.mp3"):
    response = requests.get(audio_url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path