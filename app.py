import math

if __name__ != "__main__":
    import rendering
    import easypygamewidgets as epw
    import interactions
    import variables
    import pygame
    import functions
    import networking
    import re

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

    functions.get_album_art()


def clear_widgets(exceptions=[]):
    for widget in list(epw.misc.all_widgets):
        if not isinstance(widget, tuple) and not widget in exceptions:
            widget.delete()


def create_main_ui():
    variables.screen = "main"
    clear_widgets()
    if variables.vinyl_x is None:
        variables.vinyl_x = variables.width * 0.75
        variables.vinyl_y = variables.height * 0.75
    else:
        variables.vinyl_target_x = variables.width * 0.75
        variables.vinyl_target_y = variables.height * 0.75

    variables.widgets.update({"title": epw.Label(text=variables.app_name, anchor_x="center", anchor_y="center",
                                                 font=epw.Font(font_size=55, bold=True), layer=1001).rotozoom(1, 25)})
    variables.widgets.update({"lobbycode": epw.Entry(placeholder_text="Enter lobby code", anchor_x="center",
                                                     anchor_y="center", auto_size=False, width=400).bind("<KEY>",
                                                                                                         interactions.update_join_button).place(
        50, 45, mode="%")})
    variables.widgets.update({"playername": epw.Entry(placeholder_text="Enter your name", anchor_x="center",
                                                      anchor_y="center", auto_size=False, width=400).bind("<KEY>",
                                                                                                          interactions.update_join_button).place(
        50, 55, mode="%")})
    variables.widgets.update({"join": epw.Button(text="Join", state="disabled", anchor_x="center", anchor_y="bottom",
                                                 auto_size=False, width=150, command=on_join_pressed).place(50, 95,
                                                                                                            mode="%")})
    variables.widgets.update({"settings": epw.Button(text="⚙️", anchor_x="right", anchor_y="top", auto_size=False,
                                                     width=80, height=80, font=epw.font.emoji_font).place(95, 5,
                                                                                                          mode="%")})
    variables.widgets["title"].place(variables.widgets["lobbycode"].x - 5, variables.widgets["lobbycode"].y - 5)
    variables.widgets["settings"].place(variables.width - variables.widgets["settings"].y,
                                        variables.widgets["settings"].y)

    functions.set_text_color(variables.widgets["title"], (240, 226, 210))


def on_join_pressed():
    code = variables.widgets["lobbycode"].text.strip()
    name = variables.widgets["playername"].text.strip()
    networking.on_member_update = refresh_lobby_ui
    networking.on_round_start = create_round_ui
    variables.is_host = True
    networking.join_lobby(code, name)
    create_lobby_ui()


def create_lobby_ui():
    variables.screen = "lobby"
    clear_widgets()
    variables.vinyl_target_x = variables.width / 1.7
    variables.vinyl_target_y = variables.height / 1.7

    variables.widgets.update({"lobby_title": epw.Label(text="Lobby", anchor_x="left", anchor_y="top",
                                                       font=epw.Font(font_size=40, bold=True))
                             .place(5, 5, mode="%")})
    variables.widgets.update({"lobby_code_label": epw.Label(
        text=f"Code: {re.sub(r"[a-zA-Z0-9]", "*", str(networking.session_code))}", anchor_x="right",
        anchor_y="top", font=epw.Font(font_size=20))
                             .bind("<RELEASE>", functions.copy_lobby_code)
                             .place(95, 5, mode="%")})
    variables.widgets.update({"ready_label": epw.Label(text="", anchor_x="left", anchor_y="bottom",
                                                       font=epw.Font(font_size=18))
                             .place(5, 80, mode="%")})

    variables.widgets.update({"ready": epw.Button(text="Ready", anchor_x="left", anchor_y="bottom", auto_size=False,
                                                  width=220, command=on_start_pressed)
                             .place(5, 95, mode="%")})
    variables.widgets.update({"leave": epw.Button(text="Leave lobby", anchor_x="right", anchor_y="bottom",
                                                  auto_size=False, width=220, command=on_leave_pressed)
                             .place(95, 95, mode="%")})

    variables.widgets["ready_label"].place(variables.widgets["ready_label"].x, variables.widgets["ready"].y - 15)

    functions.set_text_color(variables.widgets["lobby_title"], (240, 226, 210))
    functions.set_text_color(variables.widgets["lobby_code_label"], (200, 178, 150))
    functions.set_text_color(variables.widgets["ready_label"], (200, 178, 150))

    refresh_lobby_ui()


def refresh_lobby_ui():
    if variables.screen != "lobby":
        return
    for key in list(variables.widgets.keys()):
        if key.startswith("player_"):
            variables.widgets[key].delete()
            del variables.widgets[key]
    members = networking.get_members()
    for i, (cid, info) in enumerate(sorted(members.items())):
        y_pos = 12 + i * 6
        tag = " (you)" if cid == networking.client_id else ""
        tag += " - ready" if cid in networking.ready else ""
        label = epw.Label(text=f"{info["display_name"]}{tag}", anchor_x="left", anchor_y="top",
                          font=epw.Font(font_size=22)).place(5, y_pos, mode="%")
        functions.set_text_color(label, (240, 226, 210))
        variables.widgets[f"player_{cid}"] = label

    ready_count, total = networking.get_ready_count()
    variables.widgets["ready_label"].configure(
        text=f"{ready_count}/{math.ceil(total / 2)} ready to start").place(5, 80, mode="%")
    variables.widgets["ready_label"].place(variables.widgets["ready_label"].x, variables.widgets["ready"].y - 15)


def on_start_pressed():
    networking.vote_start()
    refresh_lobby_ui()


def on_leave_pressed():
    networking.leave_lobby()
    variables.is_host = False
    create_main_ui()


def create_round_ui():
    variables.screen = "round"
    clear_widgets()
    variables.widgets.update({"round_placeholder": epw.Label(text="Round starting...", anchor_x="center",
                                                             anchor_y="center", font=epw.Font(font_size=40))
                             .place(50, 50, mode="%")})
    functions.set_text_color(variables.widgets["round_placeholder"], (240, 226, 210))


def main():
    create_main_ui()
    while variables.running:
        interactions.react()
        rendering.render()
        variables.clock.tick(120)

    if variables.screen in ("lobby", "round"):
        networking.leave_lobby()
    pygame.quit()
    exit(0)