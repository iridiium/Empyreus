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


class MainRun:
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
                "trading_station": 2,
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
            self.board,
            self.font,
            self.font_size,
            (4, 1),
            (self.board.get_size()[0] / 4, 40),
            (8, 8),
            self.players,
            self.colours["white"],
            self.colours["dark_purple"],
        )
        self.ui_text = UIText(
            self.board,
            self.font,
            self.font_bold,
            self.font_size,
            self.font_size * 2,
            self.players,
            self.colours["white"],
        )

        self.total_turns = 0
        self.running = True

    def run_game_loop(self):
        pygame.init()

        while self.running:
            self.window.fill(self.colours["white"])
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
                        valid_move = curr_player.move(
                            mouse_board_coord, curr_player_pos
                        )

                        if valid_move:
                            self.players.cycle_curr()
                            self.total_turns += 1
                    elif action_idx := self.ui_actions.check_for_action(
                        mouse_pos
                    ):
                        self.ui_actions.handle_action(action_idx)

            self.ui_actions.render_to(self.window)

            self.ui_text.render_to(
                self.window, self.total_turns, curr_player, mouse_pos
            )

            self.board.render_to(self.window, mouse_board_coord, curr_player)

            for player_num, player in enumerate(self.players.get_list()):
                player.render_to(self.window)

            pygame.display.flip()

            self.clock.tick(100)
