import pygame


class Tile:

    def __init__(
        self,
        centre_pos: tuple[int, int],
        colour: tuple[int, int, int],
        tile: dict,
        base_size: tuple[int, int],
        border_size: tuple[int, int],
    ):
        self.centre_pos = centre_pos
        self.colour = colour
        self.tile = tile
        self.base_size = base_size
        self.border_size = border_size

        self.image = tile["sprite"]
        self.type = tile["type"]
        self.icon_image = tile["icon_sprite"]

        self.size = self.base_size + self.border_size

        self.rect = self.image.get_rect()

        self.can_trade = False

    def get_can_trade(self) -> bool:
        return self.can_trade

    def get_centre_pos(self) -> tuple[int, int]:
        return self.centre_pos

    def get_colour(self) -> tuple[int, int, int]:
        return self.colour

    def get_icon_image(self) -> pygame.Surface:
        return self.icon_image

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_type(self) -> str:
        return self.type

    def get_rect_in_board(self) -> pygame.Rect:
        rect_in_board = self.image.get_rect()
        rect_in_board.center = self.centre_pos

        return rect_in_board


class TraderTile(Tile):
    def __init__(
        self,
        centre_pos: tuple[int, int],
        colour: tuple[int, int, int],
        tile: dict,
        base_size: tuple[int, int],
        border_size: tuple[int, int],
    ):
        super().__init__(
            centre_pos,
            colour,
            tile,
            base_size,
            border_size,
        )

        self.can_trade: bool = True
        self.trade: tuple[str, int] = {
            "type_taken": tile["trade_type"],
            "amount_taken": 5,
            "amount_given": 4,
        }  # there is no "type_given" as all traders return random resources.

    def get_trade(self) -> tuple[str, int]:
        return self.trade
