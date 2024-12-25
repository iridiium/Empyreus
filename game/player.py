import pygame

from .helper import get_conns


class Player(pygame.sprite.Sprite):

    def __init__(self, name, num, image_num, board):
        super().__init__()

        self.name = name
        self.num = num
        self.image = pygame.image.load(self.get_ship_image(image_num))
        self.board = board

        self.pos = board.get_rand_planet_pos()
        self.rect = self.image.get_rect()
        self.rect.center = self.board.get_tile_centre_pos(self.pos)

        self.next = None

    def get_image(self):
        return self.image

    def get_num(self):
        return self.num

    def get_pos(self):
        return self.pos

    def get_ship_image(self, image_num):
        return f"./resources/images/tiny-spaceships/tiny_ship{image_num}.png"

    def move(self, new_pos, last_pos):
        if new_pos in get_conns(self.board.get_graph(), last_pos):
            self.pos = new_pos
            self.rect.center = self.board.get_tile_centre_pos(self.pos)
            return True
        return False

    def render_to(self, window):
        window.blit(self.image, self.rect)


# Linked List
class PlayerList:
    def __init__(self, board):
        self.board = board

        self.curr = None  # The player who is currently taking their turn.
        self.first = None  # The first player of the turn order.

        self.len_cycle = 0  # The length of one cycle (as list is infinite).

    def get_curr(self):
        return self.curr

    def cycle_curr(self, num_turns=1):
        for _ in range(num_turns):
            self.curr = self.curr.next
        return self.curr

    def add(self, name, image_num):
        new = Player(name, self.len_cycle, image_num, self.board)
        self.len_cycle += 1

        if self.first is None:
            new.next = new
            self.first = new
        else:
            curr = self.first

            while curr.next != self.first:
                curr = curr.next

            curr.next = new

            new.next = self.first

        if self.curr is None:
            self.curr = self.first

    def get_list(self):
        if self.first is None:
            return []

        result = []

        curr = self.first

        while True:
            result.append(curr)
            curr = curr.next

            if curr == self.first:
                break

        return result
