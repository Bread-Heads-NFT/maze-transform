from libmaze.generate import recursive_backtrack, prims
from libmaze.grid import Grid
from libmaze.plot import plot_path
from libmaze.solvers import breadth_first, depth_first
from libmaze.transform import transform

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
    (15, 15),
    (50, 50),
    (100, 100),
]


SOLVERS = [
    (depth_first,   'df'),
    (breadth_first, 'bf'),
]

METHODS = [
    (recursive_backtrack, 'rb'),
    (prims,               'pr'),
]


for dim in DIMS:
    for gen, gen_prefix in METHODS:
        for solve, solve_prefix in SOLVERS:
            width, height = dim
            maze = gen(width, height)
            head, tail = transform(maze)
            path = solve(head, tail)
            plot_path(maze, path).save('tmp/grid-{0}x{1}-{2}-{3}.png'.format(
                width,
                height,
                solve_prefix,
                gen_prefix,
                ))
