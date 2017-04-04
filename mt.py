from functools import partial


maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    ]


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
        self.visited = False

    def __repr__(self):
        return 'Node({0}, {1})'.format(self.x, self.y)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        node._right = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        node._left = self

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, node):
        self._top = node
        node._bottom = self

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, node):
        self._bottom = node
        node._top = self


NULL_NODE = Node(-1, -1)
NULL_NODE.visited = True


def get_bounded(delta, maze, coord, default=NULL_NODE):
    dx, dy = delta
    x0, y0 = coord
    x = x0 + dx
    y = y0 + dy
    print(x, y)
    if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
        return maze[y][x]
    return default


top    = partial(get_bounded, (0, -1))
bottom = partial(get_bounded, (0, +1))
left   = partial(get_bounded, (-1, 0))
right  = partial(get_bounded, (+1, 0))


def maze_transform(maze):
    # invariant: only one entrance and exit.
    assert maze[0].count(1) == 1
    assert maze[-1].count(1) == 1

    row = [NULL_NODE] * len(maze[0])
    nodes = [row.copy() for _ in range(len(maze))]
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            # its a wall, do nothing.
            if cell == 0:
                continue
            pos = (x, y)
            tc = top(maze, pos, 0)
            bc = bottom(maze, pos, 0)
            rc = right(maze, pos, 0)
            lc = left(maze, pos, 0)
            no_paths = tc + bc + rc + lc
            if no_paths == 4:
                node = Node(x, y)
                nodes[y][x] = node
                node.left = left(nodes, pos)
                node.top = top(nodes, pos)
                continue
            if no_paths == 3:
                node = Node(x, y)
                nodes[y][x] = node
                if lc == 1:
                    node.left = left(nodes, pos)
                if tc == 1:
                    node.top = top(nodes, pos)
                continue
            if no_paths == 1:
                node = Node(x, y)
                nodes[y][x] = node
                if lc == 1:
                    node.left = left(nodes, pos)
                if tc == 1:
                    node.top = top(nodes, pos)
                continue
            assert no_paths == 2
            if tc == 1 and bc == 1:
                nodes[y][x] = top(nodes, pos)
                continue
            if lc == 1 and rc == 1:
                nodes[y][x] = left(nodes, pos)
                continue
            if tc == 0 and rc == 0:
                node = Node(x, y)
                nodes[y][x] = node
                node.left = left(nodes, pos)
                continue
            if tc == 0 and lc == 0:
                node = Node(x, y)
                nodes[y][x] = node
                continue
            if bc == 0 and lc == 0:
                node = Node(x, y)
                nodes[y][x] = node
                node.top = top(nodes, pos)
                continue
            if bc == 0 and rc == 0:
                node = Node(x, y)
                nodes[y][x] = node
                node.top = top(nodes, pos)
                node.left = left(nodes, pos)
                continue
    print(nodes)
    root = NULL_NODE
    for node in nodes[0]:
        if node is not NULL_NODE:
            root = node
    tail = NULL_NODE
    for node in nodes[-1]:
        if node is not NULL_NODE:
            tail = node
    assert root != NULL_NODE
    assert tail != NULL_NODE
    return root, tail
