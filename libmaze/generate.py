from random import choice, randint
from .grid import Grid


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


def prims(width, height):
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1

    # 0 => wall, 1 => path.
    # need initial cell to start at even index so we
    # get nice walls bounding the maze.
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
        # select a random cell with distance 2 to the current cell
        # and carve out a path between the current cell and said cell.
        peer = choice(list(neighbors(maze, cell)))
        maze[between(peer, cell)] = 1
        front.extend(frontier(maze, cell))
    return wrap(maze)


def recursive_backtrack(width, height):
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1

    maze = Grid.from_dim(width, height - 2, 0)
    # optimisation: we can only put paths on odd numbered indices.
    unexplored = set((x, y) for x, y in maze.indices() if x % 2 == 1)
    stack = []
    cell = (random_even(width), 0)
    unexplored.remove(cell)
    while unexplored:
        maze[cell] = 1
        peers = [p for p in dist2(cell) if maze.legal(p) and p in unexplored]
        if not peers:
            # cannot progress further: either backtrack if possible or terminate.
            if not stack:
                break
            cell = stack.pop()
            continue
        stack.append(cell)
        random_peer = choice(peers)
        maze[between(random_peer, cell)] = 1
        cell = random_peer
        unexplored.remove(random_peer)
    return wrap(maze)


def wrap(maze):
    entrance = make_entrance(maze.array[0])
    exit = make_entrance(maze.array[-1])
    return Grid.from_array([entrance] + maze.array + [exit])


def make_entrance(maze_row):
    idx = choice([i for i, v in enumerate(maze_row) if v == 1])
    row = [0] * len(maze_row)
    row[idx] = 1
    return row
