import pygame

from game.board import Board


class UIActions:
    def __init__(
        self,
        board: Board,
        dims: tuple[int, int],
        elem_size: tuple[int, int],
        elem_border_size: tuple[int, int],
        colour: tuple[int, int, int],
    ):
        self.board = board
        self.dims = dims
        self.elem_size = elem_size
        self.elem_border_size = elem_border_size
        self.colour = colour

        self.board_pos = self.board.get_pos()
        self.board_pos_end = self.board.get_pos_end()
        self.start_pos = (self.board_pos[0], self.board_pos_end[1] + 20)

    def render_to(self, window: pygame.display):
        for y in range(self.dims[1]):
            for x in range(self.dims[0]):
                pygame.draw.rect(
                    window,
                    self.colour,
                    (
                        self.start_pos[0]
                        + x * (self.elem_size[0] + self.elem_border_size[0]),
                        self.start_pos[1]
                        + y * (self.elem_size[1] + self.elem_border_size[1]),
                        self.elem_size[0],
                        self.elem_size[1],
                    ),
                )
