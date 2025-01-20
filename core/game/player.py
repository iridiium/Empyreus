from __future__ import annotations

# avoiding circular imports in type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

import os
import pygame
import random

from .helper import get_conns
from .sprite_sheet import SpriteSheet


class Player:
    def __init__(
        self,
        name: str,
        num: int,
        colour: tuple[int, int, int],
        image_file_path: str,
        board: Board,
        resources: dict,
    ):
        self.name = name
        self.num = num
        self.colour = colour
        self.image = pygame.image.load(image_file_path)
        self.board = board
        self.resources = {
            resource_name: 0 for resource_name in resources.keys()
        }

        self.board_graph = board.get_graph()
        self.pos = board.get_rand_non_empty_pos()
        self.rect = self.image.get_rect()
        self.rect.center = self.board.get_tile_centre_pos(self.pos)

        self.actions_per_turn = 2
        self.actions_left = 2

        self.next = None

    def get_colour(self) -> tuple[int, int, int]:
        return self.colour

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_name(self) -> str:
        return self.name

    def get_num(self) -> int:
        return self.num

    def get_pos(self) -> tuple[int, int]:
        return self.pos

    def get_resources(self) -> dict:
        return self.resources

    def get_ship_image_file_location(self) -> str:
        return random.choice(os.listdir("./assets/images/tiny-spaceships"))

    def reset_actions_left(self) -> None:
        self.actions_left = self.actions_per_turn

    def move(self, new_pos: tuple[int, int], last_pos: tuple[int, int]) -> int:
        """
        Moves the player from one non-empty tile to another non-empty tile
        connected to it.

        Returns the number of moves left for the player that turn.
        """
        if new_pos in get_conns(self.board_graph, last_pos):
            self.actions_left -= 1
            self.pos = new_pos
            self.rect.center = self.board.get_tile_centre_pos(self.pos)

            if new_pos_resource_type := self.board.get_resource_type_from_tile_type(
                self.board.get_type_from_board_pos(new_pos)
            ):
                self.resources[new_pos_resource_type] += 1

            return self.actions_left

    def trade(self) -> bool:
        """
        Allows for a trade of one resource to another.
        This can only be done whilst on a trade station tile.

        Returns whether the trade was successful.
        """
        if not self.board.get_type_from_board_pos(self.pos).startswith(
            "trader"
        ):
            return False

        trade = self.board.get_matrix()[self.pos[1]][self.pos[0]].get_trade()

        if self.resources[trade[0]] >= trade[1]:
            self.resources[trade[0]] -= trade[1]

            self.resources[random.choice(list(self.resources.keys()))] += 1

    def render_to(self, window: pygame.display) -> None:
        window.blit(self.image, self.rect)


# Linked List
class PlayerList:
    def __init__(
        self, board: Board, resources: SpriteSheet, image_folder_path: str
    ):
        self.board = board
        self.resources = {
            resource_name: {
                "amount": 0,
                "icon_image": resources.get_sprite_from_name(resource_name),
            }
            for resource_name in resources.names
        }
        self.image_folder_path = image_folder_path

        self.curr = None  # The player who is currently taking their turn.
        self.first = None  # The first player of the turn order.

        self.len_cycle = 0  # The length of one cycle (as list is infinite).
        self.turns_taken = 0  # Number of turns taken.

    def get_curr(self) -> None | Player:
        return self.curr

    def get_turns_taken(self) -> int:
        return self.turns_taken

    def cycle_curr(self, num_turns: int = 1) -> Player:
        for _ in range(num_turns):
            self.turns_taken += 1

            if self.curr.next:
                self.curr = self.curr.next

            self.curr.reset_actions_left()
        return self.curr

    def add(self, name: str, colour: tuple[int, int, int]) -> None:
        new = Player(
            name,
            self.len_cycle,
            colour,
            f"{self.image_folder_path}/{random.choice(os.listdir(self.image_folder_path))}",
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

    def get_list(self) -> list:
        if self.first is None:
            return []

        result = [self.first]

        curr = self.first.next

        while curr != self.first:
            result.append(curr)
            curr = curr.next

        return result
