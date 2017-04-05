import png
import math
from grid import Grid


range = getattr(__builtins__, 'xrange', range)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def gradient(i, n):
    b = int(255 * (1 - i / float(n)))
    r = 255 - b
    g = 0
    return r, g, b


def plot_maze_path(maze, path, filename):
    grid = Grid.from_dim(maze.width, maze.height, BLACK)
    total = len(path)

    for y in range(maze.height):
        for x in range(maze.width):
            if maze[x,y] == 1:
                grid[x,y] = WHITE

    for idx, node in enumerate(path):
        color = gradient(idx + 1, total)
        x, y = node.x, node.y
        grid[x,y] = color
        if idx == 0:
            continue
        prev = path[idx - 1]
        px, py = prev.x, prev.y
        for iy in range(min(y, py), max(y, py) + 1): grid[x,iy] = color
        for ix in range(min(x, px), max(x, px) + 1): grid[ix,y] = color

    png.from_array(grid.array, mode='RGB').save(filename)
