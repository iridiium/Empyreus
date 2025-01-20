import pygame


class SceneManager:
    def __init__(
        self,
        window,
        window_size,
        background,
        board,
        players,
        font,
        font_bold,
        text_colour,
        ui_actions,
        ui_text,
    ):
        self.window = window
        self.window_size = window_size
        self.background = background
        self.board = board
        self.players = players
        self.font = font
        self.font_bold = font_bold
        self.text_colour = text_colour
        self.ui_actions = ui_actions
        self.ui_text = ui_text

        self.running = True
        self.scene = "title"

    def set_scene(self, new_scene):
        self.scene = new_scene

    def manage_scenes(self):
        if self.scene == "game":
            self.game_scene()
        elif self.scene == "help":
            self.help_scene()
        elif self.scene == "title":
            self.title_scene()

    def game_scene(self):
        self.window.blit(self.background.image, self.background.rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_board_coord = self.board.board_pos_from_coord(mouse_pos)

        curr_player = self.players.get_curr()
        curr_player_pos = curr_player.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    mouse_board_coord[0] is not None
                    and mouse_board_coord[1] is not None
                ):
                    actions_left = curr_player.move(
                        mouse_board_coord, curr_player_pos
                    )

                    if actions_left == 0:
                        self.players.cycle_curr()
                elif action_idx := self.ui_actions.check_for_action(mouse_pos):
                    self.ui_actions.handle_action(action_idx)

        self.ui_actions.render_to(self.window)

        self.ui_text.render_to(self.window, mouse_pos, curr_player)

        self.board.render_to(self.window, mouse_board_coord, curr_player)

        for player_num, player in enumerate(self.players.get_list()):
            player.render_to(self.window)

    def help_scene(self):
        self.title_scene()

    def title_scene(self):
        self.window.blit(self.background.image, self.background.rect)

        title = self.font_bold.render(
            "EMPYREUS",
            self.text_colour,
            size=100,
        )
        title_rect = title[0].get_rect(
            center=(self.window_size[0] / 2, self.window_size[1] / 2)
        )
        self.window.blit(title[0], title_rect)

        instruction = self.font.render(
            "Click anywhere to start.",
            self.text_colour,
        )
        instruction_rect = title[0].get_rect(
            center=(self.window_size[0] / 2, self.window_size[1] * 0.75),
        )
        self.window.blit(instruction[0], instruction_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scene = "game"
