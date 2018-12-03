"""
Instance of the threefourthree game.

:Author:     Maded Batara III
:Version:    2018-11-25
"""

from .board import Board, BoardMovements
from enum import Enum

class GameState(Enum):
    PLAYING = 1             # game still playing
    LOST = 2                # game is lost; board is full and no more moves
    WON = 3                 # game is won; win condition achieved
    KEEP_PLAYING = 4        # win condition achieved but player wants to play

class Game:

    def __init__(self, size, initial_value, initial_tiles, win_condition):
        """
        Initializes a new three-four-three game.

        Args:
            size (int): Size of board.
            initial_value (int): Initial value of the base tile. All tiles
                will be powers of this tile.
            initial_tiles (int): Initial number of tiles to place on the board.
            win_condition (int): Number of merges done on a single tile
                needed to declare a win condition: alternatively, once
                the tile (initial_value ** win_condition) is on the board,
                the game is won. In the standard 2048 game, win_condition = 11
                (since 2 ** 11 = 2048).
        """
        if initial_tiles > size * size:
            raise ValueError("Too many initial tiles")
        self.board = Board(size, initial_value)
        self.board.insert_random(initial_tiles)
        self.game_state = GameState.PLAYING
        self.win_condition = initial_value ** win_condition
        self.score = 0

    def peek_board(self):
        """
        Returns a quick "peek" at the board: all tiles on the board have
        been replaced with their values.
        """
        return [[None if tile is None else tile.value for tile in row] for row in self.board]

    def move_board(self, direction):
        """
        Moves the board to a certain direction. Direction is one of "up",
        "down", "left", "right".
        """
        if self.is_over():
            raise RuntimeError("Game has been won or lost already")
        if direction.lower() not in ["up", "down", "left", "right"]:
            raise ValueError("{0} is not a valid direction".format(direction))
        directions_dict = {
            "up": BoardMovements.UP,
            "down": BoardMovements.DOWN,
            "left": BoardMovements.LEFT,
            "right": BoardMovements.RIGHT
        }
        direction_value = directions_dict[direction]
        report = self.board.move_all(direction_value)
        self.score += report["score"]
        # check for win/lose conditions
        if self.is_lost():
            self.game_state = GameState.LOST
        if not self.is_continued() and self.win_condition in [t[0] for t in report["merged_tiles"]]:
            self.game_state = GameState.WON
        if not self.is_over() and report["moves_made"]:
            try:
                self.board.insert_random()
            except ValueError:
                pass

    def is_over(self):
        return self.game_state == GameState.WON or self.game_state == GameState.LOST

    def is_won(self):
        return self.game_state == GameState.WON

    def is_lost(self):
        return self.game_state == GameState.LOST

    def is_continued(self):
        return self.game_state == GameState.KEEP_PLAYING

    def keep_playing(self):
        if not self.is_won():
            raise RuntimeError("Can only keep playing if the game is won")
        self.game_state = GameState.KEEP_PLAYING
