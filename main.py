"""
Main launch file to start the game and process launch options.

:Author:     Maded Batara III
:Author:     Jose Enrico Salinas
:Version:    v20181013
"""

import sys

from views import TerminalInterface
from controller import Controller

USAGE = """Usage: python main.py [-d] [--help]
Load the three-four-three game.
    -t              run in terminal mode (default)
    -d              run in desktop mode
    -h, --help      show this help message"""

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(USAGE)
        exit(0)

    if '-d' in sys.argv:
        print("Whoops! That doesn't exist yet")
        exit(0)
    else:
        interface_mode = TerminalInterface()

    controller = Controller(interface=interface_mode)
    controller.run_interface()

if __name__ == "__main__":
    main()
