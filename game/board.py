import pygame
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

    def get_random_planet_pos(self):
        return choice(list(self.graph))

    def get_neighbours(self, target_pos):
        if target_pos in self.graph:
            return self.graph[target_pos]
        return []

    def get_type_at_pos_on_board(self, pos_on_board):
        return self.rows[pos_on_board[1]][pos_on_board[0]].get_type()

    def order_tiles(self, tiles):
        result = []
        tile_types = []

        for tile_type, tile_amount in tiles.items():
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

    def create_graph(self, rows):
        graph = {}
        visited = [[tile.type == "empty" for tile in row] for row in rows]

        def dfs(i, j, last_i, last_j):
            visited[i][j] = True

            if last_i is not None and last_j is not None:
                last_node = (last_j, last_i)
                node = (j, i)

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
                        and m < len(visited)
                        and n < len(visited[0])
                        and visited[m][n] is False
                    ):
                        dfs(m, n, i, j)

        islands = []
        for i in range(len(rows)):
            for j in range(len(rows[0])):
                if visited[i][j] is False:
                    islands.append([])

                    dfs(i, j, None, None)

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
