"""
A basic terminal interface.

:Author:     Maded Batara III
:Version:    v20181104
"""

from .interface import Interface

class TerminalInterface(Interface):

    def __init__(self):
        super().__init__()
        self.interface_end = True

    def introduce(self):
        print("Welcome to the three-four-three terminal interface!")
        print()
        self.view_events.create(size=4, initial_value=2,
                                initial_tiles=15, win_condition=11)

    def ask_input(self):
        while True:
            direction = input("Input a direction ('exit' to exit) > ")
            if direction.lower() in ['exit', 'left', 'right', 'up', 'down']:
                break
        if direction == 'exit':
            self.view_events.end()
            self.interface_end = True
        else:
            self.view_events.move(direction.lower())

    def print_board(self):
        print("Score:", self.current_game.score)
        print(self.current_game.board)

    def on_lose(self):
        print("You lost :(")
        self.interface_end = True

    def on_won(self):
        print("You won!")
        ans = input("Want to keep playing? (Y/N) > ")
        if ans.upper() == "Y":
            self.view_events.keep_playing()
        else:
            self.view_events.end()
            self.interface_end = True

    def run(self):
        self.initialize_event_handlers()
        self.introduce()
        self.interface_end = False
        while not self.interface_end:
            self.print_board()
            self.ask_input()
