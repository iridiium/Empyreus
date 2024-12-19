import pygame


class Background(pygame.sprite.Sprite):

    def __init__(self, image_file_path: str, pos: tuple[int, int]):
        super().__init__()

        self.image = pygame.image.load(image_file_path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos

    def change_image(self, new_image_file_path: str) -> None:
        self.image = pygame.image.load(new_image_file_path)
