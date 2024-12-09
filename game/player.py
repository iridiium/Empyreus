import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, name, number, image_number, board):
        super().__init__()

        self.name = name
        self.number = number
        self.image = pygame.image.load(self.get_ship_image(image_number))
        self.board = board

        self.pos = board.get_random_planet_pos()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.get_rect_left_top(self.pos)

        self.next = None

    def get_number(self):
        return self.number

    def get_pos(self):
        return self.pos

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

    def get_ship_image(self, image_number):
        return f"./resources/images/tiny-spaceships/tiny_ship{image_number}.png"

    def draw(self, window):
        window.blit(self.image, self.rect)

    def move(self, new_pos, last_pos):
        if new_pos in self.board.get_connected_nodes(last_pos):
            self.pos = new_pos
            self.rect.left, self.rect.top = self.get_rect_left_top(new_pos)
            return True
        return False


class PlayerList:
    def __init__(self, board):
        self.board = board

        self.current_turn_taker = None
        self.first_player = None
        self.player_number = 0

    def get_current_turn_taker(self):
        return self.current_turn_taker

    def shift_current_turn_taker(self, num_shifts=1):
        for _ in range(num_shifts):
            self.current_turn_taker = self.current_turn_taker.next
        return self.current_turn_taker

    def add(self, name, image_number):
        new_player = Player(name, self.player_number, image_number, self.board)
        self.player_number += 1

        if self.first_player is None:
            new_player.next = new_player
            self.first_player = new_player
        else:
            current_player = self.first_player

            while current_player.next != self.first_player:
                current_player = current_player.next

            current_player.next = new_player

            new_player.next = self.first_player

        if self.current_turn_taker is None:
            self.current_turn_taker = self.first_player

    def get_list(self):
        if self.first_player is None:
            return []

        result = []

        current_player = self.first_player

        while True:
            result.append(current_player)
            current_player = current_player.next

            if current_player == self.first_player:
                break

        return result
