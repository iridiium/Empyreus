import pygame
from random import randint


# Helper functions
def shuffle(arr, n=None):
    """
    Implementation of the Fisher-Yates algorithm.
    """
    if n == None:
        n = len(arr)

    for i in range(n - 1, 0, -1):
        j = randint(0, i + 1)

        arr[i], arr[j] = arr[j], arr[i]

    return arr


# Image classes
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def change_image(self, new_image_file):
        self.image = pygame.image.load(new_image_file)


class Spritesheet:
    def __init__(self, image_file, sprite_size, names):
        self.image = pygame.image.load(image_file)
        self.sprite_size = sprite_size

        self.num_row_sprites = self.image.get_width() / self.sprite_size[0]
        self.num_col_sprites = self.image.get_height() / self.sprite_size[1]

        self.names = names

    def get_sprite_by_position(self, sprite_pos):
        return self.image.subsurface(
            pygame.Rect(
                sprite_pos[0] * self.sprite_size[0],
                sprite_pos[1] * self.sprite_size[1],
                self.sprite_size[0],
                self.sprite_size[1],
            )
        )

    def get_sprite_by_name(self, sprite_name):
        sprite_pos = self.names[sprite_name]

        return self.get_sprite_by_position(sprite_pos)

    def get_sprite_rect(self, pos):
        return pygame.Rect(
            pos[0],
            pos[1],
            self.sprite_size[0],
            self.sprite_size[1],
        )

    def get_random_sprite(self):
        return self.image.subsurface(
            self.get_sprite_rect(
                (
                    randint(0, int(self.num_row_sprites) - 1)
                    * self.sprite_size[0],
                    randint(0, int(self.num_col_sprites) - 1)
                    * self.sprite_size[1],
                )
            )
        )


# Board classes
class Tile:

    def __init__(self, x_pos, y_pos, colour, image, size, border_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = colour
        self.image = image
        self.size = size
        self.border_size = border_size

    def get_colour(self):
        return self.colour

    def get_image(self):
        return self.image

    def get_rect_object(self, x, y):
        return (
            x * (self.size + self.border_size) + self.x_pos,
            y * (self.size + self.border_size) + self.y_pos,
            self.size,
            self.size,
        )

    def get_picture_rect_object(self, x, y):
        return (
            x * (self.size + self.border_size)
            + self.x_pos
            + self.border_size / 2,
            y * (self.size + self.border_size)
            + self.y_pos
            + self.border_size / 2,
            self.size,
            self.size,
        )


class Board:

    def __init__(
        self,
        num_in_row,
        num_in_column,
        x_pos,
        y_pos,
        tile_colour,
        tile_size,
        tile_border_size,
        spritesheet,
        tiles,
    ):
        self.num_in_row = num_in_row
        self.num_in_column = num_in_column
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile_colour = tile_colour
        self.tile_size = tile_size
        self.tile_border_size = tile_border_size
        self.spritesheet = spritesheet
        self.tiles = self.distribute_tiles(tiles)

        self.rows = [
            [
                Tile(
                    x_pos,
                    y_pos,
                    tile_colour,
                    next(self.tiles),
                    tile_size,
                    tile_border_size,
                )
                for _ in range(self.num_in_row)
            ]
            for _ in range(self.num_in_column)
        ]

    def distribute_tiles(self, tiles):
        distributed_tiles = []
        for tile_type, tile_count in tiles.items():
            for _ in range(tile_count):
                distributed_tiles.insert(
                    randint(0, len(distributed_tiles)),
                    self.spritesheet.get_sprite_by_name(tile_type),
                )

        return iter(distributed_tiles)

    def draw_self(self, window):
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                colour = cell.get_colour()

                # rect_object = cell.get_rect_object(x, y)
                # pygame.draw.rect(
                #     window,
                #     colour,
                #     rect_object,
                # )

                picture_rect_object = cell.get_picture_rect_object(x, y)
                window.blit(cell.get_image(), picture_rect_object)


# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WINDOW_SIZE = (800, 600)

BOARD_SIZE = (5, 5)

TILE_SIZE = 72
TILE_BORDER_SIZE = 8
TILE_TOTAL_SIZE = TILE_SIZE + TILE_BORDER_SIZE

BOARD_POS = (
    (WINDOW_SIZE[0] - BOARD_SIZE[0] * TILE_TOTAL_SIZE - TILE_BORDER_SIZE) / 2,
    (WINDOW_SIZE[1] - BOARD_SIZE[1] * TILE_TOTAL_SIZE - TILE_BORDER_SIZE) / 2,
)


# Game loop
def main():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    bg = Background("back_900x675.png", (0, 0))
    planets = Spritesheet(
        "CelestialObjects/CelestialObjects_Planets.png",
        (64, 64),
        {
            "water": (0, 0),
            "helium": (0, 1),
            "ore": (1, 0),
            "carbon": (1, 1),
            "antimatter": (2, 0),
            "empty": (2, 1),
        },
    )

    """
    num_in_row, num_in_column, x_pos, y_pos
    tile_colour, tile_size, tile_border_size
    """
    board = Board(
        BOARD_SIZE[0],
        BOARD_SIZE[1],
        BOARD_POS[0],
        BOARD_POS[1],
        GREY,
        TILE_SIZE,
        TILE_BORDER_SIZE,
        planets,
        {
            "water": 3,
            "helium": 3,
            "ore": 3,
            "carbon": 3,
            "antimatter": 3,
            "empty": 10,
        },
    )

    running = True
    while running:
        clock.tick(100)

        pos = pygame.mouse.get_pos()
        x, y = pos[0], pos[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(WHITE)
        window.blit(bg.image, bg.rect)

        board.draw_self(window)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
