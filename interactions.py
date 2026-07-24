import easypygamewidgets as epw
import pygame

import soundEngine
import variables


def update_join_button():
    if variables.widgets["lobbycode"].text.strip() != "" and variables.widgets["playername"].text.strip() != "":
        variables.widgets["join"].configure(state="enabled")
    else:
        variables.widgets["join"].configure(state="disabled")


def is_point_over_vinyl(mx, my):
    dx, dy = mx - variables.vinyl_x, my - variables.vinyl_y
    return (dx ** 2 + dy ** 2) <= variables.vinyl_width ** 2


def is_point_over_any_widget(mx, my):
    for widget in epw.misc.all_widgets:
        if not isinstance(widget, tuple) and hasattr(widget, "is_hovered") and widget.is_hovered:
            return True
    return False


def on_vinyl_clicked():
    state = variables.vinyl_state
    if state in ("idle", "finished"):
        if soundEngine.get_spotify_embed_preview(variables.vinyl_track):
            variables.vinyl_loaded_track = variables.vinyl_track
            soundEngine.play(variables.temp_path)
            variables.vinyl_state = "playing"
            variables.vinyl_rotating = True
    elif state == "playing":
        soundEngine.pause()
        variables.vinyl_state = "paused"
        variables.vinyl_rotating = False
    elif state == "paused":
        soundEngine.resume()
        variables.vinyl_state = "playing"
        variables.vinyl_rotating = True


def react():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            variables.running = False
        epw.handle_event(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and variables.screen == "main":
            variables.running = False
    mx, my = pygame.mouse.get_pos()
    variables.vinyl_hovered = is_point_over_vinyl(mx, my) and not is_point_over_any_widget(mx, my)
    if pygame.mouse.get_just_released()[0]:
        if variables.vinyl_hovered:
            on_vinyl_clicked()
    if variables.vinyl_state == "playing" and not soundEngine.is_busy():
        variables.vinyl_state = "finished"
        variables.vinyl_rotating = False
    epw.handle_special_events()