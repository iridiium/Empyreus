import pygame

from .game.background import Background
from .game.sprite_sheet import SpriteSheet


def load_assets():
    pygame.init()

    # ---- Background ----
    background = Background(
        image_file_path="./assets/images/back_1024x640.png", pos=(0, 0)
    )

    # ---- Sprite Sheets ----
    sprite_sheet_tiles = SpriteSheet(
        image_file_path="./assets/images/CelestialObjects_PlanetsAsteroids.png",
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

    sprite_sheet_resources = SpriteSheet(
        image_file_path="./assets/images/MiningIcons.png",
        sprite_size=(32, 32),
        names={
            "carbon": (1, 1),
            "helium": (8, 2),
            "ice": (4, 2),
            "ore": (5, 1),
            "uranium": (7, 3),
        },
    )

    # ---- Fonts ----
    font_size = 20
    font_bold_size = 40

    font = pygame.freetype.Font(
        "./assets/fonts/Roboto/Roboto-Regular.ttf", font_size
    )

    font_bold = pygame.freetype.Font(
        "./assets/fonts/Roboto/Roboto-Bold.ttf", font_size
    )

    return (
        background,
        sprite_sheet_tiles,
        sprite_sheet_resources,
        font_size,
        font_bold_size,
        font,
        font_bold,
    )
