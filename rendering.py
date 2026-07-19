import easypygamewidgets as epw
import pygame

import variables


def draw_vertical_gradient(surface, top_color, bottom_color):
    height = surface.get_height()
    width = surface.get_width()
    for y_pos in range(height):
        t = y_pos / max(height - 1, 1)
        color = (round(top_color[0] + (bottom_color[0] - top_color[0]) * t),
                 round(top_color[1] + (bottom_color[1] - top_color[1]) * t),
                 round(top_color[2] + (bottom_color[2] - top_color[2]) * t))
        pygame.draw.line(surface, color, (0, y_pos), (width, y_pos))


def draw_menu():
    vinyl = variables.widgets["vinyl"]
    pygame.draw.circle(variables.pg, variables.vinyl_color,
                       (vinyl.x + vinyl.surface.get_width() // 2 + vinyl.current_offset[0], vinyl.y + vinyl.surface.get_width() // 2 + vinyl.current_offset[1]),
                       vinyl.surface.get_width() // 2 - 50)


def render():
    draw_vertical_gradient(variables.pg, variables.bg_top, variables.bg_bottom)
    if variables.screen in ("main", "lobby"):
        draw_menu()
    epw.flip()