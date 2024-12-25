import pygame
import pygame.freetype

from random import randrange

from game.background import Background
from game.board import Board
from game.player import Player, PlayerList
from game.sprite_sheet import SpriteSheet

from ui.text import UIText

# Constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WINDOW_SIZE = (1024, 640)

BOARD_DIMS = (6, 6)

TILE_BASE_SIZE = (72, 72)
TILE_BORDER_SIZE = (8, 8)
TILE_SIZE = (80, 80)
FONT_SIZE = 20

NUM_PLAYERS = 2

PLANETS_ASTEROIDS = SpriteSheet(
    image_file_path="./resources/images/CelestialObjects_PlanetsAsteroids.png",
    sprite_size=(64, 64),
    names={
        "planet_ice": (0, 0),
        "empty": (0, 1),
        "planet_ore": (1, 0),
        "planet_uranium": (1, 1),
        "planet_carbon": (2, 0),
        "planet_helium": (2, 1),
        "asteroid": (3, 0),
        "asteroid_small": (3, 1),
    },
)

RESOURCES = SpriteSheet(
    image_file_path="./resources/images/MiningIcons.png",
    sprite_size=(32, 32),
    names={
        "carbon": (1, 1),
        "helium": (8, 2),
        "ice": (4, 2),
        "ore": (5, 1),
        "uranium": (7, 3),
    },
)

BOARD = Board(
    dims=BOARD_DIMS,
    line_colour=WHITE,
    tile_colour=GREY,
    tile_base_size=TILE_BASE_SIZE,
    tile_border_size=TILE_BORDER_SIZE,
    window_size=WINDOW_SIZE,
    sprite_sheet=PLANETS_ASTEROIDS,
    icon_sprite_sheet=RESOURCES,
    tiles={
        "planet_carbon": 3,
        "planet_helium": 3,
        "planet_ice": 3,
        "planet_ore": 3,
        "planet_uranium": 3,
        "asteroid": 2,
        "asteroid_small": 2,
        "empty": float("inf"),
    },
)

BACKGROUND = Background(
    image_file_path="./resources/images/back_1024x640.png", pos=(0, 0)
)


# Game loop
def main():
    pygame.init()

    FONT = pygame.freetype.Font(
        "resources/fonts/Roboto/Roboto-Regular.ttf", FONT_SIZE
    )

    FONT_BOLD = pygame.freetype.Font(
        "resources/fonts/Roboto/Roboto-Bold.ttf", FONT_SIZE
    )

    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    board_pos = BOARD.get_pos()

    players = PlayerList(BOARD)
    players.add("Anthony", 1)
    players.add("Bert", 2)
    players.add("Cuthbert", 3)

    total_turns = 0

    running = True
    while running:
        clock.tick(100)

        window.fill(WHITE)
        window.blit(BACKGROUND.image, BACKGROUND.rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_on_board = BOARD.board_pos_from_coord(mouse_pos)

        curr_player = players.get_curr()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                valid_move = curr_player.move(
                    mouse_pos_on_board, curr_player.get_pos()
                )

                if valid_move:
                    players.cycle_curr()
                    total_turns += 1

        BOARD.render_to(window, mouse_pos_on_board)

        for player_num, player in enumerate(players.get_list()):
            player.render_to(window)

        UI_TEXT = UIText(
            BOARD,
            FONT,
            FONT_BOLD,
            FONT_SIZE,
            FONT_SIZE * 2,
            players,
            WHITE,
        )
        UI_TEXT.render_on(window, total_turns, curr_player)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
