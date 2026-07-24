import io
import json
import random
import urllib

import pygame
from spotify_scraper import SpotifyClient

import networking
import variables


def set_text_color(widget, color):
    widget.configure(active_unpressed_text_color=color, active_hover_text_color=color, active_pressed_text_color=color,
                     disabled_unpressed_text_color=color, disabled_hover_text_color=color)


def circular_crop(surface: pygame.Surface) -> pygame.Surface:
    size = min(surface.get_width(), surface.get_height())
    square = pygame.Surface((size, size), pygame.SRCALPHA)
    square.blit(surface, ((size - surface.get_width()) // 2, (size - surface.get_height()) // 2))
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
    result = pygame.Surface((size, size), pygame.SRCALPHA)
    result.blit(square, (0, 0))
    result.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return result


def get_album_art(track_url=None):
    if not track_url:
        track_url = random.choice([
            "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC",
            "https://open.spotify.com/track/3Nl5OkkmS5DaBZvuYofpAt",
            "https://open.spotify.com/track/5CZ40GBx1sQ9agT82CLQCT",
            "https://open.spotify.com/track/53iuhJlwXhSER5J2IYYv1W",
            "https://open.spotify.com/track/1BxfuPKGuaTgP7aM0Bbdwr",
            "https://open.spotify.com/track/1R0a2iXumgCiFb7HEZ7gUE",
            "https://open.spotify.com/track/5YqltLsjdqFtvqE7Nrysvs",
            "https://open.spotify.com/track/1ZVp3jxaSfx1eket9duUkZ",
            "https://open.spotify.com/track/6XVSsVuzVUZ2zgRWB5xwef",
            "https://open.spotify.com/track/5qrSlOut2rNAWv3ubArkNy",
            "https://open.spotify.com/track/2VyOhGV0rwqHuCribVSutf",
            "https://open.spotify.com/track/7ygpwy2qP3NbrxVkHvUhXY",
            "https://open.spotify.com/track/1GhbQDYGEOjyFwfT8lojcx",
            "https://open.spotify.com/track/49j6SvuvWfbEKZKzsHCdLJ",
            "https://open.spotify.com/track/3BovdzfaX4jb5KFQwoPfAw",
            "https://open.spotify.com/track/1rIKgCH4H52lrvDcz50hS8",
            "https://open.spotify.com/track/6dOtVTDdiauQNBQEDOtlAB",
            "https://open.spotify.com/track/3QGsuHI8jO1Rx4JWLUh9jd",
            "https://open.spotify.com/track/7ne4VBA60CxGM75vw0EYad",
            "https://open.spotify.com/track/4nyF5lmSziBAt7ESAUjpbx",
            "https://open.spotify.com/track/3di5hcvxxciiqwMH1jarhY"
        ])
        variables.vinyl_track = track_url
    encoded_url = urllib.parse.quote(track_url)
    oembed_endpoint = f"https://open.spotify.com/oembed?url={encoded_url}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(oembed_endpoint, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        image_url = data.get("thumbnail_url")
        if not image_url:
            print("Fehler: Kein Cover im Spotify-Link gefunden.")
            return
        img_req = urllib.request.Request(image_url, headers=headers)
        with urllib.request.urlopen(img_req) as img_response:
            raw_bytes = img_response.read()
        cover_surface = pygame.image.load(io.BytesIO(raw_bytes))
        circular_cover = circular_crop(cover_surface)
        pygame.image.save(circular_cover, "assets/cover.png")
        variables.assets["cover"] = circular_cover
        print(f"Erfolgreich heruntergeladen")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def copy_lobby_code():
    pygame.scrap.put_text(str(networking.session_code))


def update_cursor():
    want_hand = variables.vinyl_hovered
    if want_hand != variables.cursor_is_hand:
        pygame.mouse.set_cursor(variables.hand_cursor if want_hand else variables.arrow_cursor)
        variables.cursor_is_hand = want_hand


def get_fitting_artists():
    limit = variables.required_to_win * 2 + 10
    genre = variables.genre
    timespan_from = variables.timespan_from
    timespan_to = variables.timespan_to

    client = SpotifyClient()
    print(f"Suche nach Künstlern im Genre '{genre}' via Web-Scraping...")
    query = f'genre:"{genre}"'

    try:
        search_results = client.search(query, types=["artist"], limit=limit)
        artists = search_results.artists
    except Exception as e:
        print(f"Fehler bei der Suche: {e}")
        return

    fitting_artists = []
    for artist in artists[:limit]:
        print(artist)
        try:
            full_artist = client.get_artist(artist.id)
            print(f"{artist.name}: albums={len(full_artist.albums)}, singles={len(full_artist.singles)}")
            variables.fitting_releases = []
            for ref in (*full_artist.albums, *full_artist.singles):
                try:
                    album = client.get_album(ref.id)
                    print(f"  {album.name}: release_date={album.release_date}")
                    if album.release_date is not None and timespan_from <= album.release_date <= timespan_to:
                        variables.fitting_releases.append(album)
                except Exception as e:
                    print(f"Fehler beim Laden von Album {ref.id}: {e}")

            if variables.fitting_releases:
                fitting_artists.append({
                    "name": artist.name,
                    "id": artist.id,
                    "releases": variables.fitting_releases,
                })
        except Exception as e:
            print(f"Fehler bei Künstler {artist.name}: {e}")