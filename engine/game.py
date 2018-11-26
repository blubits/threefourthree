"""
Instance of the threefourthree game.

:Author:     Maded Batara III
:Version:    2018-11-25
"""

from .board import Board

class Game:

    def __init__(self, size, initial_value):
        self.board = Board(size, initial_value)
