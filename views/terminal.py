"""
A basic terminal interface.

:Author:     Maded Batara III
:Version:    v20181104
"""

from .interface import Interface

import os
import json

class TerminalInterface(Interface):

    def __init__(self):
        super().__init__()
        self.interface_end = True

    def introduce(self):
        print("Welcome to the three-four-three terminal interface!")
        print()
        if os.path.exists("save.json"):
            print("Loading from a saved game...")
            with open("save.json") as infile:
                game_state = json.load(infile)
            self.view_events.create(size=6, initial_value=3,
                                    initial_tiles=1, win_condition=10,
                                    game_state=game_state)
        else:
            self.view_events.create(size=6, initial_value=3,
                                    initial_tiles=1, win_condition=10)

    def ask_input(self):
        while True:
            direction = input("Input a direction ('exit'/'save') > ")
            if direction.lower() in ['save', 'exit', 'left', 'right', 'up', 'down']:
                break
        if direction == 'exit':
            self.view_events.end()
            self.interface_end = True
        elif direction == 'save':
            game_state = self.controller.game_state()
            with open("save.json", "w") as outfile:
                json.dump(game_state, outfile)
            self.view_events.end()
            self.interface_end = True
        else:
            self.view_events.move(direction.lower())

    def print_board(self):
        print("Score:", self.current_game.score)
        print(self.current_game.board)
        print(self.controller.game_state())

    def on_lost(self):
        print("You lost :(")
        if os.path.exists("save.json"):
            os.remove("save.json")
        self.interface_end = True

    def on_won(self):
        print("You won!")
        ans = input("Want to keep playing? (Y/N) > ")
        if ans.upper() == "Y":
            self.view_events.keep_playing()
        else:
            self.view_events.end()
            self.interface_end = True
            if os.path.exists("save.json"):
                os.remove("save.json")

    def run(self):
        self.initialize_event_handlers()
        self.introduce()
        self.interface_end = False
        while not self.interface_end:
            self.print_board()
            self.ask_input()
