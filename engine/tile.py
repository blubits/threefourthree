"""
A board tile.

:Author:     Maded Batara III
:Version:    v20181125
"""

class Tile:

    def __init__(self, value, base_value, x, y):
        self.base_value = base_value
        self.value = value
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Tile):
            raise TypeError("cannot add Tile with {0}".format(type(other)))
        if other.value != self.value:
            raise ValueError("cannot add two Tiles of different values")
        self.value *= other.base_value
        return self

    def __str__(self):
        return "[{0:4}]".format(self.value)

    def to_tuple(self):
        return (self.value, self.x, self.y)
