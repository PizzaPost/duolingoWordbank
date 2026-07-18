import easypygamewidgets as epw
import pygame

import variables

def update_join_button():
    if variables.widgets["lobbycode"].text.strip() != "" and variables.widgets["playername"].text.strip() != "":
        variables.widgets["join"].configure(state="enabled")
    else:
        variables.widgets["join"].configure(state="disabled")

def react():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            variables.running = False
        epw.handle_event(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            variables.running = False
    epw.handle_special_events()