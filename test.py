from pprint import pprint
from mt import maze_transform, breadth_first
from mazegen import gen
from vis import plot_maze_path
from grid import Grid

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

root, tail = maze_transform(maze)
path = breadth_first(root, tail)
assert len(path) == 4
assert path == [
    root,
    root.bottom,
    root.bottom.left,
    root.bottom.left.bottom,
]

root, tail = maze_transform(maze2)
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
    head, tail = maze_transform(maze)
    path = breadth_first(head, tail)
    plot_maze_path(maze, path, 'grid-{0}x{1}.png'.format(*dim))
