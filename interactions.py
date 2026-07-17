import easypygamewidgets as epw
import pygame

import vars


def react():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vars.running = False
        epw.handle_event(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            vars.running = False
    epw.handle_special_events()