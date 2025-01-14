import sys
import pygame

from core.main import MainRun

if __name__ == "__main__":
    main = MainRun()
    main.run_game_loop()
    pygame.quit()
    sys.exit()
