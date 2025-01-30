import pygame
import pygame.freetype
import sys

from random import choice, randrange

from .game.board import Board
from .game.player import Player, PlayerList
from .game.shop import Shop, Product

from .ui.asset_loader import load_assets
from .ui.background import Background
from .ui.sprite_sheet import SpriteSheet

from .scene_manager import SceneManager


class Main:
    def __init__(self):
        (
            self.background,
            self.sprite_sheet_products,
            self.sprite_sheet_resources,
            self.sprite_sheet_tiles,
            self.font_size,
            self.font_bold_size,
            self.font,
            self.font_bold,
        ) = load_assets()

        self.window_size = (1024, 640)

        self.colours = {
            "white": (255, 255, 255),
            "grey": (116, 117, 114),
            "dark_purple": (16, 1, 41),
        }
        self.text_colour = self.colours["white"]

        self.board_dims = (6, 6)
        self.tile_base_size = (72, 72)
        self.tile_border_size = (8, 8)
        self.tile_size = (80, 80)

        self.num_players = 2

        self.board = Board(
            dims=self.board_dims,
            line_colour=self.colours["white"],
            tile_colour=self.colours["grey"],
            tile_base_size=self.tile_base_size,
            tile_border_size=self.tile_border_size,
            window_size=self.window_size,
            sprite_sheet=self.sprite_sheet_tiles,
            icon_sprite_sheet=self.sprite_sheet_resources,
            tiles={
                "planet_carbon": 3,
                "planet_helium": 3,
                "planet_ice": 3,
                "planet_ore": 3,
                "planet_uranium": 3,
                "asteroid": 2,
                "asteroid_small": 2,
                "trader_A": 1,
                "trader_B": 1,
                "trader_C": 1,
                "empty": float("inf"),
            },
        )

        self.window = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        self.board_pos = self.board.get_pos()

        self.players = PlayerList(
            self.board,
            self.sprite_sheet_resources,
            "./assets/images/tiny-spaceships",
        )
        self.shop = Shop(
            [
                Product(
                    idx="1",
                    name="Engine Upgrade 1",
                    icon_image=self.sprite_sheet_products.get_sprite_from_name(
                        "excavator"
                    ),
                    cost={"helium": 2, "ore": 2, "ice": 1},
                    effect=lambda: self.players.get_curr().change_actions_per_turn_by(
                        1
                    ),
                    score=1,
                    effect_desc="+1 score, +1 action per turn.",
                ),
                Product(
                    idx="2",
                    name="Engine Upgrade 2",
                    icon_image=self.sprite_sheet_products.get_sprite_from_name(
                        "bucket"
                    ),
                    cost={"helium": 3, "ore": 3, "uranium": 2},
                    effect=lambda: self.players.get_curr().change_actions_per_turn_by(
                        2
                    ),
                    score=1,
                    effect_desc="+2 score, +2 actions per turn.",
                ),
            ]
        )

        self.scene_manager = SceneManager(
            window=self.window,
            window_size=self.window_size,
            background=self.background,
            board=self.board,
            players=self.players,
            shop=self.shop,
            font_size=self.font_size,
            font_bold_size=self.font_bold_size,
            font=self.font,
            font_bold=self.font_bold,
            colours=self.colours,
            text_colour=self.text_colour,
        )

        self.running = True

    def run_game_loop(self):
        pygame.init()

        while self.running:
            self.scene_manager.handle_actions()

            self.clock.tick(100)
