import png
import math
from grid import Grid
from collections import Counter


range = getattr(__builtins__, 'xrange', range)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def gradient(i, n):
    b = int(255 * (1 - i / float(n)))
    r = 255 - b
    g = 0
    return r, g, b


def heat_gradient(i, n):
    # yellow = (255, 255, 0)
    g = int(255 * (1 - i / float(n)))
    r = 255
    b = 0
    return r, g, b


def plot_maze(maze):
    grid = Grid.from_dim(maze.width, maze.height, BLACK)
    for y in range(maze.height):
        for x in range(maze.width):
            if maze[x,y] == 1:
                grid[x,y] = WHITE
    return grid


def plot_heatmap(maze, path, filename):
    grid = plot_maze(maze)
    trace = Grid.from_dim(maze.width, maze.height, 0)

    for idx, node in enumerate(path):
        x, y = node.x, node.y
        if idx == 0:
            trace[x, y] = 1
            continue
        prev = path[idx - 1]
        px, py = prev.x, prev.y
        for ix in range(min(x, px), max(x, px) + 1): trace[ix, y] += 1
        for iy in range(min(y, py), max(y, py) + 1): trace[x, iy] += 1

    biggest = max(max(r) for r in trace.array)
    for y, row in enumerate(trace.array):
        for x, v in enumerate(row):
            if trace[x,y] == 0:
                continue
            grid[x,y] = heat_gradient(v, biggest)

    png.from_array(grid.array, mode='RGB').save(filename)


def plot_path(maze, path, filename):
    grid = plot_maze(maze)

    total = len(path)
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
