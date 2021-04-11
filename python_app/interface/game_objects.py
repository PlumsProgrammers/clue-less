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
                    'drorchid': 'Dr. Orchid'}

        return suspects.get(re.sub(r'[^a-z]+', '', name.lower()), None)

    @staticmethod
    def get_suspect_list():
        """Returns list of all Suspects"""
        return ['Miss Scarlet',
                'Mr. Green',
                'Colonel Mustard',
                'Professor Plum',
                'Mrs. Peacock',
                'Dr. Orchid']


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
    def get_room_list():
        """Returns list of all Rooms"""
        return ['Ballroom', 'Billiard Room', 'Conservatory',
                'Dining Room', 'Hall', 'Kitchen',
                'Library', 'Lounge', 'Study']


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
    def get_weapon_list():
        """Returns list of all Rooms"""
        return ['Candlestick',
                'Dagger',
                'Lead Pipe',
                'Revolver',
                'Rope',
                'Wrench']


class Player:  # pylint: disable=too-few-public-methods # Will need updates
    """Store current Player information"""

    def __init__(self):
        self.username = None
        self.uuid = None
        self.suspect = None
        self.hand = []
        self.location = None
        self.turn = None
        self.guess = (None, None, None)
