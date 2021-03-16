# -*- coding: utf-8 -*-
"""Script to start Clue-less python front-end, with argument parsing"""
from argparse import ArgumentParser

from interface.clueless_app import Clueless


class ArgParser(ArgumentParser):
    """Modified ArgumentParser for the Clue-less Game"""

    def __init__(self):
        """Adds required arguemnts to the Parser"""
        super().__init__(description='Play Clue-less, like Clue, only less!')

        self.add_argument('-g', '--gui',
                          help="Run Clueless with gui",
                          action='store_true')
        self.add_argument('-v', '--verbose',
                          help="Additional output while running",
                          action='store_true')


def main():
    """Creates game instance; runs main loop if connection found"

    Run main.py -h for info on arguments
    """
    parser = ArgParser()
    args = parser.parse_args()

    main_game = Clueless(args.verbose,
                         args.gui)

    host_found = main_game.test_connection()
    if host_found:
        main_game.run()

    print('Exiting...')


if __name__ == '__main__':
    main()
