import pygame

from .helper import deepcopy_nested_dict, get_conns


class Player(pygame.sprite.Sprite):

    def __init__(self, name, num, colour, image_num, board, resources):
        super().__init__()

        self.name = name
        self.num = num
        self.colour = colour
        self.image = pygame.image.load(self.get_ship_image(image_num))
        self.board = board
        self.resources = deepcopy_nested_dict(resources)

        self.pos = board.get_rand_planet_pos()
        self.rect = self.image.get_rect()
        self.rect.center = self.board.get_tile_centre_pos(self.pos)

        self.board_graph = board.get_graph()

        self.next = None

    def get_colour(self):
        return self.colour

    def get_image(self):
        return self.image

    def get_name(self):
        return self.name

    def get_num(self):
        return self.num

    def get_pos(self):
        return self.pos

    def get_resources(self):
        return self.resources

    def get_ship_image(self, image_num):
        return f"./assets/images/tiny-spaceships/tiny_ship{image_num}.png"

    def move(self, new_pos, last_pos):
        if new_pos in get_conns(self.board_graph, last_pos):
            self.pos = new_pos
            self.rect.center = self.board.get_tile_centre_pos(self.pos)

            new_pos_planet_type = self.board.get_type_from_board_pos(new_pos)
            new_pos_resource_type = (
                self.board.get_resource_type_from_planet_type(
                    new_pos_planet_type
                )
            )

            if new_pos_resource_type:
                self.resources[new_pos_resource_type]["amount"] += 1
            return True
        return False

    def render_to(self, window):
        window.blit(self.image, self.rect)


# Linked List
class PlayerList:
    def __init__(self, board, resources):
        self.board = board

        self.resources = {
            resource_name: {
                "amount": 0,
                "icon_image": resources.get_sprite_from_name(resource_name),
            }
            for resource_name in resources.names
        }

        self.curr = None  # The player who is currently taking their turn.
        self.first = None  # The first player of the turn order.

        self.len_cycle = 0  # The length of one cycle (as list is infinite).

    def get_curr(self):
        return self.curr

    def cycle_curr(self, num_turns=1):
        for _ in range(num_turns):
            self.curr = self.curr.next
        return self.curr

    def add(self, name, image_num, colour):
        new = Player(
            name,
            self.len_cycle,
            colour,
            image_num,
            self.board,
            self.resources,
        )
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
