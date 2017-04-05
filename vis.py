import png
import math
from mt import make_grid


BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)


def dim(maze):
    return len(maze[0]), len(maze)


def gradient(i, n):
    b = math.ceil(255 * (1 - i / float(n)))
    r = 255 - b
    g = 0
    return r, g, b


def plot_maze_path(maze, path, filename):
    width, height = dim(maze)
    array = make_grid(width, height, BLACK)
    total = len(path)

    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                array[y][x] = WHITE

    for idx, node in enumerate(path):
        color = gradient(idx + 1, total)
        x, y = node.x, node.y
        array[y][x] = color
        if idx == 0:
            continue
        prev = path[idx - 1]
        px, py = prev.x, prev.y
        for iy in range(min(y, py), max(y, py) + 1): array[iy][x] = color
        for ix in range(min(x, px), max(x, px) + 1): array[y][ix] = color

    png.from_array(array, mode='RGB').save(filename)
