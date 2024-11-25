import pygame
import heapq
from random import randint


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

    def __init__(self, x_pos, y_pos, colour, image, type, size, border_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = colour
        self.image = image
        self.type = type
        self.size = size
        self.border_size = border_size

        self.centre_x_pos = self.x_pos + self.size / 2
        self.centre_y_pos = self.y_pos + self.size / 2

    def get_rect_object(self):
        return (
            self.x_pos,
            self.y_pos,
            self.size,
            self.size,
        )

    def get_image_rect_object(self):
        return (
            self.x_pos + self.border_size / 2,
            self.y_pos + self.border_size / 2,
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
        self.tile_arrangement, self.tile_types = self.arrange_tiles(tiles)

        self.rows = [
            [
                Tile(
                    i * (self.tile_size + self.tile_border_size) + self.x_pos,
                    j * (self.tile_size + self.tile_border_size) + self.y_pos,
                    tile_colour,
                    next(self.tile_arrangement),
                    next(self.tile_types),
                    tile_size,
                    tile_border_size,
                )
                for i in range(self.num_in_row)
            ]
            for j in range(self.num_in_column)
        ]

    def arrange_tiles(self, tiles):
        result = []
        tile_types = []

        for tile_type, tile_amount in tiles.items():
            for _ in range(tile_amount):
                target = randint(0, len(result))
                result.insert(
                    target,
                    self.spritesheet.get_sprite_by_name(tile_type),
                )
                tile_types.insert(
                    target,
                    tile_type,
                )

        return iter(result), iter(tile_types)

    def draw_lines(self, window, board):
        graph = {}
        visited = [[tile.type == "empty" for tile in row] for row in board]

        def dfs(i, j, last_i, last_j):
            visited[i][j] = True

            if last_i is not None and last_j is not None:
                if (last_i, last_j) in graph:
                    graph[(last_i, last_j)].append((i, j))
                else:
                    graph[(last_i, last_j)] = [(i, j)]

                if (i, j) in graph:
                    graph[(i, j)].append((last_i, last_j))
                else:
                    graph[(i, j)] = [(last_i, last_j)]

                pygame.draw.line(
                    window,
                    WHITE,
                    (
                        board[i][j].centre_x_pos,
                        board[i][j].centre_y_pos,
                    ),
                    (
                        board[last_i][last_j].centre_x_pos,
                        board[last_i][last_j].centre_y_pos,
                    ),
                )

            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    if (
                        k >= 0
                        and l >= 0
                        and k < len(visited)
                        and l < len(visited[0])
                        and visited[k][l] == False
                    ):
                        dfs(k, l, i, j)

        num_islands = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if visited[i][j] == False:
                    num_islands += 1
                    dfs(i, j, None, None)

        return graph, num_islands

    def draw_self(self, window):
        for j, row in enumerate(self.rows):
            for i, tile in enumerate(row):
                colour = tile.colour
                image_rect_object = tile.get_image_rect_object()
                window.blit(tile.image, image_rect_object)


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
    main_board = Board(
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
        i, j = pos[0], pos[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(WHITE)
        window.blit(bg.image, bg.rect)

        main_board.draw_lines(window, main_board.rows)
        main_board.draw_self(window)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
