from pprint import pprint
from mt import maze_transform, top, bottom, left, right

maze = [
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]

root, tail = maze_transform(maze)
for row in maze:
    print(row)
