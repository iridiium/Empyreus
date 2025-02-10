from __future__ import annotations

# avoiding circular imports in type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import PlayerList

    from ..game.board import Board
    from ..game.background import Background
    from ..game.shop import Shop

    from ..ui.actions import UIActions
    from ..ui.background import Background
    from ..ui.text import UIText

import pygame
import random
import sys

from .game.helper import gen_colour, merge_sort

from .ui.actions import UIActions
from .ui.text import UIText


class SceneManager:
    def __init__(
        self,
        window: pygame.Surface,
        window_size: tuple[int, int],
        background: Background,
        board: Board,
        players: PlayerList,
        shop: Shop,
        font_size: int,
        font_bold_size: int,
        font: pygame.freetype.Font,
        font_bold: pygame.freetype.Font,
        colours: dict[str, tuple[int, int, int]],
        text_colour: tuple[int, int, int],
    ):
        self.window = window
        self.window_size = window_size
        self.background = background
        self.board = board
        self.players = players
        self.shop = shop
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
                {"name": "Shop", "func": lambda: self.set_scene("shop")},
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
        self.scene_name = "title"
        self.status = ""
        self.status_desc = ""
        self.winner = ""

        with open("./core/tutorial.txt") as f:
            self.help_text = f.read().splitlines()

        self.names = [
            "Aloysius",
            "Bartholomew",
            "Cuthbert",
            "Desmond",
            "Ezekiel",
            "Florian",
            "Godfrey",
            "Horatio",
            "Ignatius",
            "Jeremias",
            "Kensington",
            "Lysander",
            "Margaret",
            "Nathaniel",
            "Octavius",
            "Peregrine",
            "Quentin",
            "Reginald",
            "Sebastian",
            "Thaddeus",
            "Umbro",
            "Vanderbilt",
            "Xander",
            "Yorick",
            "Zephyr",
        ]

        self.clock = pygame.time.Clock()

    def set_scene(self, new_scene) -> None:
        self.scene_name = new_scene

    def handle_actions(self) -> None:
        while self.running:
            self.window.blit(self.background.image, self.background.rect)

            # Calls the correct scene function for the value in self.scene_name.
            # Functions like a five-branch if statement.
            {
                "end": lambda: self.end_scene(),
                "game": lambda: self.game_scene(),
                "help": lambda: self.help_scene(),
                "shop": lambda: self.shop_scene(),
                "title": lambda: self.title_scene(),
            }[self.scene_name]()

            # Updates the contents of the whole display.
            pygame.display.flip()

            # Sets the game FPS to 60.
            self.clock.tick(60)

    def end_scene(self) -> None:
        # Renders text showing who won.
        title_text = self.font_bold.render(
            f"P{self.winner_num + 1} ({self.winner_name}) WINS",
            self.text_colour,
            size=50,
        )
        title_text[1].center = (
            self.window_size[0] / 2,
            self.window_size[1] / 2,
        )
        self.window.blit(title_text[0], title_text[1])

        # Renders text showing how to start a new game.
        instruction_text = self.font.render(
            "Enter the number of players (1 to 5) to start a new game.",
            self.text_colour,
        )
        instruction_text[1].center = (
            self.window_size[0] / 2,
            self.window_size[1] * 0.75,
        )
        self.window.blit(instruction_text[0], instruction_text[1])

        for event in pygame.event.get():
            if not self.running:
                # Quit game if game flow stopped.
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop game flow when designated key pressed.
                    self.running = False
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    # If a number key from one to five is pressed,
                    # remove all players from the list and add new ones in.
                    self.players.clear()

                    self.selected_names = random.sample(
                        self.names, event.key - 48
                    )

                    for selected_name in self.selected_names:
                        self.players.add(selected_name, gen_colour())

                    self.scene_name = "game"

    def game_scene(self) -> None:
        # When a player has won, show this on the end game screen.

        # Sort the players by score ascending, then take the last (highest-scoring) player.
        highest_scoring_player = merge_sort(
            self.players.get_list(), lambda a, b: a.get_score() < b.get_score()
        )[-1]

        if highest_scoring_player.get_score() >= 5:
            # If the winning score threshold has been surpassed,
            # Setup the attributes to show the winning player on the end scene.
            self.scene_name = "end"
            self.winner_num = highest_scoring_player.get_num()
            self.winner_name = highest_scoring_player.get_name()

        mouse_pos = pygame.mouse.get_pos()
        mouse_board_coord = self.board.board_pos_from_coord(mouse_pos)

        curr_player = self.players.get_curr()
        curr_player_pos = curr_player.get_pos()

        for event in pygame.event.get():
            if not self.running:
                # Quit game if game flow stopped.
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Stop game flow when designated key pressed.
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    mouse_board_coord[0] is not None
                    and mouse_board_coord[1] is not None
                ):
                    actions_left = curr_player.move(
                        mouse_board_coord, curr_player_pos
                    )

                    if actions_left <= 0:
                        self.players.cycle_curr()
                elif action_idx := self.ui_actions.check_for_action(mouse_pos):
                    self.actions[action_idx[1]][action_idx[0]]["func"]()

        self.ui_actions.render_to(self.window)

        self.ui_text.render_to(self.window, mouse_pos, curr_player)

        self.board.render_to(self.window, mouse_board_coord, curr_player)

        for player_num, player in enumerate(self.players.get_list()):
            player.render_to(self.window)

    def help_scene(self) -> None:
        help_text_pos = (60, 60)

        self.font_bold.render_to(
            self.window,
            help_text_pos,
            f"HELP:",
            self.text_colour,
        )

        for help_text_line_idx, help_text_line in enumerate(self.help_text):
            # Render each of the guide's individual line of text.
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
                # Quit game if game flow stopped.
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Stop game flow when designated key pressed.
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Return to game when scene clicked.
                self.scene_name = "game"

    def shop_scene(self) -> None:
        shop_text_pos = (60, 60)

        self.font_bold.render_to(
            self.window,
            shop_text_pos,
            "SHOP:",
            self.text_colour,
        )

        shop_products_text_pos = (60, 120)
        shop_products_text_spacing = 2.5 * self.font_size

        for product_idx, product in enumerate(self.shop.get_products()):
            # Render each individual product's line of text.

            # Render index and name.
            self.font.render_to(
                self.window,
                (
                    shop_products_text_pos[0],
                    shop_products_text_pos[1]
                    + product_idx * shop_products_text_spacing,
                ),
                f"{product_idx + 1}     {product.get_name()}",
                self.text_colour,
            )

            # Render image.
            self.window.blit(
                pygame.transform.scale(
                    product.get_icon_image(), (self.font_size, self.font_size)
                ),
                (
                    shop_products_text_pos[0] + 10 * self.font_size,
                    shop_products_text_pos[1]
                    + product_idx * shop_products_text_spacing,
                ),
            )

            # Render cost.
            self.font.render_to(
                self.window,
                (
                    shop_products_text_pos[0] + 11 * self.font_size,
                    shop_products_text_pos[1]
                    + product_idx * shop_products_text_spacing,
                ),
                "    "
                + ", ".join(
                    [
                        f"{value} {key}"
                        for key, value in product.get_cost().items()
                    ]
                ),
                self.text_colour,
            )

            # Render effect description.
            self.font.render_to(
                self.window,
                (
                    shop_products_text_pos[0] + 30 * self.font_size,
                    shop_products_text_pos[1]
                    + product_idx * shop_products_text_spacing,
                ),
                product.get_effect_desc(),
                self.text_colour,
            )

        # Render status of the last purchase (success / reason of failure).
        self.font.render_to(
            self.window,
            (shop_text_pos[0], self.window_size[1] - shop_text_pos[1]),
            self.status_desc if self.status else "",
            self.text_colour,
        )

        curr_player = self.players.get_curr()

        for event in pygame.event.get():
            if not self.running:
                # Quit game if game flow stopped.
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop game flow when designated key pressed.
                    self.running = False
                # Conditions for handling the player buying a product.
                # Checks for the key press of a product's index.
                elif event.key in self.shop.get_idxs_ascii():
                    # Checks for the plaer being on a trading station.
                    if self.board.get_type_from_board_pos(
                        curr_player.get_pos()
                    ).startswith("trader"):
                        # Checks for the player having sufficient resources.
                        if self.shop.check_product_reqs(
                            curr_player,
                            product_idx := event.key
                            - 48,  # Subtracts 48 for ASCII conversion.
                        ):
                            self.shop.buy_product(curr_player, product_idx)
                            self.status = "purchase_success"
                            self.status_desc = (
                                f"Product {product_idx} purchased successfully."
                            )
                        else:
                            self.status = (
                                "purchase_failure_insufficient_resources"
                            )
                            self.status_desc = f"Insufficient resources for product {product_idx}."
                    else:
                        self.status = "purchase_failure_incorrect_location"
                        self.status_desc = (
                            f"Insufficient location, must be on a trader tile."
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Return to game when scene clicked.
                self.scene_name = "game"

    def title_scene(self) -> None:
        title_text = self.font_bold.render(
            "EMPYREUS",
            self.text_colour,
            size=100,
        )
        title_text[1].center = (
            self.window_size[0] / 2,
            self.window_size[1] / 2,
        )

        self.window.blit(title_text[0], title_text[1])

        instruction_text = self.font.render(
            "Enter the number of players (1 to 5) to start a new game.",
            self.text_colour,
        )
        instruction_text[1].center = (
            self.window_size[0] / 2,
            self.window_size[1] * 0.75,
        )

        self.window.blit(instruction_text[0], instruction_text[1])

        for event in pygame.event.get():
            if not self.running:
                # Quit game if game flow stopped.
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop game flow when designated key pressed.
                    self.running = False
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    self.selected_names = random.sample(
                        self.names, event.key - 48
                    )

                    for selected_name in self.selected_names:
                        self.players.add(selected_name, gen_colour())

                    self.scene_name = "game"
