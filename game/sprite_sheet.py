import pygame


class SpriteSheet:

    def __init__(
        self,
        image_file_path: str,
        names: dict[str, tuple[int, int]],
        sprite_size: tuple[int, int],
    ):
        self.image = pygame.image.load(image_file_path)
        self.names = names
        self.sprite_size = sprite_size

        self.dims = (
            (
                self.image.get_width() / self.sprite_size[0],
                self.image.get_height() / self.sprite_size[1],
            ),
        )

    def get_sprite_by_coord(
        self, sprite_coord: tuple[int, int]
    ) -> pygame.Surface:
        return self.image.subsurface(
            pygame.Rect(
                sprite_coord[0] * self.sprite_size[0],
                sprite_coord[1] * self.sprite_size[1],
                self.sprite_size[0],
                self.sprite_size[1],
            )
        )

    def get_sprite_by_name(self, sprite_name: str) -> pygame.Surface:
        sprite_pos = self.names[sprite_name]

        return self.get_sprite_by_coord(sprite_pos)
