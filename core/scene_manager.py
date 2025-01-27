import pygame
import random
import sys

from .game.helper import gen_colour

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
        shop,
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
        self.scene = "title"
        self.status = ""
        self.status_desc = ""

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

    def set_scene(self, new_scene):
        self.scene = new_scene

    def manage_scenes(self):
        self.window.blit(self.background.image, self.background.rect)

        if self.scene == "game":
            self.game_scene()
        elif self.scene == "help":
            self.help_scene()
        elif self.scene == "shop":
            self.shop_scene()
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
        help_text_pos = (60, 60)

        self.font_bold.render_to(
            self.window,
            help_text_pos,
            f"HELP:",
            self.text_colour,
        )

        help_text = [
            "",
            "Click anywhere, at any point, to return to the game.",
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

    def shop_scene(self):
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

            self.font.render_to(
                self.window,
                (
                    shop_products_text_pos[0] + 11 * self.font_size,
                    shop_products_text_pos[1]
                    + product_idx * shop_products_text_spacing,
                ),
                "    "
                + " ".join(
                    [
                        f"{key}: {value}"
                        for key, value in product.get_cost().items()
                    ]
                ),
                self.text_colour,
            )

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

        self.font.render_to(
            self.window,
            (shop_text_pos[0], self.window_size[1] - shop_text_pos[1]),
            self.status_desc if self.status else "",
            self.text_colour,
        )

        curr_player = self.players.get_curr()

        for event in pygame.event.get():
            if not self.running:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in self.shop.get_idxs_ascii():
                    if self.shop.check_product_reqs(
                        curr_player, product_idx := event.key - 48
                    ):
                        self.shop.buy_product(product_idx)
                        self.status = "purchase_success"
                        self.status_desc = (
                            f"Product {product_idx} purchased successfully."
                        )
                    else:
                        self.status = "purchase_failure_insufficient_resources"
                        self.status_desc = (
                            f"Insufficient resources for product {product_idx}."
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scene = "game"

    def title_scene(self):
        title = self.font_bold.render(
            "EMPYREUS",
            self.text_colour,
            size=100,
        )
        title[1].center = (self.window_size[0] / 2, self.window_size[1] / 2)

        self.window.blit(title[0], title[1])

        instruction = self.font.render(
            "Enter the number of players (2 to 5) to start a new game.",
            self.text_colour,
        )
        instruction[1].center = (
            self.window_size[0] / 2,
            self.window_size[1] * 0.75,
        )

        self.window.blit(instruction[0], instruction[1])

        for event in pygame.event.get():
            if not self.running:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif pygame.K_2 <= event.key <= pygame.K_5:
                    self.selected_names = random.sample(
                        self.names, event.key - 48
                    )

                    for selected_name in self.selected_names:
                        self.players.add(selected_name, gen_colour())

                    self.scene = "game"
