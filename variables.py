import datetime
import os
import random
import tempfile

import pygame

running: bool = None
clock: pygame.Clock = None
pg: pygame.Surface = None
app_name: str = "AppName"
width: int = None
height: int = None
widgets: dict = {}
bg_top = (18, 14, 22)
bg_bottom = (32, 20, 24)
screen: str = "menu"
is_host: bool = False
bg_time: float = 0.0
temp_path = None
hand_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
arrow_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
cursor_is_hand = False
cache_dir = os.path.join(tempfile.gettempdir(), f"{app_name}_cache")
os.makedirs(cache_dir, exist_ok=True)

vinyl_color = tuple(random.randint(0, 255) for x in range(3))
vinyl_x = None
vinyl_y = None
vinyl_target_x = None
vinyl_target_y = None
vinyl_width = 400
vinyl_rotation = 0
vinyl_rotating = False
vinyl_track = None
vinyl_state: str = "idle"
vinyl_loaded_track: str | None = None
vinyl_hovered: bool = False
lobby_row_spawn_times: dict = {}

genre: str = "pop"
timespan_to: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
timespan_from: datetime.datetime = timespan_to - datetime.timedelta(weeks=5300)
required_to_win = 10
fitting_releases = []

glow_color = (240, 226, 210)

assets = {"cover": pygame.image.load("assets/cover.png")}

GENRES = ["pop", "rock", "hip-hop", "r-n-b", "indie", "electronic", "house", "techno", "jazz", "classical", "metal",
          "punk", "country", "folk", "reggae", "latin", "k-pop", "afrobeat"]