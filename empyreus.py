import sys
import pygame

from core.main import Main

if __name__ == "__main__":
    main = Main()
    main.run_game_loop()
    pygame.quit()
    sys.exit()
