from collections import deque
from grid import Grid


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
        return 'Node({0:+}, {1:+})'.format(self.x, self.y)

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


def apply_delta(dx, dy):
    def getter(coord):
        x, y = coord
        return (x + dx, y + dy)
    return getter


top    = apply_delta(+0, -1)
bottom = apply_delta(+0, +1)
left   = apply_delta(-1, +0)
right  = apply_delta(+1, +0)


def find_first_neq(xs, item):
    for n in xs:
        if n != item:
            return n
    raise ValueError("Item != {0} not found.".format(item))


def maze_transform(maze):
    # invariant: only one entrance and exit.
    assert maze.array[0].count(1) == 1
    assert maze.array[-1].count(1) == 1
    nodes = Grid.from_dim(maze.width, maze.height, NULL_NODE)
    for y, row in enumerate(maze.array):
        for x, cell in enumerate(row):
            # its a wall, do nothing.
            if cell == 0:
                continue
            pos = (x, y)
            tc = maze.get(top(pos), 0)
            bc = maze.get(bottom(pos), 0)
            rc = maze.get(right(pos), 0)
            lc = maze.get(left(pos), 0)
            # horizontal and vertical 'paths' with no junctions
            if tc == bc == 0 and lc == rc == 1:
                nodes[x,y] = nodes.get(left(pos), NULL_NODE)
                continue
            if tc == bc == 1 and lc == rc == 0:
                nodes[x,y] = nodes.get(top(pos), NULL_NODE)
                continue
            # junction or dead ends.
            node = Node(x, y)
            nodes[x,y] = node
            if lc == 1:
                node.left = nodes.get(left(pos), NULL_NODE)
            if tc == 1:
                node.top = nodes.get(top(pos), NULL_NODE)
    root = find_first_neq(nodes.array[0], NULL_NODE)
    tail = find_first_neq(nodes.array[-1], NULL_NODE)
    return root, tail


def children(node):
    yield node.top
    yield node.left
    yield node.right
    yield node.bottom


def breadth_first(root, tail):
    queue = deque([root, node] for node in children(root))
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node is tail:
            return path
        if node is None:
            continue
        for child in children(node):
            if child is None or child.visited:
                continue
            queue.append(path + [child])
            child.visited = True
    return []
