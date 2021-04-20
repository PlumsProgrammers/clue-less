# -*- coding: utf-8 -*-
"""Main Clueless Loop"""
import os

import requests

from interface.config import ConfigManager, Router
from interface.game_objects import Player


class Clueless:  # pylint: disable=too-many-instance-attributes # All attrs required
    """Runs local Clue-less instance

    Attributes:
        configuration (ConfigManager): Stores and accesses local
            game information
    """

    def __init__(self, verbose):
        self._verbose = verbose
        self.config = ConfigManager()

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
            test_path = os.path.join(self.config.get_host(),
                                     Router.get_path(Router.TEST_CONNECTION))
            test_page = requests.get(test_path)
            try:
                test_page.raise_for_status()
                if self._verbose:
                    print(test_page.json())
                return True
            except requests.exceptions.HTTPError:
                if self._verbose:
                    print(test_page.content.decode("utf-8"))
        except requests.exceptions.ConnectionError:
            print('Clue-less Server not Found, please check connection')
        return False

    def create_game(self, game_name, password=None):
        """Create new Clue-less Game server instance"""
        self.game_name = game_name
        self.password = password

        create_game_path = os.path.join(self.config.get_host(),
                                        Router.get_path(Router.CREATE_GAME))
        json = Router.get_json_params(game=self,
                                      player=self.player,
                                      route=Router.CREATE_GAME)
        if not self.password:
            json.pop('password', None)
        response = requests.post(create_game_path,
                                 json=json)
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

        join_game_path = os.path.join(self.config.get_host(),
                                      Router.get_path(Router.JOIN_GAME))
        json = Router.get_json_params(game=self,
                                      player=self.player,
                                      route=Router.JOIN_GAME)
        if not self.password:
            json.pop('password', None)
        response = requests.post(join_game_path,
                                 json=json)

        if response.status_code == 200:
            self.status = response.json()['status']
            players = response.json()['players']
            for player in players:
                if player['username'] == self.player.username:
                    self.player.uuid = player['uuid']
                    break
            message = f'Joining Game as {self.player.username}\n' +\
                f'Invite your friends with Game Code {self.game_id}'
            return True, message
        if response.status_code == 400:
            return False, response.json()
        return False, 'Unknown Error'

    def start_game(self):
        """Starts connected game if enough players are present"""
        start_game_path = os.path.join(self.config.get_host(),
                                       Router.get_path(Router.START_GAME))
        response = requests.put(start_game_path,
                                json=Router.get_json_params(game=self,
                                                            player=self.player,
                                                            route=Router.START_GAME)
                                )
        if response.status_code == 200:
            self.status = response.json()['status']
            players = response.json()['players']
            for player in players:
                if player['username'] == self.player.username:
                    self.player.suspect = player['suspect']
                    break
            return True, 'Game Started'
        if response.status_code == 400:
            return False, response.json()
        return False, 'Unknown Error'

    def check_game_status(self):
        """Checks game status to see if game has started"""
        check_game_path = os.path.join(self.config.get_host(),
                                       Router.get_path(Router.CHECK_GAME_STATUS))
        response = requests.get(check_game_path)
        if response.status_code == 200:
            games = response.json()
            for game in games:
                if game['id'] == self.game_id:
                    self.status = game['status']
                    for player in game['players']:
                        if player['username'] == self.player.username:
                            self.player.uuid = player['uuid']
                            self.player.suspect = player['suspect']
                            self.player.hand = player['cards']
                            break
                    break
            return True, f'Game Status: {self.status}'
        return False, 'Could Not Find Game'

    def move_player(self, room):
        """Move Player to selected Room"""
        self.player.location = room
        move_path = os.path.join(self.config.get_host(),
                                 Router.get_path(Router.MOVE))
        response = requests.put(move_path,
                                json=Router.get_json_params(game=self,
                                                            player=self.player,
                                                            route=Router.MOVE))
        if response.status_code == 200:
            return True, f'Success! Moved to {room}.'
        if response.status_code == 400:
            return False, response.json()
        return False, 'Unknown Error'

    def make_suggestion(self, person, place, thing):
        """Make Suggestion"""
        self.player.suggest = (person, place, thing)
        suggestion_path = os.path.join(self.config.get_host(),
                                       Router.get_path(Router.SUGGESTION))
        response = requests.put(suggestion_path,
                                json=Router.get_json_params(game=self,
                                                            player=self.player,
                                                            route=Router.SUGGESTION)
                                )
        if response.status_code == 200:
            correct = response.json()
            if correct:
                return True, 'Correct, You Win!'
            return False, 'Sorry, You Lose.'
        if response.status_code == 400:
            if 'turn' in response.content.decode("utf-8"):
                message = 'Not your turn'
            else:
                message = response.json()
            return False, message
        return False, 'Unknown Error'

    def make_accusation(self, person, place, thing):
        """Make Accusation"""
        self.player.guess = (person, place, thing)
        accusation_path = os.path.join(self.config.get_host(),
                                       Router.get_path(Router.ACCUSATION))
        response = requests.put(accusation_path,
                                json=Router.get_json_params(game=self,
                                                            player=self.player,
                                                            route=Router.ACCUSATION)
                                )
        if response.status_code == 200:
            correct = response.json()
            if correct:
                return True, 'Correct, You Win!'
            return False, 'Sorry, You Lose.'
        if response.status_code == 400:
            if 'turn' in response.content.decode("utf-8"):
                message = 'Not your turn'
            else:
                message = response.json()
            return False, message
        return False, 'Unknown Error'

    def end_turn(self):
        end_turn_path = os.path.join(self.config.get_host(),
                                       Router.get_path(Router.ENDTURN))
        response = requests.put(end_turn_path,
                                json=Router.get_json_params(game=self,
                                                            player=self.player,
                                                            route=Router.ENDTURN)
                                )
        if response.status_code == 200:
            message = response.json()
        if response.status_code == 400:
            message = response.json()
        return False, 'Unknown Error'

    def about(self):
        """Return information from Clue-less About page"""
        about_page = os.path.join(self.config.get_host(),
                                  Router.get_path(Router.ABOUT))
        return requests.get(about_page).json()
