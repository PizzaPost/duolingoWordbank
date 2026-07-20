import random

import pygame

running: bool = None
clock: pygame.Clock = None
pg: pygame.Surface = None
app_name: str = "AppName"
width: int = None
height: int = None
widgets: dict = {}
vinyl_color = tuple(random.randint(0, 255) for x in range(3))
vinyl_x = None
vinyl_y = None
vinyl_target_x = None
vinyl_target_y = None
vinyl_width = 400
vinyl_rotation = 0
vinyl_rotating = False
vinyl_track = None
bg_top = (18, 14, 22)
bg_bottom = (32, 20, 24)
screen: str = "menu"
is_host: bool = False
bg_time: float = 0.0
temp_path = None

assets = {"cover": pygame.image.load("assets/cover.png")}