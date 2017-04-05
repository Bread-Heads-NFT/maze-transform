from collections import namedtuple
from random import choice, randint
from grid import Grid, Pos


def dist2(pos):
    x, y = pos
    yield Pos(x + 2, y)
    yield Pos(x - 2, y)
    yield Pos(x, y + 2)
    yield Pos(x, y - 2)


def frontier(grid, pos):
    return (p for p in dist2(pos) if grid.get(p) == 0)


def neighbors(grid, pos):
    return (p for p in dist2(pos) if grid.get(p) == 1)


def between(A, B):
    x = min(A.x, B.x) + 1 if A.x != B.x else A.x
    y = min(A.y, B.y) + 1 if A.y != B.y else A.y
    return Pos(x, y)


def gen(width, height):
    maze = Grid.from_dim(width, height - 1, fill=0)
    seed = Pos(randint(0, width - 1), 0)
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
