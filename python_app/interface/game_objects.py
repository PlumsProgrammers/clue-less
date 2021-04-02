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
    def get_suspect_list():
        """Returns list of all Suspects"""
        return ['Miss Scarlet',
                'Mr. Green',
                'Colonel Mustard',
                'Professor Plum',
                'Mrs. Peacock',
                'Mrs. White']

    @staticmethod
    def get_starting_positions():
        """Get Suspect Starting Positions"""
        return {'Miss Scarlet': 'Hall-Lounge-Hallway',
                'Mr. Green': 'Ballroom-Conservatory-Hallway',
                'Colonel Mustard': 'Dining Room-Lounge-Hallway',
                'Professor Plum': 'Library-Study-Hallway',
                'Mrs. Peacock': 'Conservatory-Library-Hallway',
                'Mrs. White': 'Ballroom-Kitchen-Hallway'}


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
    def get_relative_positions():
        """Return Relative Locations for each space (width, height)"""
        return {'Ballroom': (0.5, 0.9),
                'Billiard Room': (0.5, 0.5),
                'Conservatory': (0.1, 0.9),
                'Dining Room': (0.9, 0.5),
                'Hall': (0.5, 0.1),
                'Kitchen': (0.9, 0.9),
                'Library': (0.1, 0.5),
                'Lounge': (0.9, 0.1),
                'Study': (0.1, 0.1),
                'Ballroom-Billiard Room-Hallway': (0.5, 0.7),
                'Ballroom-Conservatory-Hallway': (0.3, 0.9),
                'Ballroom-Kitchen-Hallway': (0.7, 0.9),
                'Billiard Room-Dining Room-Hallway': (0.7, 0.5),
                'Billiard Room-Hall-Hallway': (0.5, 0.3),
                'Billiard Room-Library-Hallway': (0.3, 0.5),
                'Conservatory-Library-Hallway': (0.1, 0.7),
                'Dining Room-Kitchen-Hallway': (0.9, 0.7),
                'Dining Room-Lounge-Hallway': (0.9, 0.3),
                'Hall-Lounge-Hallway': (0.7, 0.1),
                'Hall-Study': (0.3, 0.1),
                'Library-Study-Hallway': (0.1, 0.3)}

    @staticmethod
    def get_location_list():
        """Returns list of all Rooms"""
        return list(Rooms.get_relative_positions().keys())

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
        self.cards = []
        self.location = None
        self.turn = None
        self.guess = (None, None, None)
