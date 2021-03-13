# -*- coding: utf-8 -*-
"""Main Clueless Loop"""
import os

import requests

from interface.config import ConfigManager


class Clueless:
    """Runs local Clue-less instance

    Attributes:
        configuration (ConfigManager): Stores and accesses local
            game information
    """

    def __init__(self, verbose, show_gui):
        self._verbose = verbose
        self._show_gui = show_gui
        self.configuration = ConfigManager()

    def test_connection(self):
        """Checks connection to Clue-less server"""
        if self._verbose:
            print('Testing Connection...')

        try:
            host = self.configuration.get_host()
            requests.get(host)
            if self._verbose:
                print(f'Server found at {host}')
            return True
        except requests.exceptions.ConnectionError:
            print('Clue-less Server not Found, please check connection')
            return False

    def run(self):
        """Runs main game loop until exit conditions met"""
        if self._verbose:
            print("Running Clue-less")

        while True:
            # Find valid player options
            options = self.get_valid_options()
            option_list = list(options.keys())
            print('\nSelect your action')
            for idx, option in enumerate(options.keys()):
                print(f'\n\t{idx + 1} {option.title()}')
            user_selection = input('')

            # Determine seleciton if integer is provided
            if user_selection.isnumeric():
                selection_num = int(user_selection)
                if selection_num - 1 < len(option_list):
                    user_selection = option_list[int(user_selection) - 1]
                else:
                    user_selection = 'help'

            # Take appropriate action, defaulting to 'Help'
            action = options.get(user_selection.lower(),
                                 options['help'])

            if action is not None:
                action()
            else:
                break

    def get_valid_options(self):
        """Find valid player options

        Returns:
            dict containing action names as keys to
                funcions they reference
        """
        options = {}

        # Need some way to find valid player options

        # Always availible, last in list
        options['about'] = self.about
        options['help'] = self.help
        options['exit'] = None

        return options

    def about(self):
        """Print out information from Clue-less About page"""
        about_page = os.path.join(self.configuration.get_host(),
                                  'about')
        print('\n', requests.get(about_page).content.decode("utf-8"))

    def help(self):
        """Print out help message descriping action selection"""
        print('\nTo select a move, enter a command or command number.')
        print('Examples:\n\t1\n\tAbout')
