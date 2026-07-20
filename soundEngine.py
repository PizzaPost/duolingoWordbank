import re
import tempfile
import threading
import time

import pygame
import requests

import variables


def play_threaded(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    try:
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except KeyboardInterrupt:
        return False
    pygame.mixer.quit()
    return True


def play(path):
    threading.Thread(target=play_threaded, args=[path]).start()


def pause():
    pygame.mixer.music.pause()


def get_spotify_embed_preview(track_url):
    track_id = track_url.split("/")[-1].split("?")[0]
    embed_url = f"https://open.spotify.com/embed/track/{track_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(embed_url, headers=headers)
    match = re.search(r'"audioPreview"\s*:\s*\{\s*"url"\s*:\s*"([^"]+)"', response.text)
    if not match: return False
    preview_url = match.group(1)
    audio_data = requests.get(preview_url).content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_data)
        variables.temp_path = temp_audio.name
    return True