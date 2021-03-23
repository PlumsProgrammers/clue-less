# -*- coding: utf-8 -*-
"""User Configuration"""
import os
from enum import Enum


class ConfigManager:
    """Stores and access information about local configuration"""

    def __init__(self):
        self._host_location = r'http://localhost:' + \
            os.environ.get('PORT') + '/'
        self._user = os.environ.get('USER')

    def get_host(self):
        """Getter method for path to server"""
        return self._host_location

    def get_user(self):
        """Getter method for username"""
        return self._user


class Routes(Enum):
    """Enum of possible server functions"""
    ABOUT = 0
    TEST_CONNECTION = 1

    CREATE_GAME = 2
    JOIN_GAME = 3
    START_GAME = 4
    CHECK_GAME_STATUS = 5

    SET_CHARACTER = 6
    ACCUSATION = 7


class Router:
    """Stores required information for requests to the Clue-less Server"""

    def __init__(self, player):
        self.paths = {}
        self.json_params = {}

        self.set_paths()
        self.get_json_params(player)

    def set_paths(self):
        """Sets dictionary for Clue-less server paths"""
        self.paths = {Routes.ABOUT: 'about',
                      Routes.TEST_CONNECTION: 'test_connection',

                      Routes.CREATE_GAME: 'games',
                      Routes.CHECK_GAME_STATUS: 'games',
                      Routes.JOIN_GAME: 'games/join',
                      Routes.START_GAME: 'games/start',

                      Routes.SET_CHARACTER: 'players/selectSuspect',

                      Routes.ACCUSATION: 'gameplay/accusation'}

    def get_json_params(self, player, route=None):
        """Sets dictionary for getting require JSON params"""
        self.json_params = {Routes.CREATE_GAME: {'name': player.game_name},
                            Routes.JOIN_GAME: {'username': player.username,
                                               'gameId': player.game_id},
                            Routes.START_GAME: {'gameId': player.game_id},
                            Routes.SET_CHARACTER: {'gameId': player.game_id,
                                                   'uuid': player.uuid,
                                                   'suspect': player.suspect},
                            Routes.ACCUSATION: {'gameId': player.game_id,
                                                'username': player.username,
                                                'accusation': {'suspect': player.guess[0],
                                                               'weapon': player.guess[1],
                                                               'room': player.guess[2]}}
                            }
        return self.json_params.get(route, None)
