import pygame
import random
running: bool = None
clock: pygame.Clock = None
pg: pygame.Surface = None
app_name: str = "AppName"
width: int = None
height: int = None
widgets: dict = {}
vinyl_color = tuple(random.randint(0, 255 ) for x in range(3))
bg_top = (18, 14, 22)
bg_bottom = (32, 20, 24)
screen: str = "menu"
is_host: bool = False
bg_time: float = 0.0