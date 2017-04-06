from grid import Grid


class Node:
    __slots__ = ('x', 'y', 'left', 'right', 'top', 'bottom', 'visited')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.visited = False

    def __repr__(self):
        return 'Node({0:+}, {1:+})'.format(self.x, self.y)


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
                peer = nodes.get(left(pos), NULL_NODE)
                node.left = peer
                peer.right = node
            if tc == 1:
                peer = nodes.get(top(pos), NULL_NODE)
                node.top = peer
                peer.bottom = node
    root = find_first_neq(nodes.array[0], NULL_NODE)
    tail = find_first_neq(nodes.array[-1], NULL_NODE)
    return root, tail
