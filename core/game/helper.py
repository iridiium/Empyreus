import pygame

from collections import deque
from copy import deepcopy
from math import sqrt
from random import randint, random, randrange


# Graph-related


def get_conns(graph, node, dist=1):
    """Gets all elements in graph connected to a node."""
    adjs = []
    if node in graph:
        adjs.extend(graph[node])

    if dist > 1:
        for adj in adjs:
            adjs.extend(get_conns(adj, dist - 1))

    return adjs


def get_min_conns_dist(graph, start, end):
    """Gets the smallest number of nodes on a path from start to end."""
    if start == end:
        return 0

    queue = deque([start])
    dist = {start: 0}

    # BFS
    while queue:
        curr = queue.popleft()

        if curr == end:
            return dist[curr]

        for conn in get_conns(graph, curr):
            if conn not in dist:
                queue.append(conn)
                dist[conn] = dist[curr] + 1

    return -1


# Matrix-related


def get_adjs(matrix, pos, dist=1):
    """Gets all elements in matrix at indices adjacent to the index at pos."""
    adjs = []

    for j in range(pos[1] - 1, pos[1] + 2):
        for i in range(pos[0] - 1, pos[0] + 2):
            if 0 <= i < len(matrix[0]) and 0 <= j < len(matrix):
                adjs.append((i, j))

    if dist > 1:
        for adj in adjs:
            adjs.extend(get_adj(adj, dist - 1))

    return adjs


def find_dist(coord1, coord2):
    """Finds the Euclidean distance between coord1 and coord2."""
    return sqrt(((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2))


# Sorting
def merge_sort(arr, key=lambda a, b: a < b):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
    """Merges two lists together. Order is determined by key()."""
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if key(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result + left[i:] + right[j:]


# Other
def gen_colour():
    return tuple(randint(0, 255) for _ in range(3))
