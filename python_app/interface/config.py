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


class Router(Enum):
    """Enum of possible server functions"""
    ABOUT = 0
    TEST_CONNECTION = 1

    CREATE_GAME = 2
    JOIN_GAME = 3
    START_GAME = 4
    CHECK_GAME_STATUS = 5

    SET_CHARACTER = 6
    MOVE = 7
    SUGGESTION = 8
    RESPONSE = 9
    ACCUSATION = 10
    ENDTURN = 11

    PUBLIC = 12
    PRIVATE = 13

    SUSPECT = 14

    @staticmethod
    def get_path(route=None):
        """Sets dictionary for Clue-less server paths"""
        paths = {Router.ABOUT: 'about',
                 Router.TEST_CONNECTION: 'test_connection',

                 Router.CREATE_GAME: 'games',
                 Router.CHECK_GAME_STATUS: 'games',
                 Router.JOIN_GAME: 'games/join',
                 Router.START_GAME: 'games/start',

                 Router.SET_CHARACTER: 'players/selectSuspect',

                 Router.MOVE: 'gameplay/move',
                 Router.SUGGESTION: 'gameplay/suggestion',
                 Router.RESPONSE: 'gameplay/suggestion_response',
                 Router.ACCUSATION: 'gameplay/accusation',
                 Router.ENDTURN: 'gameplay/end_turn',

                 Router.PUBLIC: 'messages/game',
                 Router.PRIVATE: 'messages/private',

                 Router.SUSPECT: 'players/selectSuspect'}
        return paths.get(route, None)

    @staticmethod
    def get_json_params(game, player, route=None):
        """Sets dictionary for getting require JSON params"""
        json_params = {Router.CREATE_GAME: {'name': game.game_name,
                                            'password': game.password},
                       Router.JOIN_GAME: {'username': player.username,
                                          'gameId': game.game_id,
                                          'password': game.password},
                       Router.START_GAME: {'gameId': game.game_id},
                       Router.SET_CHARACTER: {'gameId': game.game_id,
                                              'uuid': player.uuid,
                                              'suspect': player.suspect},
                       Router.MOVE: {'gameId': game.game_id,
                                     'username': player.username,
                                     'location': player.location},
                       Router.SUGGESTION: {'gameId': game.game_id,
                                           'username': player.username,
                                           'suggestion': {'suspect': player.guess[0],
                                                          'room': player.guess[1],
                                                          'weapon': player.guess[2]}},
                       Router.RESPONSE: {'gameId': game.game_id,
                                         'username': player.username},
                       Router.ACCUSATION: {'gameId': game.game_id,
                                           'username': player.username,
                                           'accusation': {'suspect': player.guess[0],
                                                          'room': player.guess[1],
                                                          'weapon': player.guess[2]}},
                       Router.ENDTURN: {'gameId': game.game_id,
                                        'username': player.username},

                       Router.PUBLIC: {'gameId': game.game_id,
                                       'username': player.username,
                                       'message': None},
                       Router.PRIVATE: {'gameId': game.game_id,
                                        'username': player.username,
                                        'targetUsername': None,
                                        'message': None},
                       Router.SUSPECT: {'gameId': game.game_id,
                                        'username': player.username,
                                        'suspect': player.suspect}
                       }
        return json_params.get(route, None)
