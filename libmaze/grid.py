from ._compat import range


class Grid:
    def __init__(self, width, height, array):
        self.width = width
        self.height = height
        self.array = array

    def __getitem__(self, pos):
        return self.array[pos[1]][pos[0]]

    def __setitem__(self, pos, value):
        self.array[pos[1]][pos[0]] = value

    def __iter__(self):
        return iter(self.array)

    def indices(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x,y

    def values(self):
        for y, row in enumerate(self.array):
            for x, v in enumerate(row):
                yield (x, y), v

    def legal(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def get(self, pos, default=None):
        if self.legal(pos):
            return self[pos]
        return default

    @classmethod
    def from_dim(cls, width, height, fill):
        row = [fill] * width
        array = [row[:] for _ in range(height)]
        return cls(width, height, array)

    @classmethod
    def from_array(cls, array):
        width = len(array[0])
        height = len(array)
        return cls(width, height, array)
