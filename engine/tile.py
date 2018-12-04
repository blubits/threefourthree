"""
A board tile.

:Author:     Maded Batara III
:Version:    v20181125
"""

class Tile:

    def __init__(self, value, base_value, i, j):
        """
        Initializes a new Tile.

        Args:
            value (int): Value of current tile.
            i (int): Row index of tile.
            j (int): Column index of tile.
        """
        self.value = value
        self.i = i
        self.j = j

    def __add__(self, other):
        if not isinstance(other, Tile):
            raise TypeError("cannot add Tile with {0}".format(type(other)))
        self.value += other.value
        return self

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return "[{0:4}]".format(self.value)

    def to_tuple(self):
        return (self.value, self.i, self.j)
