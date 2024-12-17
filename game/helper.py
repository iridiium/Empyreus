from math import sqrt


def find_dist(coord1, coord2):
    return sqrt(((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2))


def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
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
