"""
Instance of the threefourthree game.

:Author:     Maded Batara III
:Version:    2018-11-25
"""

from .board import Board, BoardMovements, Tile
from enum import Enum

class GameState(Enum):
    """
    A list of states that the game is possibly in. Used internally
    by the engine to indicate game state.
    """
    PLAYING = 1             # game still playing
    LOST = 2                # game is lost; board is full and no more moves
    WON = 3                 # game is won; win condition achieved
    KEEP_PLAYING = 4        # win condition achieved but player wants to play

class Game:

    def __init__(self, size, initial_value, initial_tiles, win_condition, game_state=None):
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
            game_state (dict): If the game is loaded from a previous state,
                this describes the state of the game that should be loaded.
                This should be in the same format as what self.game_state()
                returns. (As a consquence, the first three arguments will
                be ignored.) If None, load a new game.
        """
        if game_state is None:
            if initial_tiles > size * size:
                raise ValueError("Too many initial tiles")
            self.board = Board(size, initial_value)
            self.board.insert_random(initial_tiles)
            self.game_status = GameState.PLAYING
            self.score = 0
        else:
            initial_value = game_state["initial_value"]
            win_condition = game_state["win_condition"]
            size = game_state["size"]
            board_state = game_state["board"]
            for i in range(size):
                for j in range(size):
                    if board_state[i][j] is not None:
                        board_state[i][j] = Tile(
                            board_state[i][j], initial_value, i, j)
            self.board = Board(size, initial_value, board=board_state)
            self.game_status = GameState[game_state["status"]]
            self.score = game_state["score"]

        self.size = size
        self.initial_value = initial_value
        self.win_condition = win_condition
        self.win_tile = initial_value ** win_condition

    def game_state(self):
        """
        Returns a dictionary describing the current state of the game. In
        particular, it describes
            (1) the current board, where each tile is represented with
                an integer;
            (2) the current score; and
            (3) the game state: one of "PLAYING", "LOST", "WON", or
                "KEEP_PLAYING";
            (4) the size of the board;
            (5) the value of the base tile; and
            (6) the win condition; i.e. base tile ** win condition is
                the winning tile.
        """
        return {
            "board": self.peek_board(),
            "score": self.score,
            "status": str(self.game_status)[10:],
            "size": self.size,
            "initial_value": self.initial_value,
            "win_condition": self.win_condition
        }

    def peek_board(self):
        """
        Returns a quick "peek" at the board: all tiles on the board have
        been replaced with their values.
        """
        return [[None if tile is None else tile.value for tile in row]
                for row in self.board.board]

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
            self.game_status = GameState.LOST
        if not self.is_continued() and self.win_tile in [t[0] for t in report["merged_tiles"]]:
            self.game_status = GameState.WON
        if not self.is_over() and report["moves_made"]:
            try:
                self.board.insert_random()
            except ValueError:
                pass

    def is_over(self):
        """
        Check if the game is over, i.e. no more moves should be done on the
        board.
        """
        return self.game_status == GameState.WON or self.game_status == GameState.LOST

    def is_won(self):
        """
        Check if the game is won, i.e. the end game tile/win condition
        has been reached.
        """
        return self.game_status == GameState.WON

    def is_lost(self):
        """
        Check if the game is lost, i.e. no more moves are possible.
        """
        return self.game_status == GameState.LOST

    def is_continued(self):
        """
        Check if the game has been continued from a winning game.
        """
        return self.game_status == GameState.KEEP_PLAYING

    def keep_playing(self):
        """
        Set the game to continue even if it has already been won.
        """
        if not self.is_won():
            raise RuntimeError("Can only keep playing if the game is won")
        self.game_status = GameState.KEEP_PLAYING
