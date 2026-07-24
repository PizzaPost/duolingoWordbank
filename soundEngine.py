import os
import re
import tempfile

import pygame
import requests

import variables

mixer_ready = False

played_ms_before_pause = 0
segment_start_tick = 0


def ensure_mixer():
    global mixer_ready
    if not mixer_ready:
        pygame.mixer.init()
        mixer_ready = True


def play(path):
    global played_ms_before_pause, segment_start_tick
    ensure_mixer()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    played_ms_before_pause = 0
    segment_start_tick = pygame.time.get_ticks()


def pause():
    global played_ms_before_pause
    ensure_mixer()
    played_ms_before_pause = get_elapsed_ms()
    pygame.mixer.music.pause()


def resume():
    global segment_start_tick
    ensure_mixer()
    pygame.mixer.music.unpause()
    segment_start_tick = pygame.time.get_ticks()


def is_busy() -> bool:
    ensure_mixer()
    return pygame.mixer.music.get_busy()


def get_elapsed_ms() -> int:
    if not pygame.mixer.music.get_busy():
        return played_ms_before_pause
    return played_ms_before_pause + (pygame.time.get_ticks() - segment_start_tick)


def get_spotify_embed_preview(track_url):
    track_id = track_url.split("/")[-1].split("?")[0]
    cached_path = os.path.join(variables.cache_dir, f"{track_id}.mp3")
    if os.path.exists(cached_path):
        variables.temp_path = cached_path
        return True
    embed_url = f"https://open.spotify.com/embed/track/{track_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(embed_url, headers=headers)
        match = re.search(r'"audioPreview"\s*:\s*\{\s*"url"\s*:\s*"([^"]+)"', response.text)
        if not match:
            return False
        preview_url = match.group(1)
        audio_data = requests.get(preview_url).content
    except requests.RequestException:
        return False
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".mp3", dir=variables.cache_dir)
    with os.fdopen(tmp_fd, "wb") as f:
        f.write(audio_data)
    os.replace(tmp_path, cached_path)
    variables.temp_path = cached_path
    return True