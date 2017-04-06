from ._compat import zip
from .grid import Grid
from libmaze.vendor.png import Reader
from libmaze.plot import BLACK


def chunk3(xs):
    u = [iter(xs)] * 3
    return zip(*u)


def maze_from_file(filename):
    r = Reader(filename=filename)
    width, height, data, _ = r.asRGB()
    maze = Grid.from_dim(width, height, 0)
    for y, row in enumerate(data):
        for x, pixel in enumerate(chunk3(row)):
            maze[x,y] = 0 if pixel == BLACK else 1
    return maze
