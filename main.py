import pygame
import pygame.freetype

from random import randrange

from game.background import Background
from game.board import Board
from game.player import Player
from game.spritesheet import Spritesheet

# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WINDOW_SIZE = (800, 600)

BOARD_SIZE = (6, 6)

TILE_BASE_SIZE = 72
TILE_BORDER_SIZE = 8
TILE_SIZE = TILE_BASE_SIZE + TILE_BORDER_SIZE
FONT_SIZE = TILE_SIZE / 4

BOARD_POS = (
    (WINDOW_SIZE[0] - BOARD_SIZE[0] * TILE_SIZE - TILE_BORDER_SIZE) / 2,
    (WINDOW_SIZE[1] - BOARD_SIZE[1] * TILE_SIZE - TILE_BORDER_SIZE) / 2,
)

NUM_PLAYERS = 2

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
        "water": 4,
        "helium": 4,
        "ore": 4,
        "carbon": 4,
        "antimatter": 4,
        "empty": -1,
    },
)

bg = Background("./resources/images/back_900x675.png", (0, 0))


# Game loop
def main():
    pygame.init()

    FONT = pygame.freetype.Font(
        "resources/fonts/Roboto/Roboto-Regular.ttf", FONT_SIZE
    )

    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    players = [
        Player(2, board.get_random_planet_pos(), board),
        Player(3, board.get_random_planet_pos(), board),
    ]

    total_turns = 0
    current_turn = 0

    running = True
    while running:
        clock.tick(100)

        window.fill(WHITE)
        window.blit(bg.image, bg.rect)

        mouse_pos = pygame.mouse.get_pos()
        pos_on_board = board.coord_to_board_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                valid_move = players[current_turn].move(
                    pos_on_board, players[current_turn].get_pos()
                )
                if valid_move:
                    current_turn = (current_turn + 1) % len(players)
                    total_turns += 1
                    finished_turn = True

        board.draw(window, pos_on_board)

        for player in players:
            player.draw(window)

        FONT.render_to(window, (10, 10), f"Turns elapsed: {total_turns}", WHITE)
        FONT.render_to(
            window,
            (10, 10 + TILE_BORDER_SIZE + FONT_SIZE),
            f"Player {current_turn + 1}'s turn.",
            WHITE,
        )

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
