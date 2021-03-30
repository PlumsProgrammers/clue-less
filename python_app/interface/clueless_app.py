# -*- coding: utf-8 -*-
"""Main Clueless Loop"""
import os

import requests

from interface.config import ConfigManager, Router
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

        self.game_name = None
        self.game_id = None
        self.password = None
        self.status = None

        self.player = Player()

    def test_connection(self):
        """Checks connection to Clue-less server"""
        if self._verbose:
            print('Testing Connection...')
        try:
            test_path = os.path.join(self._config.get_host(),
                                     Router.get_path(Router.TEST_CONNECTION))
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

    def create_game(self, game_name, password=None):
        """Create new Clue-less Game server instance"""
        self.game_name = game_name
        self.password = password

        create_game_path = os.path.join(self._config.get_host(),
                                        Router.get_path(Router.CREATE_GAME))
        response = requests.post(create_game_path,
                                 json=Router.get_json_params(game=self,
                                                             player=self.player,
                                                             route=Router.CREATE_GAME)
                                 )
        if response.status_code == 201:
            self.game_id = int(response.json()["id"])
            return True, None
        if response.status_code == 400:
            return False, response.json()
        return False, 'Unknown Error'

    def join_game(self, game_id, username, password=None):
        """Join Existing Clue-less Game server instance"""
        self.player.username = username
        self.password = password
        self.game_id = game_id

        join_game_path = os.path.join(self._config.get_host(),
                                      Router.get_path(Router.JOIN_GAME))
        response = requests.post(join_game_path,
                                 json=Router.get_json_params(game=self,
                                                             player=self.player,
                                                             route=Router.JOIN_GAME)
                                 )
        if response.status_code == 200:
            self.status = response.json()['status']
            players = response.json()['players']
            for player in players:
                if player['username'] == self.player.username:
                    self.player.uuid = player['uuid']
                    break
            message = f'Joining Game as {self.player.username}\n' + \
                      f'Invite your friends with Game Code {self.game_id}'
            return True, message
        if response.status_code == 400:
            return False, response.json()
        return False, 'Unknown Error'

    def start_game(self):
        """Starts connected game if enough players are present"""
        start_game_path = os.path.join(self._config.get_host(),
                                       Router.get_path(Router.START_GAME))
        response = requests.put(start_game_path,
                                json=Router.get_json_params(self.player,
                                                            Router.START_GAME)
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
                                       Router.get_path(Router.CHECK_GAME_STATUS))
        response = requests.get(check_game_path)
        if response.status_code == 200:
            games = response.json()
            for game in games:
                if game['id'] == self.game_id:
                    self.status = game['status']
                    print(f'Game Status: {self.status}')
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
                                       Router.get_path(Router.ACCUSATION))
        response = requests.put(accusation_path,
                                json=Router.get_json_params(self.player,
                                                            Router.ACCUSATION)
                                )
        if response.status_code in [200, 400]:
            if 'turn' in response.content.decode("utf-8"):
                print('Not your turn')
            else:
                print(response.json())

    def about(self):
        """Return information from Clue-less About page"""
        about_page = os.path.join(self._config.get_host(),
                                  Router.get_path(Router.ABOUT))
        return requests.get(about_page).json()

    def help(self):
        """Print out help message descriping action selection"""
        # pylint: disable=no-self-use
        # Member function to match format of other Option functions
        print('\nTo select a move, enter a command or command number.')
        print('Examples:\n\t1\n\tAbout')
