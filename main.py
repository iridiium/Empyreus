# Paste pre-Pyrfected Python
import pygame

# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)


# Background
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# Tile
class Tile:

    def __init__(self, x_pos, y_pos, colour, size, border_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = colour
        self.size = size
        self.border_size = border_size

    def get_colour(self):
        return self.colour

    def get_rect_object(self, x, y):
        return (
            x * (self.size + self.border_size) + self.x_pos,
            y * (self.size + self.border_size) + self.y_pos,
            self.size,
            self.size,
        )


# Board
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
    ):
        self.num_in_row = num_in_row
        self.num_in_column = num_in_column
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tile_colour = tile_colour
        self.tile_size = tile_size
        self.tile_border_size = tile_border_size

        self.rows = [
            [
                Tile(x_pos, y_pos, tile_colour, tile_size, tile_border_size)
                for _ in range(self.num_in_row)
            ]
            for _ in range(self.num_in_column)
        ]

    def draw_self(self, window):
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                colour = cell.get_colour()
                rect_object = cell.get_rect_object(x, y)

                pygame.draw.rect(
                    window,
                    colour,
                    rect_object,
                )


# Game loop
WIDTH = 900
HEIGHT = 675

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

"""
num_in_row, num_in_column, x_pos, y_pos
tile_colour, tile_size, tile_border_size
"""
board = Board(8, 8, 142, 29.5, GREY, 70, 7)

bg = Background("back_900x675.png", (0, 0))

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
