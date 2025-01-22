import pygame
import sys


from .ui.actions import UIActions
from .ui.text import UIText


class SceneManager:
    def __init__(
        self,
        window,
        window_size,
        background,
        board,
        players,
        font_size,
        font_bold_size,
        font,
        font_bold,
        colours,
        text_colour,
    ):
        self.window = window
        self.window_size = window_size
        self.background = background
        self.board = board
        self.players = players
        self.font = font
        self.font_size = font_size
        self.font_bold_size = font_bold_size
        self.font = font
        self.font_bold = font_bold
        self.colours = colours
        self.text_colour = text_colour

        self.actions = [
            [
                {
                    "name": "Help",
                    "func": lambda: self.set_scene("help"),
                },
                {
                    "name": "Trade",
                    "func": lambda: self.players.get_curr().trade(),
                },
                {"name": "Buy", "func": lambda: self.players.buy()},
                {"name": "End", "func": lambda: self.players.cycle_curr()},
            ],
        ]

        self.ui_actions = UIActions(
            board=self.board,
            players=self.players,
            action_names=[
                [action["name"] for action in action_row]
                for action_row in self.actions
            ],
            dims=(4, 1),
            font=self.font,
            font_size=self.font_size,
            elem_base_size=(self.board.get_size()[0] / 4, 40),
            elem_border_size=(8, 8),
            text_colour=self.colours["dark_purple"],
            background_colour=self.colours["white"],
        )
        self.ui_text = UIText(
            board=self.board,
            players=self.players,
            font=self.font,
            font_bold=self.font_bold,
            font_size=self.font_size,
            font_bold_size=self.font_size * 2,
            text_colour=self.text_colour,
        )

        self.running = True
        self.scene = "title"

    def set_scene(self, new_scene):
        self.scene = new_scene

    def manage_scenes(self):
        self.window.blit(self.background.image, self.background.rect)

        if self.scene == "game":
            self.game_scene()
        elif self.scene == "help":
            self.help_scene()
        elif self.scene == "title":
            self.title_scene()

        pygame.display.flip()

    def game_scene(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_board_coord = self.board.board_pos_from_coord(mouse_pos)

        curr_player = self.players.get_curr()
        curr_player_pos = curr_player.get_pos()

        for event in pygame.event.get():
            if not self.running:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
                    self.actions[action_idx[1]][action_idx[0]]["func"]()

        self.ui_actions.render_to(self.window)

        self.ui_text.render_to(self.window, mouse_pos, curr_player)

        self.board.render_to(self.window, mouse_board_coord, curr_player)

        for player_num, player in enumerate(self.players.get_list()):
            player.render_to(self.window)

    def help_scene(self):
        help_text_pos = (20, 20)

        self.font_bold.render_to(
            self.window,
            help_text_pos,
            f"HELP SCREEN",
            self.text_colour,
        )

        help_text = [
            "",
            "Click anywhere to return to the game.",
            "Press ESC to exit the game at any point.",
            "",
            "There are 5 resources to collect.",
            "Resources can be viewed by hovering over the bottom-left corner.",
            "You gain resources by moving onto planets.",
            "Planets have an icon in their top-left corner denoting the resource they yield.",
            "",
            "You, by default, have two actions per turn.",
            "- Moving from one tile to another connected tile (i.e. with a white line) is one action.",
            "- Trading at a trading ship costs one action.",
            "- - At a trading ship, you can exchange 5 of one resource for 3 random resources.",
            "- - The resource taken by a trading ship is denoted by the icon in its top-left corner.",
        ]

        for help_text_line_idx, help_text_line in enumerate(help_text):
            self.font.render_to(
                self.window,
                (
                    help_text_pos[0],
                    help_text_pos[1]
                    + help_text_line_idx * 1.45 * self.font_size,
                ),
                help_text_line,
                self.text_colour,
            )

        for event in pygame.event.get():
            if not self.running:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scene = "game"

    def title_scene(self):
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
            if not self.running:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scene = "game"
