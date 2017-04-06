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


def plot_heatmap(maze, path):
    grid = plot_maze(maze)
    trace = Grid.from_dim(maze.width, maze.height, 0)

    for prev, node in prev_curr(path):
        x, y = node.x, node.y
        if prev is None:
            trace[x,y] = 1
            continue
        px, py = prev.x, prev.y
        for ix in range(min(x, px), max(x, px) + 1): trace[ix,y] += 1
        for iy in range(min(y, py), max(y, py) + 1): trace[x,iy] += 1

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
        x, y = node.x, node.y
        grid[x,y] = color
        if prev is None:
            continue
        px, py = prev.x, prev.y
        for iy in range(min(y, py), max(y, py) + 1): grid[x,iy] = color
        for ix in range(min(x, px), max(x, px) + 1): grid[ix,y] = color

    return png.from_array(grid.array, mode='RGB')
