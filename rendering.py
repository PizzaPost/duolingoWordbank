import math

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


def update_vinyl_position(dt):
    if variables.vinyl_target_x is None or variables.vinyl_target_y is None: return
    ease = 1 - math.pow(1 - (1 / 20), dt / 0.01)
    variables.vinyl_x += (variables.vinyl_target_x - variables.vinyl_x) * ease
    variables.vinyl_y += (variables.vinyl_target_y - variables.vinyl_y) * ease


def draw_menu():
    pygame.draw.circle(variables.pg, (0, 0, 0),
                       (variables.vinyl_x, variables.vinyl_y), variables.vinyl_width)
    pygame.draw.circle(variables.pg, variables.vinyl_color, (variables.vinyl_x, variables.vinyl_y),
                       variables.vinyl_width // 3.5)
    rotated_cover = pygame.transform.rotozoom(variables.assets["cover"], variables.vinyl_rotation, 1)
    cover_rect = rotated_cover.get_rect(center=(variables.vinyl_x, variables.vinyl_y))
    variables.pg.blit(rotated_cover, cover_rect)
    pygame.draw.circle(variables.pg, (0, 0, 0), (variables.vinyl_x, variables.vinyl_y), 15)
    variables.vinyl_rotation += 1


def render():
    dt = variables.clock.get_time() / 1000
    draw_vertical_gradient(variables.pg, variables.bg_top, variables.bg_bottom)
    if variables.screen in ("main", "lobby"):
        update_vinyl_position(dt)
        draw_menu()
    epw.flip()