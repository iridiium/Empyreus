import pygame

from ..game.board import Board
from ..game.player import Player, PlayerList

from .action_functions import skip_turn


class UIActions:
    def __init__(
        self,
        board: Board,
        font: pygame.freetype.Font,
        font_size: int,
        dims: tuple[int, int],
        elem_size: tuple[int, int],
        elem_border_size: tuple[int, int],
        players: PlayerList,
        colour: tuple[int, int, int],
        text_colour: tuple[int, int, int],
    ):
        self.board = board
        self.font = font
        self.font_size = font_size
        self.dims = dims
        self.elem_base_size = elem_size
        self.elem_border_size = elem_border_size
        self.players = players
        self.colour = colour
        self.text_colour = text_colour

        self.elem_size = (
            self.elem_base_size[0] + self.elem_border_size[0],
            self.elem_base_size[1] + self.elem_border_size[1],
        )

        self.board_pos = self.board.get_pos()
        self.board_pos_end = self.board.get_pos_end()

        self.pos = (self.board_pos[0], self.board_pos_end[1] + 20)
        self.pos_end = (
            self.pos[0] + self.dims[0] * self.elem_size[0],
            self.pos[1] + self.dims[1] * self.elem_size[1],
        )

        self.actions = [
            [
                {"name": "Skip", "function": self.skip_turn},
                {"name": "Skip", "function": self.skip_turn},
                {"name": "Skip", "function": self.skip_turn},
                {"name": "Skip", "function": self.skip_turn},
            ],
        ]

    def check_for_action(self, mouse_pos):
        if not (
            self.pos[0] < mouse_pos[0] < self.pos_end[0]
            and self.pos[1] < mouse_pos[1] < self.pos_end[1]
        ):
            return None

        return (
            int((mouse_pos[0] - self.pos[0]) // self.elem_size[0]),
            int((mouse_pos[1] - self.pos[1]) // self.elem_size[1]),
        )

    def handle_action(self, action_idx):
        return self.actions[action_idx[1]][action_idx[0]]["function"]()

    def render_to(self, window: pygame.display):
        for y in range(self.dims[1]):
            for x in range(self.dims[0]):
                action_rect = pygame.draw.rect(
                    window,
                    self.colour,
                    (
                        self.pos[0] + x * self.elem_size[0],
                        self.pos[1] + y * self.elem_size[1],
                        self.elem_base_size[0],
                        self.elem_base_size[1],
                    ),
                )

                action_text = self.font.render(
                    self.actions[y][x]["name"],
                    self.text_colour,
                    size=self.font_size,
                )
                action_text_rect = action_text[0].get_rect(
                    center=action_rect.center
                )
                window.blit(action_text[0], action_text_rect)

    def skip_turn(self):
        return self.players.cycle_curr()
