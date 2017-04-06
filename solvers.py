from collections import deque
from random import choice
from mt import NULL_NODE


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


def random_mouse(root, tail):
    path = [root]
    node = root
    while True:
        node = choice([
            n for n in children(node)
            if n != None and n != NULL_NODE
            ])
        path.append(node)
        if node is tail:
            break
    return path
