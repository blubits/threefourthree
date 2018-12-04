"""
Controller class for the threefourthree game.

:Author:     Maded Batara III
:Version:    v20181126
"""

from engine import Game, ControllerEvents

class Controller:

    def __init__(self, interface):
        """
        Initializes a new Controller.
        """
        self.current_game = None
        self.interface = interface

        # Enable two-way comms between interface and view
        self.interface.controller = self
        self.controller_events = ControllerEvents()

        # register view event handlerrs
        self.interface.view_events.create += self.on_create
        self.interface.view_events.move += self.on_move
        self.interface.view_events.keep_playing += self.on_keep_playing
        self.interface.view_events.end += self.on_end

    def game_state(self):
        return {
            "board": self.current_game.peek_board(),
            "score": self.current_game.score,
            "state": str(self.current_game.game_state)[10:]
        }

    def on_create(self, *args, **kwargs):
        self.current_game = Game(*args, **kwargs)

    def on_move(self, direction):
        self.current_game.move_board(direction)
        if self.current_game.is_lost():
            self.controller_events.lost()
        if self.current_game.is_won():
            self.controller_events.won()

    def on_keep_playing(self):
        self.current_game.keep_playing()

    def on_end(self):
        self.current_game = None

    def run_interface(self):
        self.interface.run()
