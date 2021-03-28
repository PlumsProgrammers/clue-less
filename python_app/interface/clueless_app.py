# -*- coding: utf-8 -*-
"""Main Clueless Loop"""
import os

import requests

from interface.config import ConfigManager, Router, Routes
from interface.game_objects import Player, Rooms, Suspects, Weapons


class Clueless:
    """Runs local Clue-less instance

    Attributes:
        configuration (ConfigManager): Stores and accesses local
            game information
    """

    def __init__(self, verbose):
        self._verbose = verbose
        self._config = ConfigManager()

        self.game_id = None
        self.password = None

        self.player = Player()
        self.router = Router(self.player)

    def test_connection(self):
        """Checks connection to Clue-less server"""
        if self._verbose:
            print('Testing Connection...')
        try:
            test_path = os.path.join(self._config.get_host(),
                                     self.router.paths[Routes.TEST_CONNECTION])
            test_page = requests.get(test_path)
            try:
                test_page.raise_for_status()
                if self._verbose:
                    print(test_page.json())
                return True
            except requests.exceptions.HTTPError:
                print(test_page.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            print('Clue-less Server not Found, please check connection')
        return False

    def run(self):
        """Runs main game loop until exit conditions met"""
        if self._verbose:
            print("Running Clue-less")

        while True:
            # Find valid player options

            # May need updates to the way this handles allowed options
            if self.player.uuid is None:
                options = self.get_valid_options('find_game')
            elif self.player.status == 'waiting':
                options = self.get_valid_options('waiting')
            elif self.player.status == 'playing':
                options = self.get_valid_options('playing')

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

    def get_valid_options(self, current_status):
        """Find valid player options

        Returns:
            dict containing action names as keys to
                funcions they reference
        """
        options = {}

        if current_status == 'find_game':
            options['new game'] = self.create_game
            options['join game'] = self.join_game

        if current_status == 'waiting':
            options['start game'] = self.start_game
            options['check game status'] = self.check_game_status

        if current_status == 'playing':
            options['make accusation'] = self.make_accusation

        # Always availible, last in list
        options['about'] = self.about
        options['help'] = self.help
        options['exit'] = None

        return options

    def create_game(self):
        """Create new Clue-less Game server instance"""
        game_name = ''
        print('Creating new Game')
        while not game_name:
            game_name = input(
                'Please Provide the Game Name you would like to use:\n')

            if game_name:
                self.player.game_name = game_name
                create_game_path = os.path.join(self._config.get_host(),
                                                self.router.paths[Routes.CREATE_GAME])
                response = requests.post(create_game_path,
                                         json=self.router.get_json_params(self.player,
                                                                          Routes.CREATE_GAME)
                                         )
                if response.status_code == 201:
                    self.player.game_id = int(response.json()["id"])
                    print('Game Started')
                    print(
                        f'Invite Friends using Game Code: {self.player.game_id}')
                    self.join_game()
                else:
                    if response.status_code == 400:
                        print(response.json())
                    game_name = ''

    def join_game(self):
        """Join Existing Clue-less Game server instance"""
        while True:
            while not self.player.username:
                username = input(
                    'Please Provide the username you would like to use:\n')
                if username:
                    self.player.username = username

            while not self.player.game_id:
                game_id = input(
                    'Please the Game Code for the game you would like to join:\n')
                if game_id and game_id.isnumeric():
                    self.player.game_id = int(game_id)

            join_game_path = os.path.join(self._config.get_host(),
                                          self.router.paths[Routes.JOIN_GAME])
            response = requests.post(join_game_path,
                                     json=self.router.get_json_params(self.player,
                                                                      Routes.JOIN_GAME)
                                     )
            if response.status_code == 200:
                self.player.status = response.json()['status']
                players = response.json()['players']
                for player in players:
                    if player['username'] == self.player.username:
                        self.player.uuid = player['uuid']
                        break
                print(f'Joining Game as {self.player.username}')
                break
            if response.status_code == 400:
                print(response.json())
            self.player.username = ''
            self.player.game_id = ''

    def start_game(self):
        """Starts connected game if enough players are present"""
        start_game_path = os.path.join(self._config.get_host(),
                                       self.router.paths[Routes.START_GAME])
        response = requests.put(start_game_path,
                                json=self.router.get_json_params(self.player,
                                                                 Routes.START_GAME)
                                )
        if response.status_code == 200:
            print('Game Started')
            self.player.status = response.json()['status']
        else:
            print('Could not start Game')
            if response.status_code == 400:
                print(response.json())

    def check_game_status(self):
        """Checks game status to see if game has started"""
        check_game_path = os.path.join(self._config.get_host(),
                                       self.router.paths[Routes.CHECK_GAME_STATUS])
        response = requests.get(check_game_path)
        if response.status_code == 200:
            games = response.json()
            for game in games:
                if game['id'] == self.player.game_id:
                    self.player.status = game['status']
                    print(f'Game Status: {self.player.status}')
        else:
            print('Could not find game')

    def make_accusation(self):
        """Make Accusation"""
        person = ''
        place = ''
        thing = ''

        while not person:
            Suspects.print_suspects()
            person = Suspects.get_suspect(input('Select a Suspect:\n'))
        while not place:
            Rooms.print_rooms()
            place = Rooms.get_room(input('Select a Room:\n'))
        while not thing:
            Weapons.print_weapons()
            thing = Weapons.get_weapon(input('Select a Weapon:\n'))

        self.player.guess = (person, place, thing)
        accusation_path = os.path.join(self._config.get_host(),
                                       self.router.paths[Routes.ACCUSATION])
        response = requests.put(accusation_path,
                                json=self.router.get_json_params(self.player,
                                                                 Routes.ACCUSATION)
                                )
        if response.status_code in [200, 400]:
            if 'turn' in response.content.decode("utf-8"):
                print('Not your turn')
            else:
                print(response.json())

    def about(self):
        """Return information from Clue-less About page"""
        about_page = os.path.join(self._config.get_host(),
                                  self.router.paths[Routes.ABOUT])
        return requests.get(about_page).json()

    def help(self):
        """Print out help message descriping action selection"""
        # pylint: disable=no-self-use
        # Member function to match format of other Option functions
        print('\nTo select a move, enter a command or command number.')
        print('Examples:\n\t1\n\tAbout')
