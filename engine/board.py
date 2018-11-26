"""
A board of tiles.

:Author:     Maded Batara III
:Version:    v20181125
"""

from .tile import Tile
import random
from enum import Enum

class BoardMovements(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Board:

    def __init__(self, size, initial_value):
        self.board = [[None for _ in range(size)] for i in range(size)]
        self.size = size
        self.initial_value = initial_value

    def __len__(self):
        return self.size

    def __str__(self):
        return '\n'.join([
            ' '.join([
                str(tile) if tile is not None else "[    ]" for tile in row
            ]) for row in self.board
        ])

    def available(self):
        """
        List of available positions on the board.
        """
        cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.tile(i, j) is None:
                    cells.append((i, j))
        return cells

    def delete(self, tile):
        """
        Deletes a tile from the board.
        """
        self.board[tile.x][tile.y] = None

    def insert(self, tile):
        """
        Inserts a tile on the board.
        """
        self.board[tile.x][tile.y] = tile

    def insert_random(self, n=1):
        """
        Inserts n random tiles on the board.
        """
        random_cells = random.sample(self.available(), n)
        for i, j in random_cells:
            if random.random() > 0.9:
                value = self.initial_value * self.initial_value
            else:
                value = self.initial_value
            self.insert(Tile(value, i, j))

    def is_out_of_bounds(self, i, j):
        """
        Checks if a certain position (i, j) is out of the bounds
        of the board.
        """
        return not (0 <= i < self.size and 0 <= j < self.size)

    def is_empty(self, i, j):
        """
        Checks if a position (i, j) on the board is empty.
        """
        return not self.is_out_of_bounds(i, j) and self.tile(i, j) is None

    def move_all(self, direction):
        """
        Moves all tiles onto a certain direction and merges
        like tiles.
        """
        if direction == BoardMovements.DOWN:
            vector = (1, 0)
            tile_list = self.tiles_by_column_reversed()
        elif direction == BoardMovements.UP:
            vector = (-1, 0)
            tile_list = self.tiles_by_column()
        elif direction == BoardMovements.RIGHT:
            vector = (0, 1)
            tile_list = self.tiles_by_row_reversed()
        elif direction == BoardMovements.LEFT:
            vector = (0, -1)
            tile_list = self.tiles_by_row()
        for tile in tile_list:
            i = tile.x
            j = tile.y
            while self.is_empty(i + vector[0], j + vector[1]):
                i += vector[0]
                j += vector[1]
            if i != tile.x or j != tile.y:
                self.move(tile, i, j)
            if not self.is_out_of_bounds(i + vector[0], j + vector[1]) and self.tile(i + vector[0], j + vector[1]).value == tile.value:
                self.board[i + vector[0]][j + vector[1]] += tile
                self.delete(tile)

    def move(self, tile, i, j):
        if self.is_out_of_bounds(i, j):
            raise IndexError("Index {0}, {1} out of bounds".format(i, j))
        if not self.is_empty(i, j):
            raise IndexError(
                "A tile already exists at index {0}, {1}".format(i, j))
        self.board[i][j] = tile
        self.delete(tile)
        tile.x = i
        tile.y = j

    def tile(self, i, j):
        """
        Returns the tile at (i, j).
        """
        return self.board[i][j]

    def tiles_by_column(self):
        """
        Returns an iterator through each tile, by column.
        """
        for j in range(self.size):
            for i in range(self.size):
                if self.board[i][j] is not None:
                    yield self.board[i][j]

    def tiles_by_column_reversed(self):
        """
        Returns an iterator through each tile, by column and in reverse.
        """
        for j in range(self.size):
            for i in range(self.size - 1, -1, -1):
                if self.board[i][j] is not None:
                    yield self.board[i][j]

    def tiles_by_row(self):
        """
        Returns an iterator through each tile, by row.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    yield self.board[i][j]

    def tiles_by_row_reversed(self):
        """
        Returns an iterator through each tile, by row and in reverse.
        """
        for i in range(self.size):
            for j in range(self.size - 1, -1, -1):
                if self.board[i][j] is not None:
                    yield self.board[i][j]
