from __future__ import annotations

# avoiding circular imports in type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player
    from .sprite_sheet import SpriteSheet

import pygame

from collections import defaultdict
from random import choice, randint, sample
from typing import Iterator, TypedDict

from .helper import (
    find_dist,
    get_adjs,
    get_conns,
    get_min_conns_dist,
    merge_sort,
)
from .tile import Tile, TraderTile


class Board:

    def __init__(
        self,
        dims: tuple[int, int],
        line_colour: tuple[int, int, int],
        tile_colour: tuple[int, int, int],
        tile_base_size: tuple[int, int],
        tile_border_size: tuple[int, int],
        window_size: tuple[int, int],
        sprite_sheet: SpriteSheet,
        icon_sprite_sheet: SpriteSheet,
        tiles: dict[str, int],
    ):
        self.dims = dims
        self.line_colour = line_colour
        self.tile_colour = tile_colour
        self.tile_base_size = tile_base_size
        self.tile_border_size = tile_border_size
        self.window_size = window_size
        self.sprite_sheet = sprite_sheet
        self.icon_sprite_sheet = icon_sprite_sheet

        self.num_planets = sum(
            list(filter(lambda amount: amount > 0, tiles.values()))
        )
        self.num_traders = sum(
            amount
            for type, amount in tiles.items()
            if type.startswith("trader")
        )

        self.tile_order = self.order_tiles(tiles)
        self.tile_size: tuple[int, int] = (
            tile_base_size[0] + tile_border_size[0],
            tile_base_size[1] + tile_border_size[1],
        )

        self.pos = (
            int(
                (
                    self.window_size[0]
                    - self.dims[0] * self.tile_size[0]
                    - self.tile_border_size[0]
                )
                / 2
            ),
            int(
                (
                    self.window_size[1]
                    - self.dims[1] * self.tile_size[1]
                    - self.tile_border_size[1]
                )
                / 2
            ),
        )
        self.pos_end = (
            self.pos[0] + self.tile_size[0] * self.dims[0],
            self.pos[1] + self.tile_size[1] * self.dims[1],
        )

        self.matrix = [
            [
                (
                    TraderTile(
                        centre_pos=(
                            int((i + 0.5) * self.tile_size[0] + self.pos[0]),
                            int((j + 0.5) * self.tile_size[1] + self.pos[1]),
                        ),
                        colour=tile_colour,
                        tile=curr_tile,
                        base_size=tile_base_size,
                        border_size=tile_border_size,
                    )
                    if self.get_tile_behaviour_type_from_tile_type(
                        (curr_tile := next(self.tile_order))["type"]
                    )
                    == "trader"
                    else Tile(
                        centre_pos=(
                            int((i + 0.5) * self.tile_size[0] + self.pos[0]),
                            int((j + 0.5) * self.tile_size[1] + self.pos[1]),
                        ),
                        colour=tile_colour,
                        tile=curr_tile,
                        base_size=tile_base_size,
                        border_size=tile_border_size,
                    )
                )
                for i in range(self.dims[0])
            ]
            for j in range(self.dims[1])
        ]

        self.graph = self.create_graph(self.matrix)

    def get_icon_sprite_sheet(self) -> SpriteSheet:
        return self.icon_sprite_sheet

    def get_pos(self) -> tuple[int, int]:
        return self.pos

    def get_pos_end(self) -> tuple[int, int]:
        return self.pos_end

    def get_matrix(self) -> list[list[Tile | TraderTile]]:
        return self.matrix

    def get_graph(self) -> dict[tuple[int, int], set[tuple[int, int]]]:
        return self.graph

    def get_tile_border_size(self) -> tuple[int, int]:
        return self.tile_border_size

    def get_tile_size(self) -> tuple[int, int]:
        return self.tile_size

    def get_window_size(self) -> tuple[int, int]:
        return self.window_size

    def get_size(self) -> tuple[int, int]:
        return (self.pos_end[0] - self.pos[0], self.pos_end[1] - self.pos[1])

    def get_icon_sprite_from_type(self, type) -> None | pygame.Surface:
        resource_type = self.get_resource_type_from_tile_type(type)

        if resource_type:
            return self.icon_sprite_sheet.get_sprite_from_name(resource_type)

        return None

    def get_resource_type_from_tile_type(self, type) -> None | str:
        resource_names = self.icon_sprite_sheet.get_names()
        resource_type = type.split("_")[-1]

        if resource_type in resource_names:  # For planets
            return resource_type
        elif (
            resource_type in "QWERTYUIOPASDFGHJKLZXCVBNM"
        ):  # For trading stations
            return choice(list(resource_names.keys()))

        return None

    def get_tile_behaviour_type_from_tile_type(self, type) -> str:
        return type.split("_")[0]

    def get_tile_centre_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        return self.matrix[pos[1]][pos[0]].get_centre_pos()

    def board_pos_from_coord(
        self, coord: tuple[int, int]
    ) -> tuple[int | None, int | None]:
        board_pos_x = (coord[0] - self.pos[0]) // self.tile_size[0]
        board_pos_y = (coord[1] - self.pos[1]) // self.tile_size[1]

        return (
            board_pos_x if 0 <= board_pos_x <= self.dims[0] - 1 else None,
            board_pos_y if 0 <= board_pos_y <= self.dims[1] - 1 else None,
        )

    def create_graph(
        self, matrix: list[list[Tile]]
    ) -> defaultdict[tuple[int, int], set[tuple[int, int]]]:
        # Creates a tree which may be disconnected.
        graph: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
            set
        )
        visited = [
            [tile.get_type() == "empty" for tile in row] for row in matrix
        ]

        def dfs(
            i: int,
            j: int,
            last_i: int,
            last_j: int,
            island: list[tuple[int, int]],
        ):
            last_node = (last_j, last_i)
            node = (j, i)

            visited[i][j] = True
            if last_node != (-1, -1):
                graph[last_node].add(node)
                graph[node].add(last_node)

            island.append(node)

            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if (
                        0 <= m < self.dims[1]
                        and 0 <= n < self.dims[0]
                        and not visited[m][n]
                    ):
                        dfs(m, n, i, j, island)

        islands: list[list[tuple[int, int]]] = []
        for i in range(self.dims[1]):
            for j in range(self.dims[0]):
                if not visited[i][j]:
                    island: list[tuple[int, int]] = []
                    dfs(i, j, -1, -1, island)
                    islands.append(island)

        # Creates a connected tree.
        # Links the mainland to all the isles.
        # - mainland: the largest connected group of planets.
        # - isles: any smaller connected groups not adjacent to the mainland.
        if len(islands) > 1:
            islands = merge_sort(islands, lambda a, b: len(a) > len(b))

            mainland, *isles = islands

            for isle in isles:
                for planet in isle:
                    min_dist_planet = min(
                        mainland,
                        key=lambda other_planet: find_dist(
                            planet, other_planet
                        ),
                    )

                    graph[planet].add(min_dist_planet)
                    graph[min_dist_planet].add(planet)

        # Creates a graph (with potential for multiple edges per node).
        # Ensures that all neighbours are closer than 3 moves away.
        # This is purely for a less frustrating game.
        for node in graph:
            for adj in get_adjs(self.matrix, node):
                if get_min_conns_dist(graph, node, adj) > 3:
                    graph[adj].add(node)
                    graph[node].add(adj)

        return graph

    def get_rand_non_empty_pos(self) -> tuple[int, int]:
        return choice(list(self.graph))

    def get_type_from_board_pos(self, board_pos: tuple[int, int]) -> str:
        return self.matrix[board_pos[1]][board_pos[0]].get_type()

    def order_tiles(self, tiles: dict[str, int]) -> Iterator[dict]:
        tile_order: list[dict] = []

        trader_types: Iterator[str] = iter(
            sample(
                sorted(self.icon_sprite_sheet.get_names().keys()),
                self.num_traders,
            )
        )

        total = 0

        for tile_type, tile_amount in tiles.items():
            if tile_amount == float("inf"):
                tile_amount = self.dims[0] * self.dims[1] - total
            else:
                total += tile_amount

            for _ in range(tile_amount):
                tile_attrs = {
                    "sprite": self.sprite_sheet.get_sprite_from_name(tile_type),
                    "type": tile_type,
                    "icon_sprite": self.get_icon_sprite_from_type(tile_type),
                }

                if tile_type.startswith("trader"):
                    tile_attrs["trade_type"] = next(trader_types)

                tile_order.insert(
                    randint(0, len(tile_order)),
                    tile_attrs,
                )

        return iter(tile_order)

    def render_to(
        self,
        window: pygame.display,
        mouse_board_coord: tuple[int, int],
        player: Player,
    ) -> None:
        drawn = set()

        for node, conns in self.graph.items():
            for conn in conns:
                edge = frozenset([node, conn])
                if edge not in drawn:
                    pygame.draw.line(
                        window,
                        self.line_colour,
                        self.matrix[node[1]][node[0]].get_centre_pos(),
                        self.matrix[conn[1]][conn[0]].get_centre_pos(),
                    )

                    drawn.add(edge)

        for j, row in enumerate(self.matrix):
            for i, tile in enumerate(row):
                tile_rect = tile.get_rect_in_board()

                if (i, j) == mouse_board_coord:
                    mouse_board_highlight_rect = tile_rect.scale_by(1)
                    pygame.draw.rect(
                        window, tile.get_colour(), mouse_board_highlight_rect
                    )

                if (i, j) == player.get_pos():
                    player_highlight_rect = tile_rect.scale_by(1)
                    pygame.draw.rect(
                        window, player.get_colour(), player_highlight_rect
                    )

                window.blit(tile.get_image(), tile_rect)

                if tile_icon_image := tile.get_icon_image():
                    window.blit(tile_icon_image, tile_rect)
