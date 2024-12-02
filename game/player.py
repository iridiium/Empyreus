import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, number, pos, board):
        super().__init__()

        self.number = number
        self.pos = pos
        self.board = board

        self.image = pygame.image.load(
            f"./resources/images/tiny-spaceships/tiny_ship{number}.png"
        )

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.get_rect_left_top(pos)

    def get_pos(self):
        return self.pos

    def draw(self, window):
        window.blit(self.image, self.rect)

    def get_rect_left_top(self, pos):
        return (
            (
                self.board.get_pos()[0]
                + pos[0] * self.board.get_tile_size()
                + (self.board.get_tile_size() - self.image.get_width()) / 2
            ),
            (
                self.board.get_pos()[1]
                + pos[1] * self.board.get_tile_size()
                + (self.board.get_tile_size() - self.image.get_height()) / 2
            ),
        )

    def move(self, new_pos, last_pos):
        if new_pos in self.board.get_nodes_connected_to(last_pos):
            self.pos = new_pos
            self.rect.left, self.rect.top = self.get_rect_left_top(new_pos)
            return True
        return False
