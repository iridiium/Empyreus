import pygame


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
