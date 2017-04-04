from pprint import pprint
from mt import maze_transform, breadth_first, make_grid
from mazegen import gen
from vis import plot_maze_path

maze = [
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]

maze2 = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0],
]

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


maze = gen(100, 100)
head, tail = maze_transform(maze)
path = breadth_first(head, tail)
plot_maze_path(maze, path, 'grid.png')
