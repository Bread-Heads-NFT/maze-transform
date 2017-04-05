from collections import namedtuple
from random import choice, randint
from mt import make_grid


Pos = namedtuple('Pos', ['x', 'y'])


def width(maze):
    return len(maze[0])


def height(maze):
    return len(maze)


def assign(maze, p, v):
    maze[p.y][p.x] = v


def get(maze, p):
    return maze[p.y][p.x]


def is_legal(maze, pos):
    return 0 <= pos.x < width(maze) and 0 <= pos.y < height(maze)


def dist2(pos):
    x, y = pos
    yield Pos(x + 2, y)
    yield Pos(x - 2, y)
    yield Pos(x, y + 2)
    yield Pos(x, y - 2)


def frontier(maze, pos):
    for p in dist2(pos):
        if is_legal(maze, p) and get(maze, p) == 0:
            yield p


def neighbors(maze, pos):
    for p in dist2(pos):
        if is_legal(maze, p) and get(maze, p) == 1:
            yield p


def between(A, B):
    x = min(A.x, B.x) + 1 if A.x != B.x else A.x
    y = min(A.y, B.y) + 1 if A.y != B.y else A.y
    return Pos(x, y)


def gen(width, height):
    maze = make_grid(width, height - 1, fill=0)
    seed = Pos(randint(0, width - 1), 0)
    assign(maze, seed, 1)
    front = list(frontier(maze, seed))
    explored = set([seed])
    while front:
        idx = randint(0, len(front) - 1)
        cell = front.pop(idx)
        if cell in explored:
            continue
        explored.add(cell)
        assign(maze, cell, 1)
        peer = choice(list(neighbors(maze, cell)))
        assign(maze, between(peer, cell), 1)
        front.extend(frontier(maze, cell))

    entrance = make_entrance(maze[0])
    exit = make_entrance(maze[-1])
    return [entrance] + maze + [exit]


def make_entrance(reference):
    idx = choice([i for i, v in enumerate(reference) if v == 1])
    row = [0] * len(reference)
    row[idx] = 1
    return row
