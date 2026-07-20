import easypygamewidgets as epw
import pygame

import soundEngine
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
        if keys[pygame.K_ESCAPE] and variables.screen == "main":
            variables.running = False
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        colliding_with_widget = False
        for widget in epw.misc.all_widgets:
            if not isinstance(widget, tuple):
                if hasattr(widget, "is_hovered"):
                    if widget.is_hovered:
                        colliding_with_widget = True
                        break
        dx, dy = mx - variables.vinyl_x, my - variables.vinyl_y
        if not colliding_with_widget:
            if (dx ** 2 + dy ** 2) <= variables.vinyl_width ** 2:
                variables.vinyl_rotating = not variables.vinyl_rotating
                soundEngine.get_spotify_embed_preview(variables.vinyl_track)
                if variables.vinyl_rotating:
                    if soundEngine.play(variables.temp_path):
                        variables.vinyl_rotating = False
                else:
                    soundEngine.pause()
    epw.handle_special_events()