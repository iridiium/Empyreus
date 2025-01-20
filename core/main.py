import pygame
import pygame.freetype

from random import choice, randrange

from .asset_loader import load_assets
from .game.background import Background
from .game.board import Board
from .game.helper import gen_rand_light_colour
from .game.player import Player, PlayerList
from .game.sprite_sheet import SpriteSheet

from .ui.actions import UIActions
from .ui.text import UIText

from .scene_manager import SceneManager


class Main:
    def __init__(self):
        (
            self.background,
            self.sprite_sheet_tiles,
            self.sprite_sheet_resources,
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
        self.players.add("Aloysius", gen_rand_light_colour())
        self.players.add("Bartholomew", gen_rand_light_colour())
        self.players.add("Cuthbert", gen_rand_light_colour())

        self.ui_actions = UIActions(
            board=self.board,
            players=self.players,
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

        self.scene_manager = SceneManager(
            window=self.window,
            window_size=self.window_size,
            background=self.background,
            board=self.board,
            players=self.players,
            font=self.font,
            font_bold=self.font_bold,
            text_colour=self.text_colour,
            ui_actions=self.ui_actions,
            ui_text=self.ui_text,
        )

        self.running = True

    def run_game_loop(self):
        pygame.init()

        while self.running:
            self.scene_manager.manage_scenes()

            pygame.display.flip()
            self.clock.tick(100)
