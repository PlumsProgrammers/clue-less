# -*- coding: utf-8 -*-
"""Script to start Clue-less python front-end, with argument parsing"""
import sys
from argparse import ArgumentParser

from PySide6.QtWidgets import QApplication

from interface.clueless_app import Clueless
from gui.main_gui import MainWindow


class ArgParser(ArgumentParser):
    """Modified ArgumentParser for the Clue-less Game"""

    def __init__(self):
        """Adds required arguemnts to the Parser"""
        super().__init__(description='Play Clue-less, like Clue, only less!')

        self.add_argument('-v', '--verbose',
                          help="Additional output while running",
                          action='store_true')


def main():
    """Creates game instance; runs main loop if connection found"

    Run main.py -h for info on arguments
    """
    parser = ArgParser()
    args = parser.parse_args()

    main_game = Clueless(args.verbose)

    host_found = main_game.test_connection()
    if host_found:
        app = QApplication(sys.argv)
        gui = MainWindow(app)
        gui.show()
        app.exec_()

    print('Exiting...')


if __name__ == '__main__':
    main()
