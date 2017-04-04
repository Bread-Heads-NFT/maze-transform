import png
from mt import make_grid


BLACK = (0, 0, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)


def dim(maze):
    return len(maze[0]), len(maze)


def plot_maze_path(maze, path, filename):
    width, height = dim(maze)
    array = make_grid(width, height, BLACK)

    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                array[y][x] = WHITE

    for idx, node in enumerate(path):
        x, y = node.x, node.y
        array[y][x] = RED
        if idx == 0:
            continue
        prev = path[idx - 1]
        px, py = prev.x, prev.y
        for iy in range(min(y, py), max(y, py) + 1): array[iy][x] = RED
        for ix in range(min(x, px), max(x, px) + 1): array[y][ix] = RED

    png.from_array(array, mode='RGB').save(filename)
