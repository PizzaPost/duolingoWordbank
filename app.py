if __name__ != "__main__":
    import rendering
    import easypygamewidgets as epw
    import interactions
    import vars
    import pygame

    pygame.init()
    test_screen = 3
    match test_screen:
        case 0:
            vars.pg = pygame.display.set_mode((1511, 850), vsync=1)
        case 1:
            vars.pg = pygame.display.set_mode((1180, 1100), vsync=1)
        case 2:
            vars.pg = pygame.display.set_mode((3840, 2160), vsync=1)
        case _:
            vars.pg = pygame.display.set_mode(vsync=1)
    epw.link_pygame_window(vars.pg)
    vars.clock = pygame.time.Clock()
    vars.running = True


def main():
    while vars.running:
        interactions.react()
        rendering.render()
    pygame.quit()
    exit(0)