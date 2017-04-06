from random import choice, randint
from .grid import Grid


range = getattr(__builtins__, 'xrange', range)


def dist2(pos):
    x, y = pos
    yield x + 2, y
    yield x - 2, y
    yield x, y + 2
    yield x, y - 2


def frontier(grid, pos):
    return (p for p in dist2(pos) if grid.get(p) == 0)


def neighbors(grid, pos):
    return (p for p in dist2(pos) if grid.get(p) == 1)


def between(A, B):
    x0, y0 = A
    x1, y1 = B
    x = min(x0, x1) + 1 if x0 != x1 else x0
    y = min(y0, y1) + 1 if y0 != y1 else y0
    return x, y


def random_even(width):
    while True:
        r = randint(2, width - 1)
        if r % 2 == 0:
            return r - 1


def gen(width, height):
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1

    maze = Grid.from_dim(width, height - 2, fill=0)
    seed = (random_even(width), 0)
    maze[seed] = 1
    front = list(frontier(maze, seed))
    explored = set([seed])
    while front:
        idx = randint(0, len(front) - 1)
        cell = front.pop(idx)
        if cell in explored:
            continue
        explored.add(cell)
        maze[cell] = 1
        peer = choice(list(neighbors(maze, cell)))
        maze[between(peer, cell)] = 1
        front.extend(frontier(maze, cell))

    entrance = make_entrance(maze.array[0])
    exit = make_entrance(maze.array[-1])
    return Grid.from_array([entrance] + maze.array + [exit])


def make_entrance(reference):
    idx = choice([i for i, v in enumerate(reference) if v == 1])
    row = [0] * len(reference)
    row[idx] = 1
    return row
