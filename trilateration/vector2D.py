from math import sqrt


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2D(self.x / other, self.y / other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return sqrt(self.x*self.x + self.y*self.y)

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    @staticmethod
    def average_vector(vectors):
        """
        Finds the average of multiple vectors
        :param vectors: List[Vector2D, Vector2D, ...]
        :return: Vector2D
        """
        # Returns the average vector from a list of vectors
        return Vector2D(*tuple(sum(n) / len(n) for n in zip(*vectors)))
