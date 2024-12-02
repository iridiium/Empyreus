import pygame

from game.background import Background
from game.board import Board
from game.player import Player
from game.spritesheet import Spritesheet

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

PLANETS = Spritesheet(
    "./resources/images/CelestialObjects/CelestialObjects_Planets.png",
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

board = Board(
    size=BOARD_SIZE,
    pos=BOARD_POS,
    line_colour=WHITE,
    tile_colour=GREY,
    tile_base_size=TILE_BASE_SIZE,
    tile_border_size=TILE_BORDER_SIZE,
    spritesheet=PLANETS,
    tiles={
        "water": 3,
        "helium": 3,
        "ore": 3,
        "carbon": 3,
        "antimatter": 3,
        "empty": -1,
    },
)

bg = Background("./resources/images/back_900x675.png", (0, 0))


# Game loop
def main():
    def coord_to_board_pos(pos):
        return (
            int(
                min(
                    max((pos[0] - BOARD_POS[0]) // TILE_SIZE, 0),
                    BOARD_SIZE[0] - 1,
                )
            ),
            int(
                min(
                    max((pos[1] - BOARD_POS[1]) // TILE_SIZE, 0),
                    BOARD_SIZE[1] - 1,
                )
            ),
        )

    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    players = [Player(7, board.get_random_planet_pos(), board)]

    current = 0

    running = True
    while running:
        clock.tick(100)

        window.fill(WHITE)
        window.blit(bg.image, bg.rect)

        mouse_pos = pygame.mouse.get_pos()
        pos_on_board = coord_to_board_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                players[current].move(pos_on_board, players[current].get_pos())
                current = (current + 1) % len(players)

        board.draw(window, pos_on_board)

        for player in players:
            player.draw(window)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
