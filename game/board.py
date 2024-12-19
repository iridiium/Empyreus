import pygame

from collections import defaultdict
from random import randint, choice

from .helper import (
    find_dist,
    get_adjs,
    get_conns,
    get_min_conns_dist,
    merge_sort,
)
from .sprite_sheet import SpriteSheet


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
        tiles: dict[str, int],
    ):
        self.dims = dims
        self.line_colour = line_colour
        self.tile_colour = tile_colour
        self.tile_base_size = tile_base_size
        self.tile_border_size = tile_border_size
        self.window_size = window_size
        self.sprite_sheet = sprite_sheet
        self.tile_order, self.tile_types = self.order_tiles(tiles)

        self.num_planets = sum(
            list(filter(lambda num: num > 0, tiles.values()))
        )
        self.tile_size = tuple(
            sum(val) for val in zip(tile_base_size, tile_border_size)
        )
        self.pos = (
            (
                self.window_size[0]
                - self.dims[0] * self.tile_size[0]
                - self.tile_border_size[0]
            )
            / 2,
            (
                self.window_size[1]
                - self.dims[1] * self.tile_size[1]
                - self.tile_border_size[1]
            )
            / 2,
        )
        self.end_pos = (
            self.pos[0] + self.tile_size[0] * self.dims[0],
            self.pos[1] + self.tile_size[1] * self.dims[1],
        )

        self.matrix = [
            [
                Tile(
                    pos=(
                        i * self.tile_size[0] + self.pos[0],
                        j * self.tile_size[1] + self.pos[1],
                    ),
                    colour=tile_colour,
                    image=next(self.tile_order),
                    type=next(self.tile_types),
                    base_size=tile_base_size,
                    border_size=tile_border_size,
                )
                for i in range(self.dims[0])
            ]
            for j in range(self.dims[1])
        ]

        self.graph = self.create_graph(self.matrix)

    def get_end_pos(self):
        return self.end_pos

    def get_graph(self):
        return self.graph

    def get_pos(self):
        return self.pos

    def get_tile_size(self):
        return self.tile_size

    def coord_to_board_pos(self, coord):
        board_pos_x = (coord[0] - self.pos[0]) // self.tile_size[0]
        board_pos_y = (coord[1] - self.pos[1]) // self.tile_size[1]

        return (
            board_pos_x if 0 <= board_pos_x <= self.dims[0] - 1 else None,
            board_pos_y if 0 <= board_pos_y <= self.dims[1] - 1 else None,
        )

    def create_graph(self, matrix):
        graph = defaultdict(set)
        visited = [
            [tile.get_type() == "empty" for tile in row] for row in matrix
        ]

        def dfs(i, j, last_i, last_j, total_targets):
            last_node = (last_j, last_i)
            node = (j, i)

            visited[i][j] = True
            if last_node != (-1, -1):
                graph[last_node].add(node)
                graph[node].add(last_node)

            total_targets.append(node)

            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if (
                        0 <= m < self.dims[1]
                        and 0 <= n < self.dims[0]
                        and not visited[m][n]
                    ):
                        dfs(m, n, i, j, total_targets)

        islands = []
        for i in range(self.dims[1]):
            for j in range(self.dims[0]):
                if not visited[i][j]:
                    island = []
                    dfs(i, j, -1, -1, island)
                    islands.append(island)

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

        # Ensures that all neighbours are closer than 3 moves away.
        # This is purely for a less frustrating game.
        for node in graph:
            for adj in get_adjs(self.matrix, node):
                if get_min_conns_dist(graph, node, adj) > 3:
                    graph[adj].add(node)
                    graph[node].add(adj)

        return graph

    def draw(self, window, mouse_pos_on_board):
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
                if (i, j) == mouse_pos_on_board:
                    pygame.draw.rect(
                        window,
                        tile.get_colour(),
                        tile.get_rect_in_board(),
                    )

                image_rect = tile.get_rect_in_board()
                window.blit(tile.get_image(), image_rect)

    def get_rand_planet_pos(self):
        return choice(list(self.graph))

    def get_type_at_board_pos(self, board_pos):
        return self.matrix[board_pos[1]][board_pos[0]].get_type()

    def order_tiles(self, tiles):
        result = []
        tile_types = []
        total = 0

        for tile_type, tile_amount in tiles.items():
            if tile_amount == float("inf"):
                tile_amount = self.dims[0] * self.dims[1] - total
            else:
                total += tile_amount

            for _ in range(tile_amount):
                target = randint(0, len(result))
                result.insert(
                    target,
                    self.sprite_sheet.get_sprite_by_name(tile_type),
                )
                tile_types.insert(
                    target,
                    tile_type,
                )

        return iter(result), iter(tile_types)


class Tile:

    def __init__(self, pos, colour, image, type, base_size, border_size):
        self.pos = pos
        self.colour = colour
        self.image = image
        self.type = type
        self.base_size = base_size
        self.border_size = border_size

        self.dims = self.base_size + self.border_size

        self.centre_pos = (
            self.pos[0] + self.dims[0] / 2,
            self.pos[1] + self.dims[1] / 2,
        )

        self.rect = self.image.get_rect()

    def get_centre_pos(self):
        return self.centre_pos

    def get_colour(self):
        return self.colour

    def get_image(self):
        return self.image

    def get_type(self):
        return self.type

    def get_rect_in_board(self):
        return (
            self.pos[0] + self.border_size[0] / 2,
            self.pos[1] + self.border_size[1] / 2,
            self.dims[0],
            self.dims[1],
        )
