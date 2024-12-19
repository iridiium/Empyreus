import pygame

from collections import defaultdict, deque
from random import randint, choice

from .helper import find_dist, merge_sort


class Board:

    def __init__(
        self,
        size,
        pos,
        line_colour,
        tile_colour,
        tile_base_size,
        tile_border_size,
        spritesheet,
        tiles,
    ):
        self.size = size
        self.pos = pos
        self.line_colour = line_colour
        self.tile_colour = tile_colour
        self.tile_base_size = tile_base_size
        self.tile_border_size = tile_border_size
        self.spritesheet = spritesheet
        self.tile_order, self.tile_types = self.order_tiles(tiles)

        self.num_planets = sum(
            list(filter(lambda num: num > 0, tiles.values()))
        )
        self.tile_size = self.tile_base_size + self.tile_border_size

        self.rows = [
            [
                Tile(
                    pos=(
                        i * self.tile_size + self.pos[0],
                        j * self.tile_size + self.pos[1],
                    ),
                    colour=tile_colour,
                    image=next(self.tile_order),
                    type=next(self.tile_types),
                    base_size=tile_base_size,
                    border_size=tile_border_size,
                )
                for i in range(self.size[0])
            ]
            for j in range(self.size[1])
        ]

        self.graph, self.num_islands = self.create_graph(self.rows)

    def get_pos(self):
        return self.pos

    def get_tile_size(self):
        return self.tile_size

    def coord_to_board_pos(self, coord):
        return (
            int(
                min(
                    max((coord[0] - self.pos[0]) // self.tile_size, 0),
                    self.size[0] - 1,
                )
            ),
            int(
                min(
                    max((coord[1] - self.pos[1]) // self.tile_size, 0),
                    self.size[1] - 1,
                )
            ),
        )

    def create_graph(self, rows):
        graph = defaultdict(set)
        visited = [[tile.get_type() == "empty" for tile in row] for row in rows]

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
                        0 <= m < self.size[1]
                        and 0 <= n < self.size[0]
                        and not visited[m][n]
                    ):
                        dfs(m, n, i, j, total_targets)

            return

        islands = []
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if not visited[i][j]:
                    island = []
                    dfs(i, j, -1, -1, island)
                    islands.append(island)

        islands = merge_sort(islands, lambda a, b: len(a) > len(b))

        self.graph = graph

        if len(islands) > 1:
            mainland, *isles = islands

            for isle in isles:
                for planet in isle:
                    min_dist = float("inf")
                    min_dist_planet = min(
                        mainland,
                        key=lambda other_planet: find_dist(
                            planet, other_planet
                        ),
                    )

                    graph[planet].add(min_dist_planet)
                    graph[min_dist_planet].add(planet)

        for node in graph:
            for adj in self.get_adj(node):
                if self.get_min_conns_dist(node, adj) > 3:
                    graph[adj].add(node)
                    graph[node].add(adj)

        return graph, islands

    def draw(self, window, mouse_pos_on_board):
        drawn = set()

        for node, conns in self.graph.items():
            for conn in conns:
                edge = frozenset([node, conn])
                if edge not in drawn:
                    pygame.draw.line(
                        window,
                        self.line_colour,
                        self.rows[node[1]][node[0]].get_centre_pos(),
                        self.rows[conn[1]][conn[0]].get_centre_pos(),
                    )

                    drawn.add(edge)

        for j, row in enumerate(self.rows):
            for i, tile in enumerate(row):
                if (i, j) == mouse_pos_on_board:
                    pygame.draw.rect(
                        window,
                        tile.get_colour(),
                        tile.get_rect_in_board(),
                    )

                image_rect = tile.get_rect_in_board()
                window.blit(tile.get_image(), image_rect)

    def get_adj(self, pos, dist=1):
        adjs = []

        for j in range(pos[1] - 1, pos[1] + 2):
            for i in range(pos[0] - 1, pos[0] + 2):
                if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
                    adjs.append((i, j))

        if dist > 1:
            for adj in adjs:
                adjs.extend(get_adj(adj, dist - 1))

        return adjs

    def get_conns(self, node, dist=1):
        adjs = []
        if node in self.graph:
            adjs.extend(self.graph[node])

        if dist > 1:
            for adj in adjs:
                adjs.extend(get_conns(adj, dist - 1))

        return adjs

    def get_min_conns_dist(self, start, end):
        if start == end:
            return 0

        queue = deque([start])
        dist = {start: 0}

        # BFS
        while queue:
            curr = queue.popleft()

            if curr == end:
                return dist[curr]

            for adj in self.get_conns(curr):
                if adj not in dist:
                    queue.append(adj)
                    dist[adj] = dist[curr] + 1

        return -1

    def get_rand_planet_pos(self):
        return choice(list(self.graph))

    def get_type_at_board_pos(self, board_pos):
        return self.rows[board_pos[1]][board_pos[0]].get_type()

    def order_tiles(self, tiles):
        result = []
        tile_types = []
        total = 0

        for tile_type, tile_amount in tiles.items():
            if tile_amount < 0:
                tile_amount = self.size[0] * self.size[1] - total
            else:
                total += tile_amount

            for _ in range(tile_amount):
                target = randint(0, len(result))
                result.insert(
                    target,
                    self.spritesheet.get_sprite_by_name(tile_type),
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

        self.size = self.base_size + self.border_size

        self.centre_pos = (
            self.pos[0] + self.size / 2,
            self.pos[1] + self.size / 2,
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
            self.pos[0] + self.border_size / 2,
            self.pos[1] + self.border_size / 2,
            self.size,
            self.size,
        )
