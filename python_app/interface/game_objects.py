"""Clue Game Objects
To include Player, Card, Suspect, Weapon, Location
"""
from enum import Enum
import re


class Suspects(Enum):
    """Enum of possible server functions"""

    @staticmethod
    def get_suspect(name):
        """Find Suspect by Name"""
        suspects = {'missscarlet': 'Miss Scarlet',
                    'mrgreen': 'Mr. Green',
                    'colonelmustard': 'Colonel Mustard',
                    'professorplum': 'Professor Plum',
                    'mrspeacock': 'Mrs. Peacock',
                    'mrswhite': 'Mrs. White'}

        return suspects.get(re.sub(r'[^a-z]+', '', name.lower()), None)

    @staticmethod
    def print_suspects():
        """Print all Rooms"""
        print('Miss Scarlet, '
              'Mr. Green, '
              'Colonel Mustard, '
              'Professor Plum, '
              'Mrs. Peacock, '
              'Mrs. White')


class Rooms(Enum):
    """Enum of possible server functions"""

    @staticmethod
    def get_room(room_name):
        """Find Room by Name"""
        rooms = {'ballroom': 'Ballroom',
                 'billiardroom': 'Billiard Room',
                 'conservatory': 'Conservatory',
                 'diningroom': 'Dining Room',
                 'hall': 'Hall',
                 'kitchen': 'Kitchen',
                 'library': 'Library',
                 'lounge': 'Lounge',
                 'study': 'Study'}

        return rooms.get(re.sub(r'[^a-z]+', '', room_name.lower()), None)

    @staticmethod
    def print_rooms():
        """Print all Rooms"""
        print('Ballroom, Billiard Room, Conservatory, '
              'Dining Room, Hall, Kitchen, Library, Lounge, Study')


class Weapons(Enum):
    """Enum of possible server functions"""

    @staticmethod
    def get_weapon(weapon_name):
        """Find Weapon by Name"""
        weapons = {'candlestick': 'Candlestick',
                   'dagger': 'Dagger',
                   'leadpipe': 'Lead Pipe',
                   'revolver': 'Revolver',
                   'rope': 'Rope',
                   'wrench': 'Wrench'}

        return weapons.get(re.sub(r'[^a-z]+', '', weapon_name.lower()), None)

    @staticmethod
    def print_weapons():
        """Print all Rooms"""
        print('Candlestick, '
              'Dagger, '
              'Lead Pipe, '
              'Revolver, '
              'Rope, '
              'Wrench')

# pylint: disable=too-many-instance-attributes # need to move game_name and id to game
class Player:  # pylint: disable=too-few-public-methods # Will need updates
    """Store current Player information"""

    def __init__(self):
        self.username = None
        self.uuid = None
        self.game_id = None
        self.game_name = None
        self.suspect = None
        self.cards = []
        self.location = None
        self.status = None
        self.guess = (None, None, None)
