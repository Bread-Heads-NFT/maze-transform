from pprint import pprint
from collections import deque
from random import choice, randint
from mt import make_grid


def bounded_pos(pos, grid):
    x, y = pos
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return pos
    return None


def legal_deltas(pos, grid, deltas):
    x, y = pos
    for dx, dy in deltas:
        coord = (x + dx, y + dy)
        coord = bounded_pos(coord, grid)
        if coord is None:
            continue
        yield coord


def gen(width, height):
    maze = make_grid(width, height-1, fill=0)
    head = randint(0, width-1)
    maze[0][head] = 1

    frontier = [(head, 0)]
    visited = set(frontier)
    while frontier:
        pos = frontier.pop()
        points = legal_deltas(pos, maze, [
            (+0, -1),
            (+0, +1),
            (-1, +0),
            (+1, +0),
        ])
        for point in points:
            if point in visited:
                continue
            visited.add(point)
            x, y = point
            if y == 0:
                continue
            value = choice((0, 1))
            if all(v == 0 for v in maze[y]):
                value = 1
            maze[y][x] = value
            if value == 1:
                frontier.append(point)

    # add the exit
    indices = [i for i, v in enumerate(maze[-1]) if v == 1]
    last = [0] * width
    last[choice(indices)] = 1
    maze.append(last)
    return maze
