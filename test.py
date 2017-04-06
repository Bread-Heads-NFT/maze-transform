from libmaze.transform import transform
from libmaze.generate import gen
from libmaze.plot import plot_path
from libmaze.solvers import breadth_first
from libmaze.grid import Grid

maze = Grid.from_array([
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
])

maze2 = Grid.from_array([
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0],
])

root, tail = transform(maze)
path = breadth_first(root, tail)
assert len(path) == 4
assert path == [
    root,
    root.bottom,
    root.bottom.left,
    root.bottom.left.bottom,
]

root, tail = transform(maze2)
path = breadth_first(root, tail)
assert len(path) == 7
assert path == [
    root,
    root.bottom,
    root.bottom.left,
    root.bottom.left.bottom,
    root.bottom.left.bottom.bottom,
    root.bottom.left.bottom.bottom.right,
    root.bottom.left.bottom.bottom.right.bottom,
]


DIMS = [
    (10, 10),
    (50, 50),
    (10, 100),
    (100, 100),
    (500, 500),
]


for dim in DIMS:
    maze = gen(*dim)
    head, tail = transform(maze)
    path = breadth_first(head, tail)
    plot_path(maze, path).save('grid-{0}x{1}.png'.format(*dim))
