import pygame, random


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
    def __init__(self, image_file, sprite_dimensions):
        self.image = pygame.image.load(image_file)
        self.sprite_dimensions = sprite_dimensions

    def get_sprite(self, sprite_position):
        return self.image.subsurface(
            pygame.Rect(
                sprite_position[0] * self.sprite_dimensions[0],
                sprite_position[1] * self.sprite_dimensions[1],
                self.sprite_dimensions[0],
                self.sprite_dimensions[1],
            )
        )

    def get_random_sprite(self):
        sprites_in_row = self.image.get_width() / self.sprite_dimensions[0]
        sprites_in_column = self.image.get_height() / self.sprite_dimensions[1]

        return self.image.subsurface(
            pygame.Rect(
                random.randint(0, int(sprites_in_row) - 1)
                * self.sprite_dimensions[0],
                random.randint(0, int(sprites_in_column) - 1)
                * self.sprite_dimensions[1],
                self.sprite_dimensions[0],
                self.sprite_dimensions[1],
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
    ):
        self.num_in_row = num_in_row
        self.num_in_column = num_in_column
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile_colour = tile_colour
        self.tile_size = tile_size
        self.tile_border_size = tile_border_size
        self.spritesheet = spritesheet

        self.rows = [
            [
                Tile(
                    x_pos,
                    y_pos,
                    tile_colour,
                    spritesheet.get_random_sprite(),
                    tile_size,
                    tile_border_size,
                )
                for _ in range(self.num_in_row)
            ]
            for _ in range(self.num_in_column)
        ]

    def draw_self(self, window):
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                colour = cell.get_colour()

                rect_object = cell.get_rect_object(x, y)
                picture_rect_object = cell.get_picture_rect_object(x, y)

                pygame.draw.rect(
                    window,
                    colour,
                    rect_object,
                )

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
    (WINDOW_SIZE[0] - BOARD_SIZE[0] * TILE_TOTAL_SIZE) / 2,
    (WINDOW_SIZE[1] - BOARD_SIZE[1] * TILE_TOTAL_SIZE) / 2,
)


# Game loop
def main():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    bg = Background("back_900x675.png", (0, 0))
    planets = Spritesheet(
        "CelestialObjects/CelestialObjects_Planets.png", (64, 64)
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
