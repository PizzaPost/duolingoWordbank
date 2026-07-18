if __name__ != "__main__":
    import rendering
    import easypygamewidgets as epw
    import interactions
    import variables
    import pygame
    import functions

    pygame.init()
    test_screen = 3
    match test_screen:
        case 0:
            variables.pg = pygame.display.set_mode((1511, 850), vsync=1)
        case 1:
            variables.pg = pygame.display.set_mode((1180, 1100), vsync=1)
        case 2:
            variables.pg = pygame.display.set_mode((3840, 2160), vsync=1)
        case _:
            variables.pg = pygame.display.set_mode(vsync=1)
    variables.width, variables.height = variables.pg.get_size()
    pygame.display.set_caption(variables.app_name)
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))
    epw.link_pygame_window(variables.pg)
    variables.clock = pygame.time.Clock()
    variables.running = True

def create_main_ui():
    for widget in epw.misc.all_widgets:
        if not isinstance(widget, tuple):
            widget.delete()
    variables.widgets.clear()
    variables.widgets.update({"title": epw.Label(text=variables.app_name, anchor_x="center", anchor_y="center", font=epw.Font(font_size=55), layer=1001).rotozoom(1, 25)})
    variables.widgets.update({"lobbycode": epw.Entry(placeholder_text="Enter lobby code", anchor_x="center", anchor_y="center", auto_size=False, width=400).bind("<KEY>", interactions.update_join_button).place(50, 45, mode="%")})
    variables.widgets.update({"playername": epw.Entry(placeholder_text="Enter your name", anchor_x="center", anchor_y="center", auto_size=False, width=400).bind("<KEY>", interactions.update_join_button).place(50, 55, mode="%")})
    variables.widgets.update({"join": epw.Button(text="Join", anchor_x="center", anchor_y="bottom", auto_size=False, width=150).place(50, 95, mode="%")})
    variables.widgets.update({"settings": epw.Button(text="⚙️", anchor_x="right", anchor_y="top", auto_size=False, width=80, height=80, font=epw.font.emoji_font).place(95, 5, mode="%")})

    variables.widgets["title"].place(variables.widgets["lobbycode"].x-5, variables.widgets["lobbycode"].y-5)
    variables.widgets["settings"].place(variables.width-variables.widgets["settings"].y, variables.widgets["settings"].y)


def main():
    create_main_ui()
    while variables.running:
        interactions.react()
        rendering.render()
    pygame.quit()
    exit(0)