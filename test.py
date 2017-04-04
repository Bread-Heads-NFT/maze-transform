from pprint import pprint
from mt import maze_transform, breadth_first
from mazegen import gen
from vis import Table

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

maze  = gen(300, 300)
table = Table(300, 300)
for y, row in enumerate(maze):
    for x, value in enumerate(row):
        if value == 0:
            table.rows[y][x].color = "#000"
head, tail = maze_transform(maze)
path = breadth_first(head, tail)
for idx, node in enumerate(path):
    table.rows[node.y][node.x].color = 'red'
    if idx == 0:
        continue
    prev = path[idx - 1]
    if abs(prev.y - node.y) > 0:
        for y in range(min(node.y, prev.y), max(node.y, prev.y) + 1):
            table.rows[y][node.x].color = 'red'
    if abs(prev.x - node.x) > 0:
        for x in range(min(node.x, prev.x), max(node.x, prev.x) + 1):
            table.rows[node.y][x].color = 'red'
print(table.render())
