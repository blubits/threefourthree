"""
A board of tiles.

:Author:     Maded Batara III
:Version:    v20181125
"""

import random
from enum import Enum

from .tile import Tile

class BoardMovements(Enum):
    """
    Directions that the board can move in. Used internally by the
    engine to signal movements to the Board.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Board:
    """
    A board of tiles, part of the TFT engine.
    """

    def __init__(self, size, initial_value, board=None):
        """
        Initializes a new Board.

        Args:
            size (int): The size of the board's side.
            initial_value (int): The value of the base tile in the game.
                In regular 2048 play, this is 2.
            board (list of Tiles, optional): Board to load in, can be
                used to load a saved game. If None, a new Board will
                be loaded.
        """
        if board is None:
            self.board = [[None for _ in range(size)] for i in range(size)]
        else:
            self.board = board
        self.size = size
        self.initial_value = initial_value

    def __iter__(self):
        """
        Returns iter(self).
        """
        return iter(self.board)

    def __len__(self):
        """
        Returns len(self).
        """
        return self.size

    def __str__(self):
        """
        Returns str(self).
        """
        return '\n'.join([
            ' '.join([
                str(tile) if tile is not None else "[    ]" for tile in row
            ]) for row in self.board
        ])

    def available(self):
        """
        Returns a list of available positions on the board.
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
        self.board[tile.i][tile.j] = None

    def insert(self, tile):
        """
        Inserts a tile on the board.
        """
        self.board[tile.i][tile.j] = tile

    def insert_random(self, n=1):
        """
        Inserts n random tiles on the board.
        """
        try:
            random_cells = random.sample(self.available(), n)
        except ValueError:
            raise ValueError("too many tiles to insert")
        for i, j in random_cells:
            if random.random() > 0.9:
                value = self.initial_value * self.initial_value
            else:
                value = self.initial_value
            self.insert(Tile(value, self.initial_value, i, j))

    def is_out_of_bounds(self, i, j):
        """
        Checks if a certain position (i, j) is out of the bounds
        of the board.

        Args:
            i (int): Row index.
            j (int): Column index.
        """
        return not (0 <= i < self.size and 0 <= j < self.size)

    def is_empty(self, i, j):
        """
        Checks if a position (i, j) on the board is empty.

        Args:
            i (int): Row index.
            j (int): Column index.
        """
        return not self.is_out_of_bounds(i, j) and self.tile(i, j) is None

    def is_full(self):
        """
        Checks if the board is already full.
        """
        return not any([tile is None for row in self.board for tile in row])

    def move_all(self, direction):
        """
        Moves all tiles onto a certain direction and merges like tiles
        three - wise.

        Args:
            direction (BoardMovements): The direction of the tiles' movement.

        Returns:
            A report of the game state upon merge, listing (1) the total
            value of all merged tiles, (2) the values of the tiles merged,
            and (3) whether any moves were made on the board itself.
        """

        report = {
            "score": 0,
            "merged_tiles": [],
            "moves_made": False
        }

        v, tile_list = {
            BoardMovements.DOWN: ((1, 0), self.tiles_by_column_reversed()),
            BoardMovements.UP: ((-1, 0), self.tiles_by_column()),
            BoardMovements.RIGHT: ((0, 1), self.tiles_by_row_reversed()),
            BoardMovements.LEFT: ((0, -1), self.tiles_by_row())
        }[direction]

        vi = v[0]
        vj = v[1]

        # 2048 algorithm:
        #   iterate through each tile in the appropriate order,
        #   pushing it towards the wall the specified direction
        #   is going to.
        #
        # This will always work if the iteration order is correct:
        # for example, if we push all tiles left, we iterate
        # row-wise and from the rightmost column.
        for tile in tile_list:
            i = tile.i
            j = tile.j
            while self.is_empty(i + vi, j + vj):
                i += vi
                j += vj
            if i != tile.i or j != tile.j:
                self.move(tile, i, j)
                report["moves_made"] = True
            if not self.is_out_of_bounds(i + (2 * vi), j + (2 * vj)) \
                    and self.tile(i + vi, j + vj) == tile \
                    and self.tile(i + (2 * vi), j + (2 * vj)) == tile:
                # We do three-way merges here
                self.board[i + (2 * vi)][j + (2 * vj)
                                         ] += self.board[i + vi][j + vj]
                self.board[i + (2 * vi)][j + (2 * vj)] += tile
                report["score"] += self.board[i + (2 * vi)][j + (2 * vj)].value
                report["merged_tiles"].append(
                    self.board[i + (2 * vi)][j + (2 * vj)].to_tuple())
                self.delete(tile)
                self.delete(self.board[i + vi][j + vj])
        return report

    def move(self, tile, i, j):
        """
        Moves a tile to the position (i, j).

        Args:
            tile (Tile): Tile to move.
            i (int): Row of the new tile's position.
            j (int): Column of the new tile's position.
        """
        if self.is_out_of_bounds(i, j):
            raise IndexError("Index {0}, {1} out of bounds".format(i, j))
        if not self.is_empty(i, j):
            raise IndexError(
                "A tile already exists at index {0}, {1}".format(i, j))
        self.board[i][j] = tile
        self.delete(tile)
        tile.i = i
        tile.j = j

    def no_moves_possible(self):
        """
        Checks if no more moves are possible.

        Returns:
            True if the board is full and no more merges can be done
            on the board.
        """
        if not self.is_full():
            return False
        vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for tile in self.tiles_by_row():
            for vector in vectors:
                i2 = tile.i + (2 * vector[0])
                j2 = tile.j + (2 * vector[1])
                i = tile.i + vector[0]
                j = tile.j + vector[1]
                if not self.is_out_of_bounds(i2, j2) \
                        and self.tile(i, j) == tile \
                        and self.tile(i2, j2) == tile:
                    return False
        return True

    def tile(self, i, j):
        """
        Returns the tile at (i, j).

        Args:
            i (int): Row index.
            j (int): Column index.
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
