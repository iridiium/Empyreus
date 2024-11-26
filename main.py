import pygame
from random import randint


# Helper functions
def cycle(arr, start=0):
    while True:
        yield arr[start]
        start = (start + 1) % len(arr)


# Image classes
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__()

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

    def get_sprite_by_pos(self, sprite_pos):
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

        return self.get_sprite_by_pos(sprite_pos)

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


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, number, start_pos):
        super().__init__()

        self.tile_total_size = TILE_SIZE
        self.board_pos = BOARD_POS

        self.number = number
        self.image = pygame.image.load(f"tiny-spaceships/tiny_ship{number}.png")

        self.move(start_pos)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def move(self, new_pos):
        self.rect = self.image.get_rect()
        self.rect.left = (
            self.board_pos[0]
            + new_pos[0] * self.tile_total_size
            + (self.tile_total_size - self.image.get_width()) / 2
        )
        self.rect.top = (
            self.board_pos[1]
            + new_pos[1] * self.tile_total_size
            + (self.tile_total_size - self.image.get_height()) / 2
        )


# Board classes
class Tile:

    def __init__(self, pos, colour, image, type, base_size, border_size, size):
        self.pos = pos
        self.colour = colour
        self.image = image
        self.type = type
        self.base_size = base_size
        self.border_size = border_size
        self.size = size

        self.centre_pos = (
            self.pos[0] + self.size / 2,
            self.pos[1] + self.size / 2,
        )

        self.rect = self.image.get_rect()

    def get_colour(self):
        return self.colour

    def get_type(self):
        return self.type

    def get_rect_in_board(self):
        return (
            self.pos[0] + self.border_size / 2,
            self.pos[1] + self.border_size / 2,
            self.size,
            self.size,
        )


class Board:

    def __init__(
        self,
        size,
        pos,
        tile_colour,
        tile_base_size,
        tile_border_size,
        tile_size,
        spritesheet,
        tiles,
    ):
        self.size = size
        self.pos = pos
        self.tile_colour = tile_colour
        self.tile_base_size = tile_base_size
        self.tile_border_size = tile_border_size
        self.tile_size = tile_size
        self.spritesheet = spritesheet
        self.tile_order, self.tile_types = self.order_tiles(tiles)

        self.rows = [
            [
                Tile(
                    pos=(
                        i * tile_size + self.pos[0],
                        j * tile_size + self.pos[1],
                    ),
                    colour=tile_colour,
                    image=next(self.tile_order),
                    type=next(self.tile_types),
                    base_size=tile_base_size,
                    border_size=tile_border_size,
                    size=tile_size,
                )
                for i in range(self.size[0])
            ]
            for j in range(self.size[1])
        ]

    def get_type_at_pos_on_board(self, pos_on_board):
        return self.rows[pos_on_board[1]][pos_on_board[0]].get_type()

    def order_tiles(self, tiles):
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

    def create_graph(self, window, board):
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
                    board[i][j].centre_pos,
                    board[last_i][last_j].centre_pos,
                )

            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if (
                        m >= 0
                        and n >= 0
                        and m < len(visited)
                        and n < len(visited[0])
                        and visited[m][n] is False
                    ):
                        dfs(m, n, i, j)

        islands = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if visited[i][j] is False:
                    islands.append([])

                    dfs(i, j, None, None)

        self.graph = graph

        return graph

    def draw(self, window, pos):
        for j, row in enumerate(self.rows):
            for i, tile in enumerate(row):
                if i == pos[0] and j == pos[1]:
                    colour = tile.get_colour()
                    rect_object = tile.get_rect_in_board()

                    pygame.draw.rect(
                        window,
                        colour,
                        rect_object,
                    )

                image_rect = tile.get_rect_in_board()
                window.blit(tile.image, image_rect)


# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WINDOW_SIZE = (800, 600)

BOARD_SIZE = (5, 5)

TILE_BASE_SIZE = 72
TILE_BORDER_SIZE = 8

TILE_SIZE = TILE_BASE_SIZE + TILE_BORDER_SIZE

BOARD_POS = (
    (WINDOW_SIZE[0] - BOARD_SIZE[0] * TILE_SIZE - TILE_BORDER_SIZE) / 2,
    (WINDOW_SIZE[1] - BOARD_SIZE[1] * TILE_SIZE - TILE_BORDER_SIZE) / 2,
)


# Game loop
def coord_to_board_pos(pos):
    return (
        int(
            min(max((pos[0] - BOARD_POS[0]) // TILE_SIZE, 0), BOARD_SIZE[0] - 1)
        ),
        int(
            min(max((pos[1] - BOARD_POS[1]) // TILE_SIZE, 0), BOARD_SIZE[1] - 1)
        ),
    )


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
    players = [Player(5, (0, 1)), Player(7, (0, 0))]

    main_board = Board(
        size=BOARD_SIZE,
        pos=BOARD_POS,
        tile_colour=GREY,
        tile_base_size=TILE_BASE_SIZE,
        tile_border_size=TILE_BORDER_SIZE,
        tile_size=TILE_SIZE,
        spritesheet=planets,
        tiles={
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

        window.fill(WHITE)
        window.blit(bg.image, bg.rect)

        main_board.create_graph(window, main_board.rows)

        mouse_pos = pygame.mouse.get_pos()
        pos_on_board = coord_to_board_pos(mouse_pos)

        turn = cycle(players)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(main_board.get_type_at_pos_on_board(pos_on_board))
                current_player = next(turn)
                print(current_player)
                current_player.move(pos_on_board)
                print(pos_on_board)

        main_board.draw(window, pos_on_board)

        for player in players:
            player.draw(window)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
