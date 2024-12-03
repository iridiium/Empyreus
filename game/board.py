import pygame

from collections import deque
from random import randint, choice


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

        self.graph = self.create_graph(self.rows)

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
        graph = {}
        visited = [[tile.type == "empty" for tile in row] for row in rows]

        def dfs(i, j, last_i, last_j):
            visited[i][j] = True

            last_node = (last_j, last_i)
            node = (j, i)

            if last_i is not None and last_j is not None:
                if last_node in graph:
                    graph[last_node].append(node)
                else:
                    graph[last_node] = [node]

                if node in graph:
                    graph[node].append(last_node)
                else:
                    graph[node] = [last_node]

            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if (
                        m >= 0
                        and n >= 0
                        and m < self.size[1]
                        and n < self.size[0]
                        and visited[m][n] is False
                    ):
                        dfs(m, n, i, j)

        islands = []
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if visited[i][j] is False:
                    islands.append([])

                    dfs(i, j, None, None)

        self.graph = graph

        for node in graph:
            for neighbour in self.get_adjacent_nodes(node):
                if self.get_shortest_distance(node, neighbour) > 3:
                    if neighbour in graph:
                        graph[neighbour].append(node)
                    else:
                        graph[neighbour] = [node]

                    if node in graph:
                        graph[node].append(neighbour)
                    else:
                        graph[node] = [neighbour]

        self.graph = graph

        return graph

    def draw(self, window, pos):
        drawn = []
        for node, neighbours in self.graph.items():
            for neighbour in neighbours:
                if [neighbour, node] not in drawn:
                    pygame.draw.line(
                        window,
                        self.line_colour,
                        self.rows[node[1]][node[0]].centre_pos,
                        self.rows[neighbour[1]][neighbour[0]].centre_pos,
                    )

                    drawn.append([node, neighbour])

        for j, row in enumerate(self.rows):
            for i, tile in enumerate(row):
                if i == pos[0] and j == pos[1]:
                    colour = tile.get_colour()
                    rect_object = tile.get_rect_in_board()

                    pygame.draw.rect(
                        window,
                        colour,
                        rect_object,
                    )

                image_rect = tile.get_rect_in_board()
                window.blit(tile.image, image_rect)

    def get_adjacent_nodes(self, pos, dist=1):
        neighbours = []

        for i in range(pos[1] - 1, pos[1] + 2):
            for j in range(pos[0] - 1, pos[0] + 2):
                if i >= 0 and j >= 0 and i < self.size[1] and j < self.size[0]:
                    neighbours.append((j, i))

        if dist > 1:
            for neighbour in neighbours:
                neighbours.extend(get_adjacent_nodes(neighbour, dist - 1))

        return neighbours

    def get_connected_nodes(self, node, dist=1):
        neighbours = []
        if node in self.graph:
            neighbours.extend(self.graph[node])

        if dist > 1:
            for neighbour in neighbours:
                neighbours.extend(get_connected_nodes(neighbour, dist - 1))

        return neighbours

    def get_shortest_distance(self, start, end):
        queue = deque([start])
        dist = {start: 0}

        # DFS
        while queue:
            current = queue.popleft()

            if current == end:
                return dist[current]

            for neighbour in self.get_connected_nodes(current):
                if neighbour not in dist:
                    queue.append(neighbour)
                    dist[neighbour] = dist[current] + 1

        return -1

    def get_random_planet_pos(self):
        return choice(list(self.graph))

    def get_type_at_pos_on_board(self, pos_on_board):
        return self.rows[pos_on_board[1]][pos_on_board[0]].get_type()

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

    def get_colour(self):
        return self.colour

    def get_type(self):
        return self.type

    def get_rect_in_board(self):
        return (
            self.pos[0] + self.border_size / 2,
            self.pos[1] + self.border_size / 2,
            self.size,
            self.size,
        )
