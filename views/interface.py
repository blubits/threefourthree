"""
Abstract base class for all Interfaces.

:Author:     Maded Batara III
:Version:    v20181126
"""

from engine import ViewEvents

class Interface:
    """A view for the three-four-three game engine.
    """

    def __init__(self):
        """
        Initializes an Interface.

        When subclassing Interface, always make sure to call super().__init__()
        so the controller can communicate with your interface.
        """
        self.view_events = ViewEvents()
        self.controller = None

    @property
    def current_game(self):
        """Game: Current game on the controller."""
        return self.controller.current_game

    def initialize_event_handlers(self):
        """Bind all event handlers to the controller."""
        if self.controller is None:
            raise RuntimeError("Controller not registered in the view yet")
        else:
            self.controller.controller_events.won += self.on_won
            self.controller.controller_events.lost += self.on_lost

    def on_won(self):
        """
        Event handler when the game has been judged as won by the controller.
        """
        raise NotImplementedError

    def on_lost(self):
        """
        Event handler when the game has been judged as lost by the controller.
        """
        raise NotImplementedError

    def run(self):
        """
        Event loop, where your interface should be started. The controller
        will call this function to start your interface up.
        """
        raise NotImplementedError
