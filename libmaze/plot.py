import math
from .grid import Grid
from ._compat import range
from .vendor import png


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def prev_curr(xs):
    prev = None
    for curr in xs:
        yield prev, curr
        prev = curr


def path_gradient(i, n):
    b = int(255 * (1 - i / float(n)))
    r = 255 - b
    g = 0
    return r, g, b


def heat_gradient(i, n):
    # yellow = (255, 255, 0
    g = int(255 * (1 - i / float(n)))
    r = 255
    b = 0
    return r, g, b


def plot_maze(maze):
    grid = Grid.from_dim(maze.width, maze.height, BLACK)
    for x, y in maze.indices():
        if maze[x,y] == 1:
            grid[x,y] = WHITE
    return grid


def autorange(a, b):
    return range(
            min(a, b),
            max(a, b) + 1,
            )


def path_between(prev, node):
    for x in autorange(node.x, prev.x): yield x, node.y
    for y in autorange(node.y, prev.y): yield node.x, y


def plot_heatmap(maze, path):
    grid = plot_maze(maze)
    trace = Grid.from_dim(maze.width, maze.height, 0)

    for prev, node in prev_curr(path):
        prev = node if prev is None else prev
        for x, y in path_between(prev, node):
            trace[x,y] += 1

    biggest = max(max(r) for r in trace)
    for x, y in trace.indices():
        if trace[x,y] == 0:
            continue
        grid[x,y] = heat_gradient(trace[x,y], biggest)

    return png.from_array(grid.array, mode='RGB')


def plot_path(maze, path):
    grid = plot_maze(maze)

    total = len(path)
    for idx, (prev, node) in enumerate(prev_curr(path)):
        color = path_gradient(idx + 1, total)
        prev = node if prev is None else prev
        for x, y in path_between(prev, node):
            grid[x,y] = color

    return png.from_array(grid.array, mode='RGB')
